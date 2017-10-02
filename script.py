import cnf_encoding as cnf
import os
import numpy as np


# define global variables and paths
START, END = 4000, 4010
PUZZLE_SIZE = 3
puzzle_size = PUZZLE_SIZE ** 2
PUZZLE_DIR = "./puzzles/" + str(PUZZLE_SIZE) + "/"
ENCODE_DIR_N = "./encodings/" + str(PUZZLE_SIZE) + "/naive/"
ENCODE_DIR_3SAT = "./encodings/" + str(PUZZLE_SIZE) + "/3_sat/"
ENCODE_DIR_L = "./encodings/" + str(PUZZLE_SIZE) + "/layered/"

# define the grid
sudoku = np.zeros((puzzle_size, puzzle_size))

# encode the general rules
encode_general_3sat, var_count_3sat = cnf.general_encoding_3sat(puzzle_size)
encode_general_l, var_count_l = cnf.general_encoding_l(puzzle_size)
encode_general_n = cnf.general_encoding(puzzle_size)


# import the sudoku from txt file
for index in range(START, END + 1):
    complete_encode_n = list(encode_general_n)
    complete_encode_l = list(encode_general_l)
    complete_encode_3sat = list(encode_general_3sat)

    with open(os.path.join(PUZZLE_DIR, "{}.txt".format(index))) as reader:
        sudoku_read = reader.read()
        sudoku_lines = [s for s in sudoku_read.split('\n')]
        actual_sudoku = []
        for element in sudoku_lines[:-1]:
            arr = [int(n) for n in element.split(',')]
            actual_sudoku.append(arr)

        for thing in actual_sudoku:
            sudoku[thing[0], thing[1]] = thing[2]

    # add constrains
    constraints = cnf.encode_constraints(sudoku)
    complete_encode_n.extend(constraints)
    complete_encode_l.extend(constraints)
    complete_encode_3sat.extend(constraints)

    # translate into CNF
    encode_n = cnf.encoding_CNF(complete_encode_n, puzzle_size ** 3, index, ENCODE_DIR_N)
    encode_l = cnf.encoding_CNF(complete_encode_l, var_count_l + len(constraints), index, ENCODE_DIR_L)
    encode_3sat = cnf.encoding_CNF(complete_encode_3sat, var_count_3sat + len(constraints), index, ENCODE_DIR_3SAT)


    print('Sudoku {} encoded'.format(index))


