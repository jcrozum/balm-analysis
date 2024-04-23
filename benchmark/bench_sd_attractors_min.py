from biodivine_aeon import BooleanNetwork
from biobalm import SuccessionDiagram
import sys
import os
import pickle

NODE_LIMIT = 1_000_000
DEPTH_LIMIT = 10_000

bn = BooleanNetwork.from_file(sys.argv[1])
bn = bn.infer_valid_graph()

# Load the precomputed succession diagram. If the file does not
# exist, this will fail, which is fine.
with open(f"{sys.argv[1]}.sd.min.pickle", "rb") as handle:
    sd = pickle.load(handle)

print(f"Succession diagram size:", len(sd))
print(f"Minimal traps:", len(sd.minimal_trap_spaces()))

attractor_count = 0
motif_avoidant_count = 0

for node in sd.node_ids():
    if not sd.node_is_minimal(node):
        continue
    attr = sd.node_attractor_seeds(node, compute=True)
    attractor_count += len(attr)
    if not sd.node_is_minimal(node):
        motif_avoidant_count += len(attr)

print("nodes, minimal-traps, attractors, motif-avoidant")
print(
    f"{len(sd)}, {len(sd.minimal_trap_spaces())}, {attractor_count}, {motif_avoidant_count}"
)
