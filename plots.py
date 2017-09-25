import os
import numpy as np
import matplotlib.pyplot as plt

START, END = 4000, 4100
PUZZLE_SIZE = 3
puzzle_size = PUZZLE_SIZE**2
STAT_DIR_N = "./stat/"+str(PUZZLE_SIZE)+"/"
STAT_DIR_3SAT = "./stat/"+str(PUZZLE_SIZE)+"_3SAT/"
STAT_DIR_BE = "./stat/"+str(PUZZLE_SIZE)+"_BE/"

file_names = ["final_conflicts_cpu",
              "final_conflicts_literals", "final_conflicts", "final_cpu_time",
              "final_decisions_cpu", "final_decisions", "final_memory",
              "final_propagation_cpu", "final_propagation"]

x = np.arange(START, END + 1)

for i in range(len(file_names)):

    with open(os.path.join(STAT_DIR_N, "{}.txt".format(file_names[i]))) as reader:
        string_array_n = reader.read()
        actual_array_n = np.fromstring(string_array_n, dtype = float, sep=",")

    with open(os.path.join(STAT_DIR_3SAT, "{}.txt".format(file_names[i]))) as reader:
        string_array_3sat = reader.read()
        actual_array_3sat = np.fromstring(string_array_3sat, dtype = float, sep=",")

    with open(os.path.join(STAT_DIR_BE, "{}.txt".format(file_names[i]))) as reader:
        string_array_be = reader.read()
        actual_array_be = np.fromstring(string_array_be, dtype=float, sep=",")



    plt.subplot(3,3, i+1)
    min_graph = min(min(actual_array_3sat), min(actual_array_n), min(actual_array_be))
    max_graph = max(max(actual_array_3sat), max(actual_array_n), max(actual_array_be))
    bins = np.linspace(min_graph, max_graph, 30)
    plt.hist(actual_array_n, bins, color = 'y', alpha=0.3, label = 'naive')
    plt.hist(actual_array_3sat, bins, color = 'g', alpha=0.3, label = '3sat')
    plt.hist(actual_array_be, bins, color='g', alpha=0.3, label='optimised')

    plt.title(file_names[i])
    plt.legend()



plt.show()

print

