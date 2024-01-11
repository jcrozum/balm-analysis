from biodivine_aeon import BooleanNetwork
from nfvsmotifs.SuccessionDiagram import SuccessionDiagram
import sys
import nfvsmotifs

# Print progress and succession diagram size.
nfvsmotifs.SuccessionDiagram.DEBUG = True

NODE_LIMIT = 1_000_000

# This is unfortunately necessary for PyEDA Boolean expression parser (for now).
sys.setrecursionlimit(150000)

bn = BooleanNetwork.from_file(sys.argv[1])
bn = bn.infer_regulatory_graph()

# Compute the succession diagram.
sd = SuccessionDiagram(bn)
fully_expanded = sd.expand_attractor_seeds(size_limit=NODE_LIMIT)
assert fully_expanded

attractor_count = 0
motif_avoidant_count = 0

for node in sd.expanded_ids():
    attr = sd.node_attractor_seeds(node, compute=True)
    attractor_count += len(attr)
    if not sd.node_is_minimal(node):
        motif_avoidant_count += len(attr)

print("nodes, expanded, attractors, motif-avoidant")
print(f"{len(sd)}, {len(list(sd.expanded_ids()))}, {attractor_count}, {motif_avoidant_count}")