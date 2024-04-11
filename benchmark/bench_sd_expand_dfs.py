from biodivine_aeon import BooleanNetwork
from balm import SuccessionDiagram
import sys
import os
import pickle
import balm.succession_diagram

# Print progress and succession diagram size.
balm.succession_diagram.DEBUG = True

NODE_LIMIT = 1_000_000
STACK_LIMIT = 10_000

bn = BooleanNetwork.from_file(sys.argv[1])
bn = bn.infer_valid_graph()

# Compute the succession diagram.
sd = SuccessionDiagram(bn)
fully_expanded = sd.expand_dfs(dfs_stack_limit=STACK_LIMIT, size_limit=NODE_LIMIT)
assert fully_expanded

#sd.reclaim_node_data()
with open(f"{sys.argv[1]}.sd.pickle", "wb") as handle:
    pickle.dump(sd, handle)

print(f"Succession diagram size:", len(sd))
print(f"Minimal traps:", len(sd.minimal_trap_spaces()))

print("size, expanded, minimal")
print(f"{len(sd)},{len(list(sd.expanded_ids()))},{len(sd.minimal_trap_spaces())}")
