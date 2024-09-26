from biodivine_aeon import BooleanNetwork
from biobalm import SuccessionDiagram
import sys
import os
import pickle

NODE_LIMIT = 1_000_000
DEPTH_LIMIT = 10_000

bn = BooleanNetwork.from_file(sys.argv[1])
bn = bn.infer_valid_graph()
bn = bn.inline_constants(infer_constants=True, repair_graph=True)
print(f"Simplified network: {bn}")

# Prepare a config which will print progress.
config = SuccessionDiagram.default_config()
config["debug"] = True
config["max_motifs_per_node"] = 1_000_000
config["attractor_candidates_limit"] = 100_000

# Compute the succession diagram.
sd = SuccessionDiagram(bn, config)
fully_expanded = sd.expand_bfs(bfs_level_limit=DEPTH_LIMIT, size_limit=NODE_LIMIT)
assert fully_expanded

print(f"Succession diagram size:", len(sd))
print(f"Minimal traps:", len(sd.minimal_trap_spaces()))

print("size, expanded, minimal")
print(f"{len(sd)},{len(list(sd.expanded_ids()))},{len(sd.minimal_trap_spaces())}")
