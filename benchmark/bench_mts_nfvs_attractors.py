import biodivine_aeon as ba
import sys
import os
from pathlib import Path
import subprocess

ba.LOG_LEVEL = ba.LOG_ESSENTIAL

# This is a very basic script for running attractor detection using mts-nfvs.
#
# The script only takes one argument: a path to the network file.

bn = ba.BooleanNetwork.from_file(sys.argv[1])
bn = bn.infer_valid_graph()


bn = bn.inline_constants(infer_constants=True, repair_graph=True)
if bn.variable_count() == 0:
    # We can't give an empty network to mts-nfvs.
    print("Network solved through constant propagation.")
    sys.exit(0)

# Fix header and output network.
Path("./mtsNFVS/python/networks/test.bnet").write_text(bn.to_bnet().replace("targets,", "targets, "))

# Figure out the path where the script currently is, and add mtsNFVS/python to LD_LIBRARY_PATH.
# This allows us to link agains the libz3java library that is required by mtsNFVS.
my_path = os.path.dirname(os.path.realpath(__file__))
my_env = os.environ.copy()
my_env["LD_LIBRARY_PATH"] = f"{my_path}/mtsNFVS/python"

# Use the current python interpreter executable to preserve venv and other configuration.
p = subprocess.Popen([sys.executable, "test.py", "test.bnet"], cwd="./mtsNFVS/python", env=my_env)
p.wait()
