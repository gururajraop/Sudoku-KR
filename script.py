import CNF_encoding_Linda as CNF
import better_encoding as be
import os
import numpy as np

START, END = 4000, 4100
PUZZLE_SIZE = 4
puzzle_size = PUZZLE_SIZE ** 2
PUZZLE_DIR = "./puzzles/" + str(PUZZLE_SIZE) + "/"
ENCODE_DIR = "./encodings/" + str(PUZZLE_SIZE) + "/"

sudoku = np.zeros((puzzle_size, puzzle_size))
# encode, var_count = be.general_encoding_3sat(puzzle_size)
# encode, var_count = be.general_encoding_normal(puzzle_size)
encode = CNF.general_encoding(puzzle_size)

for index in range(START, END + 1):
    complete_encode = list(encode)
    with open(os.path.join(PUZZLE_DIR, "{}.txt".format(index))) as reader:
        sudoku_read = reader.read()
        sudoku_lines = [s for s in sudoku_read.split('\n')]
        actual_sudoku = []
        for element in sudoku_lines[:-1]:
            arr = [int(n) for n in element.split(',')]
            actual_sudoku.append(arr)

        for thing in actual_sudoku:
            sudoku[thing[0], thing[1]] = thing[2]
    # print sudoku
    constraints = CNF.encode_constraints(sudoku)
    complete_encode.extend(constraints)


    encode_n = CNF.encoding_CNF(complete_encode, puzzle_size ** 3, index, PUZZLE_SIZE)
    # encode_n = CNF.encoding_CNF(complete_encode, var_count+len(constraints), index, PUZZLE_SIZE)

    # encode_3sat = CNF.k_SAT(puzzle_size, complete_encode, 3)
    # encode_CNF_3sat = CNF.encoding_CNF(encode_3sat[0], puzzle_size**3, index, PUZZLE_SIZE)

    print('Sudoku {} encoded'.format(index))


