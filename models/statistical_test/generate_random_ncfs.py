import os
import csv

import sys

sys.path.append("../..")

from rbn_generators import power_law_graph_generator
from rbn_generators import add_negative_edges
from rbn_generators import generate_ncf_rule

file = open("bbm_list.csv", "r")
csv_file = csv.reader(file)

PER_MODEL = 100
# POWER = 1.95  # power for the out-degree, diverges at 1.0
power_dict = {
    10:1.05,
    20:1.60,
    40:1.85,
    80:2.00,
    160:2.10,
    320:2.15,
    640:2.20,
              }

P_NEG = 0.24  # ratio of negative edges
SINK = 0.1 # ratio of sink nodes
DIRECTORY = "random_ncf"

next(csv_file)
seed = 0
for line in csv_file:
    n_nodes = int(line[2]) + int(line[3])

    for key in power_dict.keys():
        if n_nodes < key:
            power = power_dict[key]
            break

    for i in range(PER_MODEL):
        seed += 1
        G = power_law_graph_generator(n_nodes, power, sink=SINK, seed=seed)

        add_negative_edges(G, P_NEG, seed=i)

        rules = ""
        for node in G.nodes():
            rules += generate_ncf_rule(G, node, bias=0.5, seed=seed) + "\n"
        writePath = DIRECTORY + f"/{line[0]}_{i:03d}.bnet"
        isExist = os.path.exists(DIRECTORY)
        if not isExist:
            os.makedirs(DIRECTORY)

        with open(writePath, "w") as f:
            f.write("targets, factors\n")
            f.write(rules)
