import CNF_encoding_Linda as CNF

with open(‘./solution.txt') as reader:
    file_solution = reader.read()
    solution = [s for s in file_solution.split(' ')]
    solution[0:1] = solution[0].split('\n')
    actual_solution = solution[1:-1]
    actual_solution = [int(s) for s in actual_solution]



# print actual_solution
CNF.decode_sudoku(actual_solution, 9)