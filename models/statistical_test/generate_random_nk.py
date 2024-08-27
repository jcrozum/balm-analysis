import os
import csv

import pystablemotifs.random_boolean_networks as rbn

file = open("bbm_list.csv", "r")
csv_file = csv.reader(file)

PER_MODEL = 100
# K = 3  # in-degree
# p = 0.211325 # ratio of 1 in the truth table
# DIRECTORY = "random_nk3"

K = 2  # in-degree
p = 0.5 # ratio of 1 in the truth table
DIRECTORY = "random_nk2"

next(csv_file)
for line in csv_file:
    seed = int(line[0])
    n_nodes = int(line[2]) + int(line[3])

    rules_list = rbn.random_boolean_network_ensemble_kauffman(n_nodes,K,p,PER_MODEL,seed=seed)

    for i in range(PER_MODEL):

        rules = rules_list[i]
        
        rules = rules.replace(" *=", ",")
        rules = rules.replace(" and ", " & ")
        rules = rules.replace(" or ", " | ")
        rules = rules.replace("not ", "!")
        rules = rules.replace(", 1", ", true")
        rules = rules.replace(", 0", ", false")

        writePath = DIRECTORY + f"/{line[0]}_{i:03d}.bnet"
        isExist = os.path.exists(DIRECTORY)
        if not isExist:
            os.makedirs(DIRECTORY)

        with open(writePath, "w") as f:
            f.write("targets, factors\n")
            f.write(rules)
    
    # break