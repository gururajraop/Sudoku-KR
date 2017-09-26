import math
import CNF_encoding_Linda as CNF


def encode_dummy_var_normal(names, var_count):
    encode = []
    DIM = len(names)
    dim = int(math.sqrt(DIM))
    new_variables = []
    for i in range(0, DIM, dim):
        var_count = var_count + 1
        new_variables.append(var_count)

        actual_variables = names[i:(i + dim)]
        encode.extend(CNF.encode_at_most_one(actual_variables))
        for number in actual_variables:
            encode.append([(-1) * number, var_count])

        missing_string = names[i:(i + dim)]
        missing_string.extend([(-1) * var_count])
        encode.append(missing_string)

    return encode, var_count, new_variables

def encode_dummy_var_3sat(names, var_count, k):
    encode = []
    DIM = len(names)
    dim = k
    new_variables = []

    if DIM % 2 == 0:
        for i in range(0, DIM, dim):
            var_count += 1
            new_variables.append(var_count)

            actual_variables = names[i:(i + dim)]
            encode.extend(CNF.encode_at_most_one(actual_variables))
            for number in actual_variables:
                encode.append([(-1) * number, var_count])

            missing_string = names[i:(i + dim)]
            missing_string.extend([(-1) * var_count])
            encode.append(missing_string)

    else:
        for i in range(0, DIM-1, dim):
            var_count += 1
            new_variables.append(var_count)

            actual_variables = names[i:(i + dim)]
            encode.extend(CNF.encode_at_most_one(actual_variables))
            for number in actual_variables:
                encode.append([(-1) * number, var_count])

            missing_string = names[i:(i + dim)]
            missing_string.extend([(-1) * var_count])
            encode.append(missing_string)
        new_variables.append(names[DIM-1])

    return encode, var_count, new_variables

def general_encoding_3sat(dim):
    names = CNF.sudoku_names(dim)
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

            encode.extend(CNF.encode_exactly_one(new_variables))

    # for each row, for each value, only one is true
    for row in range(dim):
        for value in range(dim):
            row_poss_values = names[row, :, value]
            row_encode, var_count, new_variables = encode_dummy_var_3sat(row_poss_values.tolist(), var_count, k)
            encode.extend(row_encode)
            while len(new_variables) > 3:
                cell_encode, var_count, new_variables = encode_dummy_var_3sat(new_variables, var_count, k)
                encode.extend(cell_encode)
            encode.extend(CNF.encode_exactly_one(new_variables))

    # for each column, for each value, only one is true
    for column in range(dim):
        for value in range(dim):
            column_poss_values = names[:, column, value]
            column_encode, var_count, new_variables = encode_dummy_var_3sat(column_poss_values.tolist(), var_count, k)
            encode.extend(column_encode)
            while len(new_variables) > 3:
                cell_encode, var_count, new_variables = encode_dummy_var_3sat(new_variables, var_count, k)
                encode.extend(cell_encode)
            encode.extend(CNF.encode_exactly_one(new_variables))

    # for each block, for each value, only one is true
    if CNF.isSquare(dim):
        block_pos = CNF.get_block_positions(dim)
        for row in block_pos:
            for column in block_pos:
                for value in range(dim):
                    block_poss_values = names[row:row + block_pos[1], column:column + block_pos[1], value].flatten()
                    block_encode, var_count, new_variables = encode_dummy_var_3sat(block_poss_values.tolist(), var_count,k)
                    encode.extend(block_encode)
                    while len(new_variables) > 3:
                        cell_encode, var_count, new_variables = encode_dummy_var_3sat(new_variables, var_count, k)
                        encode.extend(cell_encode)
                    encode.extend(CNF.encode_exactly_one(new_variables))

    return encode, var_count



def general_encoding_normal(dim):
    names = CNF.sudoku_names(dim)
    encode = []
    var_count = dim ** 3
    # for each cell, exactly one value
    for row in range(dim):
        for column in range(dim):
            cell_poss_values = names[row, column, :]
            cell_encode, var_count, new_variables = encode_dummy_var_normal(cell_poss_values.tolist(), var_count)
            encode.extend(cell_encode)
            # while len(new_variables) > 3:
            #     cell_encode, var_count, new_variables = encode_dummy_var_3sat(new_variables, var_count, k)
            #     encode.extend(cell_encode)

            encode.extend(CNF.encode_exactly_one(new_variables))

    # for each row, for each value, only one is true
    for row in range(dim):
        for value in range(dim):
            row_poss_values = names[row, :, value]
            row_encode, var_count, new_variables = encode_dummy_var_normal(row_poss_values.tolist(), var_count)
            encode.extend(row_encode)
            # while len(new_variables) > 3:
            #     cell_encode, var_count, new_variables = encode_dummy_var_3sat(new_variables, var_count, k)
            #     encode.extend(cell_encode)
            encode.extend(CNF.encode_exactly_one(new_variables))

    # for each column, for each value, only one is true
    for column in range(dim):
        for value in range(dim):
            column_poss_values = names[:, column, value]
            column_encode, var_count, new_variables = encode_dummy_var_normal(column_poss_values.tolist(), var_count)
            encode.extend(column_encode)
            # while len(new_variables) > 3:
            #     cell_encode, var_count, new_variables = encode_dummy_var_3sat(new_variables, var_count, k)
            #     encode.extend(cell_encode)
            encode.extend(CNF.encode_exactly_one(new_variables))

    # for each block, for each value, only one is true
    if CNF.isSquare(dim):
        block_pos = CNF.get_block_positions(dim)
        for row in block_pos:
            for column in block_pos:
                for value in range(dim):
                    block_poss_values = names[row:row + block_pos[1], column:column + block_pos[1], value].flatten()
                    block_encode, var_count, new_variables = encode_dummy_var_normal(block_poss_values.tolist(), var_count)
                    encode.extend(block_encode)
                    # while len(new_variables) > 3:
                    #     cell_encode, var_count, new_variables = encode_dummy_var_3sat(new_variables, var_count, k)
                    #     encode.extend(cell_encode)
                    encode.extend(CNF.encode_exactly_one(new_variables))

    return encode, var_count
