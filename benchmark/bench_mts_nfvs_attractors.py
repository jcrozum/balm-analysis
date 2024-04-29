import biodivine_aeon as ba
import sys
from pathlib import Path
import subprocess

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

# Fix header and output network.
Path("./mtsNFVS/python/networks/test.bnet").write_text(bn.to_bnet().replace("targets,", "targets, "))

p = subprocess.Popen(["python3", "test.py", "test.bnet"], cwd="./mtsNFVS/python")
p.wait()
