from biodivine_aeon import BooleanNetwork
from biobalm import SuccessionDiagram
import sys
import os
import pickle

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
fully_expanded = sd.expand_block(find_motif_avoidant_attractors=True)
assert fully_expanded

print(f"Succession diagram size:", len(sd))
print(f"Minimal traps:", len(sd.minimal_trap_spaces()))

attractor_count = 0
motif_avoidant_count = 0

for node in sd.expanded_ids():
    attr = sd.node_attractor_seeds(node, compute=True)
    attractor_count += len(attr)
    if not sd.node_is_minimal(node):
        motif_avoidant_count += len(attr)

print("nodes, expanded, minimal-traps, attractors, motif-avoidant")
print(
    f"{len(sd)}, {len(list(sd.expanded_ids()))}, {len(sd.minimal_trap_spaces())}, {attractor_count}, {motif_avoidant_count}"
)
