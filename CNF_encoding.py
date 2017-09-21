import numpy as np


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
def encode_constraints(sudoku, Dim, names):
    encode = []
    for row in range(Dim):
        for column in range(Dim):
            if (sudoku[row, column] != 0):
                arr = [names[row, column, sudoku[row, column] - 1].tolist()]
                encode.insert(0, arr)
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


def encode_sudoku(sudoku, Dim):
    names = sudoku_names(Dim)
    encode = []
    constraints = encode_constraints(sudoku, Dim, names)
    encode.extend(constraints)

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


def decode_sudoku(solution, Dim):
    names = sudoku_names(Dim)
    sudoku = np.zeros([Dim, Dim], dtype=np.int)
    indexes = []
    for el in solution:
        if el > 0:
            index = np.where(names == el)
            for num in index:
                sudoku[index[0], index[1]] = index[2] + 1

    print(sudoku)


def reduce_clause(clause, k, var_count):
    clause_1 = clause[:(k - 1)]
    clause_2 = clause[(k - 1):]
    clause_1.append(var_count + 1)
    clause_2.append(-1 * (var_count + 1))

    return clause_1, clause_2


def k_SAT(dim, code, k):
    encode = []
    variables = dim ** 3
    for clause in code:

        while len(clause) > k:
            clause_1, clause_2 = reduce_clause(clause, k, variables)
            clause = clause_2
            encode.append(clause_1)
            variables += 1
        encode.append(clause)

    return encode, variables


def encoding_CNF(encode, var2):
    import os
    data = encode
    with open(os.path.join("./", "sudoku.txt"), "w") as writer:
        # var = str(var2) + str(len(encode))
        writer.write("p cnf {0} {1}".format(str(var2), str(len(encode))))
        for d in data:
            writer.write("{} 0 \n".format(" ".join(str(_) for _ in d)))
