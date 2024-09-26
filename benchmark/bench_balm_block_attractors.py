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
fully_expanded = sd.expand_block(
    find_motif_avoidant_attractors=True,
    exact_attractor_detection=True,
    size_limit=1_000,
)

skipped = 0
if not fully_expanded:
    skipped = sd.skip_remaining()

print(f"Succession diagram size:", len(sd))
print(f"Minimal traps:", len(sd.minimal_trap_spaces()))
print(f"Skip nodes: {skipped}")

attractor_count = 0
motif_avoidant_count = 0

# The order of iteration is important, because it ensures we start
# from minimal (or rather last expanded) nodes, i.e. the info from these
# can be reused in the other methods.
for node in reversed(list(sd.expanded_ids())):
    attr = sd.node_attractor_seeds(node, compute=True, symbolic_fallback=True)
    attractor_count += len(attr)
    if not sd.node_is_minimal(node):
        motif_avoidant_count += len(attr)

print("nodes, expanded, minimal-traps, attractors, motif-avoidant")
print(
    f"{len(sd)}, {len(list(sd.expanded_ids()))}, {len(sd.minimal_trap_spaces())}, {attractor_count}, {motif_avoidant_count}"
)
