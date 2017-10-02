import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


#define general variables
START, END = 4000, 4500
PUZZLE_SIZE = 3
puzzle_size = PUZZLE_SIZE**2
STAT_DIR_N = "./stat/"+str(PUZZLE_SIZE)+"/"+str(PUZZLE_SIZE)+"/"
STAT_DIR_3SAT = "./stat/"+str(PUZZLE_SIZE)+"/"+str(PUZZLE_SIZE)+"_3SAT/"
STAT_DIR_L = "./stat/"+str(PUZZLE_SIZE)+"/"+str(PUZZLE_SIZE)+"_L/"

# observed statistics
file_names = ["final_conflicts", "final_cpu_time",     "final_decisions", "final_memory"]
# file_names = ["final_restarts", ""final_conflicts", "final_cpu_time", "final_decisions", "final_memory", "final_propagation","final_propagation_cpu",
            #  "final_decisions_cpu", "final_conflicts_literals", "final_conflicts_cpu"]

plot_names = ["Number of conflicts", "CPU time (s)", "Number of decisions", "Memory usage (MB)"]

# import stat from txt
for i in range(len(file_names)):
    # naive
    with open(os.path.join(STAT_DIR_N, "{}.txt".format(file_names[i]))) as reader:
        string_array_n = reader.read()
        actual_array_n = np.fromstring(string_array_n, dtype = float, sep=",")
    # 3sat
    with open(os.path.join(STAT_DIR_3SAT, "{}.txt".format(file_names[i]))) as reader:
        string_array_3sat = reader.read()
        actual_array_3sat = np.fromstring(string_array_3sat, dtype = float, sep=",")
    # layered
    with open(os.path.join(STAT_DIR_L, "{}.txt".format(file_names[i]))) as reader:
        string_array_l = reader.read()
        actual_array_l = np.fromstring(string_array_l, dtype=float, sep=",")



    # some  stat
    stat_n = pd.Series(actual_array_n.tolist())
    d_n = pd.DataFrame.describe(stat_n)
    d_n.to_csv(os.path.join(STAT_DIR_N,'{}_stat.txt'.format(file_names[i])))

    stat_3sat = pd.Series(actual_array_3sat.tolist())
    d_3sat = pd.DataFrame.describe(stat_3sat)
    d_3sat.to_csv(os.path.join(STAT_DIR_3SAT, '{}_stat.txt'.format(file_names[i])))

    stat_l = pd.Series(actual_array_l.tolist())
    d_l = pd.DataFrame.describe(stat_l)
    d_l.to_csv(os.path.join(STAT_DIR_L, '{}_stat.txt'.format(file_names[i])))


    # plot histograms
    plt.subplot(2,2, i+1)
    min_graph = min(min(actual_array_3sat), min(actual_array_n), min(actual_array_l))
    max_graph = max(max(actual_array_3sat), max(actual_array_n), max(actual_array_l))
    bins = np.linspace(min_graph, max_graph, 40)
    plt.hist(actual_array_n, bins, color = 'y', alpha=0.3, label = 'naive')
    plt.hist(actual_array_3sat, bins, color = 'm', alpha=0.3, label = '3sat')
    plt.hist(actual_array_l, bins, color='c', alpha=0.3, label='layered')
    if i == 0 or i == 2:
        plt.yscale('log')

    plt.xlabel(plot_names[i])
    plt.ylabel("number of sudoku")
    plt.legend()



plt.show()



