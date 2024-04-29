import biodivine_aeon as ba
import sys

ba.LOG_LEVEL = ba.LOG_ESSENTIAL

# This is a very basic script for running attractor detection usin AEON.
# The results should be comparable to `bench_attractor_search`.
#
# The script only takes one argument: a path to the network file.

bn = ba.BooleanNetwork.from_file(sys.argv[1])
bn = bn.infer_valid_graph()

print(f"Loaded network: {bn}")

bn = bn.inline_constants(infer_constants=True, repair_graph=True)

print(f"Simplified network: {bn}")

stg = ba.AsynchronousGraph(bn)

attr = ba.Attractors.attractors(stg)

print("Attractors:", len(attr))

attr_states = stg.mk_empty_colored_vertices()

for a in attr:
    attr_states = attr_states.union(a)

print("attractors, attractor-states")
print(f"{len(attr)}, {attr_states.cardinality()}")