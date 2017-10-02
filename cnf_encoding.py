import numpy as np
import os
import math


def sudoku_names(Dim):
    names = np.zeros([Dim, Dim, Dim], dtype=np.int)

    for i in range(Dim):
        for j in range(Dim):
            for k in range(Dim):
                names[i][j][k] = (i * Dim * Dim) + (j * Dim) + k + 1
    return names


def encode_at_most_one(names):
    encode = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            arr = [-1 * names[i], -1 * names[j]]
            encode.insert(0, arr)
    return encode


def encode_at_least_one(names):
    return [names]


def encode_exactly_one(names):
    encode = []
    at_most_one = encode_at_most_one(names)
    at_least_one = encode_at_least_one(names)
    encode.extend(at_least_one)
    encode.extend(at_most_one)
    return encode


# add constrains
def encode_constraints(sudoku):
    Dim = len(sudoku)
    names = sudoku_names(Dim)
    encode = []
    for row in range(Dim):
        for column in range(Dim):
            if sudoku[row, column] != 0:
                arr = [names[row, column, int(sudoku[row, column]) - 1].tolist()]
                encode.append(arr)
    return encode


def isSquare(number):
    if (np.sqrt(number) - int(np.sqrt(number))):
        return False
    else:
        return True


def get_block_positions(Dim):
    block_size = int(np.sqrt(Dim))
    block_positions = np.zeros([block_size], dtype=int)
    for pos in range(block_size):
        block_positions[pos] = block_size * pos

    return block_positions


def general_encoding(Dim):
    names = sudoku_names(Dim)
    encode = []
    # for each cell, exactly one value
    for row in range(Dim):
        for column in range(Dim):
            cell_poss_values = names[row, column, :]
            cell_encode = encode_exactly_one(cell_poss_values.tolist())
            encode.extend(cell_encode)

    # for each row, for each value, only one is true
    for row in range(Dim):
        for value in range(Dim):
            row_poss_values = names[row, :, value]
            row_encode = encode_exactly_one(row_poss_values.tolist())
            encode.extend(row_encode)

    # for each column, for each value, only one is true
    for column in range(Dim):
        for value in range(Dim):
            column_poss_values = names[:, column, value]
            column_encode = encode_exactly_one(column_poss_values.tolist())
            encode.extend(column_encode)

    # for each block, for each value, only one is true
    if isSquare(Dim):
        block_pos = get_block_positions(Dim)
        for row in block_pos:
            for column in block_pos:
                for value in range(Dim):
                    block_poss_values = names[row:row + block_pos[1], column:column + block_pos[1], value].flatten()
                    block_encode = encode_exactly_one(block_poss_values.tolist())
                    encode.extend(block_encode)

    return encode


def encode_sudoku(sudoku):
    encode = general_encoding(sudoku)
    Dim = len(sudoku)
    names = sudoku_names(Dim)
    constraints = encode_constraints(sudoku)
    encode.extend(constraints)

    return encode


def decode_sudoku(solution, Dim):
    names = sudoku_names(Dim)
    sudoku = np.zeros([Dim, Dim], dtype=np.int)
    for el in solution:
        if el > 0:
            index = np.where(names == el)
            sudoku[index[0], index[1]] = index[2] + 1

    print(sudoku)


def reduce_clause(clause, k, var_count):
    clause_1 = clause[:(k - 1)]
    clause_2 = clause[(k - 1):]
    clause_1.extend([var_count + 1])
    clause_2.extend([-1 * (var_count + 1)])

    return clause_1, clause_2


def k_SAT(dim, code, k):
    encode = []
    variables = dim ** 3
    for clause in code:
        while len(clause) > k:
            clause_1, clause_2 = reduce_clause(clause, k, variables)
            clause = clause_2[:]
            encode.append(clause_1)
            variables += 1
        encode.append(clause)

    return encode, variables


def encoding_CNF(encode, var2, puzzle_no, ENCODING_DIR):

    with open(os.path.join(ENCODING_DIR, "{}.txt".format(puzzle_no)), "w") as writer:
        writer.write("p cnf {} {} \n".format(str(var2), str(len(encode))))
        for d in encode:
            writer.write("{} 0 \n".format(" ".join(str(_) for _ in d)))


def encode_dummy_var_l(names, var_count):
    encode = []
    DIM = len(names)
    dim = int(math.sqrt(DIM))
    new_variables = []
    # split variables into groups
    for i in range(0, DIM, dim):
        # add dummy variable
        var_count = var_count + 1
        new_variables.append(var_count)

        # encode at most one of the variables
        actual_variables = names[i:(i + dim)]
        encode.extend(encode_at_most_one(actual_variables))

        # encode -c => -a, -b, -c
        for number in actual_variables:
            encode.append([(-1) * number, var_count])

        # encode c => a, b ,c
        missing_string = names[i:(i + dim)]
        missing_string.extend([(-1) * var_count])
        encode.append(missing_string)

    return encode, var_count, new_variables


def encode_dummy_var_3sat(names, var_count, k):
    encode = []
    DIM = len(names)
    dim = k
    new_variables = []

    if 0 == DIM % 2:
        for i in range(0, DIM, dim):
            var_count += 1
            new_variables.append(var_count)

            actual_variables = names[i:(i + dim)]
            encode.extend(encode_at_most_one(actual_variables))
            for number in actual_variables:
                encode.append([(-1) * number, var_count])

            missing_string = names[i:(i + dim)]
            missing_string.extend([(-1) * var_count])
            encode.append(missing_string)

    else:
        for i in range(0, DIM - 1, dim):
            var_count += 1
            new_variables.append(var_count)

            actual_variables = names[i:(i + dim)]
            encode.extend(encode_at_most_one(actual_variables))
            for number in actual_variables:
                encode.append([(-1) * number, var_count])

            missing_string = names[i:(i + dim)]
            missing_string.extend([(-1) * var_count])
            encode.append(missing_string)
        new_variables.append(names[DIM - 1])

    return encode, var_count, new_variables


def general_encoding_3sat(dim):
    names = sudoku_names(dim)
    encode = []
    var_count = dim ** 3
    k = 2
    # for each cell, exactly one value
    for row in range(dim):
        for column in range(dim):
            cell_poss_values = names[row, column, :]
            cell_encode, var_count, new_variables = encode_dummy_var_3sat(cell_poss_values.tolist(), var_count, k)
            encode.extend(cell_encode)
            while len(new_variables) > 3:
                cell_encode, var_count, new_variables = encode_dummy_var_3sat(new_variables, var_count, k)
                encode.extend(cell_encode)

            encode.extend(encode_exactly_one(new_variables))

    # for each row, for each value, only one is true
    for row in range(dim):
        for value in range(dim):
            row_poss_values = names[row, :, value]
            row_encode, var_count, new_variables = encode_dummy_var_3sat(row_poss_values.tolist(), var_count, k)
            encode.extend(row_encode)
            while len(new_variables) > 3:
                cell_encode, var_count, new_variables = encode_dummy_var_3sat(new_variables, var_count, k)
                encode.extend(cell_encode)
            encode.extend(encode_exactly_one(new_variables))

    # for each column, for each value, only one is true
    for column in range(dim):
        for value in range(dim):
            column_poss_values = names[:, column, value]
            column_encode, var_count, new_variables = encode_dummy_var_3sat(column_poss_values.tolist(), var_count, k)
            encode.extend(column_encode)
            while len(new_variables) > 3:
                cell_encode, var_count, new_variables = encode_dummy_var_3sat(new_variables, var_count, k)
                encode.extend(cell_encode)
            encode.extend(encode_exactly_one(new_variables))

    # for each block, for each value, only one is true
    if isSquare(dim):
        block_pos = get_block_positions(dim)
        for row in block_pos:
            for column in block_pos:
                for value in range(dim):
                    block_poss_values = names[row:row + block_pos[1], column:column + block_pos[1], value].flatten()
                    block_encode, var_count, new_variables = encode_dummy_var_3sat(block_poss_values.tolist(),
                                                                                   var_count, k)
                    encode.extend(block_encode)
                    while len(new_variables) > 3:
                        cell_encode, var_count, new_variables = encode_dummy_var_3sat(new_variables, var_count, k)
                        encode.extend(cell_encode)
                    encode.extend(encode_exactly_one(new_variables))

    return encode, var_count


def general_encoding_l(dim):
    names = sudoku_names(dim)
    encode = []
    var_count = dim ** 3
    # for each cell, exactly one value
    for row in range(dim):
        for column in range(dim):
            cell_poss_values = names[row, column, :]
            cell_encode, var_count, new_variables = encode_dummy_var_l(cell_poss_values.tolist(), var_count)
            encode.extend(cell_encode)
            encode.extend(encode_exactly_one(new_variables))

    # for each row, for each value, only one is true
    for row in range(dim):
        for value in range(dim):
            row_poss_values = names[row, :, value]
            row_encode, var_count, new_variables = encode_dummy_var_l(row_poss_values.tolist(), var_count)
            encode.extend(row_encode)
            encode.extend(encode_exactly_one(new_variables))

    # for each column, for each value, only one is true
    for column in range(dim):
        for value in range(dim):
            column_poss_values = names[:, column, value]
            column_encode, var_count, new_variables = encode_dummy_var_l(column_poss_values.tolist(), var_count)
            encode.extend(column_encode)
            encode.extend(encode_exactly_one(new_variables))

    # for each block, for each value, only one is true
    if isSquare(dim):
        block_pos = get_block_positions(dim)
        for row in block_pos:
            for column in block_pos:
                for value in range(dim):
                    block_poss_values = names[row:row + block_pos[1], column:column + block_pos[1], value].flatten()
                    block_encode, var_count, new_variables = encode_dummy_var_l(block_poss_values.tolist(), var_count)
                    encode.extend(block_encode)
                    encode.extend(encode_exactly_one(new_variables))

    return encode, var_count

