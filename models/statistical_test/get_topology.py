from biodivine_aeon import BooleanNetwork

import os

# directory = "bbm-bnet-inputs-true"
# log_loc = "bbm_topology.csv"

directory = "random_ncf"
log_loc = "ncf_topology.csv"

# directory = "random_nk2"
# log_loc = "nk2_topology.csv"

# directory = "random_nk3"
# log_loc = "nk3_topology.csv"


for filename in os.listdir(directory):
    model_no = filename.split(".")[0]
    print(model_no)
    
    if model_no == "079":
        continue
    if not filename.endswith(".bnet"):
        continue

    f = os.path.join(directory, filename)

    # bn = BooleanNetwork.from_file("balm-analysis/models/statistical_test/random_nk3/001_000.bnet")
    # bn = BooleanNetwork.from_file("balm-analysis/models/bbm-bnet-inputs-true/001.bnet")
    bn = BooleanNetwork.from_file(f)

    # bn = bn.infer_regulatory_graph()

    nodes = bn.num_vars()
    constants = 0
    sources = 0
    total_in_degree = 0

    constants_list = []
    sources_list = []

    for variable in bn.variables():
        name = bn.get_variable_name(variable)
        
        # print(f"{name=}")

        regulators = bn.regulators(variable)

        in_degree = len(regulators)

        total_in_degree += in_degree

        if in_degree == 0:
            constants += 1
            constants_list.append(name)

        elif in_degree == 1:
            if name == bn.get_variable_name(regulators.pop()):
                sources += 1
                sources_list.append(name)

    # print(f"{nodes}")
    # print(f"{constants=}")
    # print(f"{sources=}")
    # print(f"{total_in_degree=}")

    print(f"{nodes},{constants},{sources},{total_in_degree}")
    log = open(log_loc, "a")

    log.write(f"{model_no},{nodes},{constants},{sources},{total_in_degree}\n")
    log.close()

