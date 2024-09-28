from biodivine_aeon import BooleanNetwork
from biobalm import SuccessionDiagram
from biobalm.control import succession_control
from biobalm.space_utils import is_subspace
from pathlib import Path
import sys
import os
import pickle
import functools

NODE_LIMIT = 1_000_000
DEPTH_LIMIT = 10_000

bn = BooleanNetwork.from_file(sys.argv[1])
bn = bn.infer_valid_graph()
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

# Select target space
min_trap = sd.minimal_trap_spaces()[0]
target = sd.node_data(min_trap)["space"]

# Print target space so that we can reuse it in pystablemotifs.
Path(sys.argv[1].replace(".bnet", ".target.txt")).write_text(repr(target))

# Do the control in biobalm
interventions_nfvsmotifs = succession_control(sd, target, skip_feedforward_successions=True)
interventions = []
for x in interventions_nfvsmotifs:
	print(x)
	for control_sequence in x.all_control_strategies():
		if len(control_sequence) == 0:
			# Empty intervention... works always.
			interventions.append("[]")
			continue

		# Merge sequence into one control intervention.
		control = functools.reduce(lambda x, y: x | y, control_sequence)
		skip_completely = False
		for i in reversed(range(len(interventions))):
			existing_control = interventions[i]
			if is_subspace(control, existing_control):
				skip_completely = True
				break
			if is_subspace(existing_control, control):
				del interventions[i]
		if skip_completely:
			continue
		interventions.append(control)

for control in interventions:
	print(control)

print(len(interventions))
