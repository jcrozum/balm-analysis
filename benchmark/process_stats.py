import os
import csv

# Load data for all three tools from the results folder

aeon_data = {
	"bbm": {},
	"nk2": {},
	"nk3": {},
	"ncf": {},
	"dense": {},
}

mts_data = {
	"bbm": {},
	"nk2": {},
	"nk3": {},
	"ncf": {},
	"dense": {},
}

balm_block_data = {
	"bbm": {},
	"nk2": {},
	"nk3": {},
	"ncf": {},
	"dense": {},
}

balm_expand_data = {
	"bbm": {},
	"nk2": {},
	"nk3": {},
	"ncf": {},
	"dense": {},
}

balm_attr_data = {
	"bbm": {},
	"nk2": {},
	"nk3": {},
	"ncf": {},
	"dense": {},
}

all_models = {
	"bbm": set(),
	"nk2": set(),
	"nk3": set(),
	"ncf": set(),
	"dense": set(),
}

def find_in_folder(folder, find, is_dir=False, all=False):
	results = [ f for f in os.listdir(folder) if find in f ]
	if is_dir:
		results = [ f for f in results if os.path.isdir(f) ]
	if not all:
		assert len(results) == 1
		return results[0]
	else:
		return results

def read_row(tool, row):
	if tool == "aeon":
		try:
			assert len(row) == 4
			return (row[0], float(row[1]), int(row[2]))
		except:
			return None
	if tool == "nfvs":		
		try:
			assert len(row) == 3
			row[2] = row[2].strip()			
			if row[2] == "Network solved through constant propagation.":
				return (row[0], float(row[1]), 1)
			else:
				assert row[2].startswith("Number of attractors:")
				return (row[0], float(row[1]), int(row[2].replace("Number of attractors:", "")))
		except:
			return None
	if tool == "balm-block":
		try:			
			assert len(row) == 7
			return (row[0], float(row[1]), int(row[-2]))
		except:
			return None
	if tool == "balm-expand":
		try:
			assert len(row) == 5
			return (row[0], float(row[1]), int(row[2]))
		except:
			return None
	if tool == "balm-attractors":
		try:
			assert len(row) == 6
			return (row[0], float(row[1]), int(row[-2]))
		except:
			return None
	return None

# Load data from csv files

for folder in os.listdir('./results-raw'):
	if not os.path.isdir(f"./results-raw/{folder}"):
		# Folders in results-raw contain experimental datasets.
		continue
	print("Processing", folder)
	for experiment in os.listdir(f"./results-raw/{folder}"):
		if not os.path.isdir(f"./results-raw/{folder}/{experiment}") or not experiment.startswith("_run_"):
			# Experiments are folders that start with _run_
			continue
		# Stats file name contains all identifying information, including tool, experiment type and model type
		stats_file = find_in_folder(f"./results-raw/{folder}/{experiment}", "_times.csv")
		
		tool = None
		if "aeon" in stats_file:
			data = aeon_data
			tool = "aeon"
		elif "nfvs" in stats_file:
			data = mts_data
			tool = "nfvs"
		elif "balm" in stats_file and "block" in stats_file:
			data = balm_block_data
			tool = "balm-block"
		elif "balm" in stats_file and "full_expand" in stats_file:
			data = balm_expand_data
			tool = "balm-expand"
		elif "balm" in stats_file and "full_attractors" in stats_file:
			data = balm_attr_data
			tool = "balm-attractors"
		else:
			raise RuntimeError("Unknown tool configuration", stats_file)

		model_type = None
		for type in ["bbm", "nk2", "nk3", "ncf", "dense"]:
			if type in stats_file:
				model_type = type
		if model_type is None:
			raise RuntimeError("Unknown model type", stats_file)

		print("Loading...", stats_file)

		with open(f"./results-raw/{folder}/{experiment}/{stats_file}") as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			next(reader) # Skip header
			total = 0
			for row in reader:
				row_data = read_row(tool, row)
				if row_data is not None:
					(model, time, attr) = row_data
					model = f"{model_type}-{model}"
					data[model_type][model] = (time, attr)
					total += 1
					all_models[model_type].add(model)
				else:
					model = f"{model_type}-{row[0]}"
					all_models[model_type].add(model)					
			print("Successful models:", total)

# Check that the data is ok

print("Model counts:")
for model_type in all_models:
	print(model_type, len(all_models[model_type]))

errors = 0
for model_type in ["bbm", "nk2", "nk3", "ncf", "dense"]:
	for model in all_models[model_type]:
		if model in balm_block_data[model_type]:
			if model in aeon_data[model_type]:
				if aeon_data[model_type][model][1] != balm_block_data[model_type][model][1]:
					print(f"Found AEON error in {model}. Removed.")
					del aeon_data[model_type][model]
					errors += 1
			if model in mts_data[model_type]:
				if mts_data[model_type][model][1] != balm_block_data[model_type][model][1]:
					print(f"Found NFVS error in {model}. Removed.")
					del mts_data[model_type][model]
					errors += 1
			if model in balm_attr_data[model_type]:
				if balm_attr_data[model_type][model][1] != balm_block_data[model_type][model][1]:
					print(f"Found BALM error in {model}. Removed.")
					del balm_block_data[model_type][model][1]
					errors += 1

print("Measurements removed due to mismatch errors:", errors)

for model_type in ["bbm", "nk2", "nk3", "ncf", "dense"]:
	with open(f'results-{model_type}.tsv', 'w') as csvfile:
		writer = csv.writer(csvfile, delimiter='\t')
		# Header
		writer.writerow([
			'model',
			'aeon [time]',
			'mts-nfvs [time]',
			'balm-block [time]',
			'balm-full-expand [time]',
			'balm-full-attractors [time]',
			'balm-full-total [time]',
			'attractors',
			'full-sd-size',
		])
		for model in sorted(all_models[model_type]):
			row = [ None for _ in range(9) ]
			row[0] = model
			attractors = None
			full_sd_size = None
			if model in aeon_data[model_type]:
				row[1] = '{0:.2f}'.format(aeon_data[model_type][model][0])
				if attractors is None:
					attractors = aeon_data[model_type][model][1]
			if model in mts_data[model_type]:
				row[2] = '{0:.2f}'.format(mts_data[model_type][model][0])
				if attractors is None:
					attractors = mts_data[model_type][model][1]
			if model in balm_block_data[model_type]:
				row[3] = '{0:.2f}'.format(balm_block_data[model_type][model][0])
				if attractors is None:
					attractors = balm_block_data[model_type][model][1]
			if model in balm_expand_data[model_type]:
				row[4] = '{0:.2f}'.format(balm_expand_data[model_type][model][0])
				full_sd_size = balm_expand_data[model_type][model][1]
			if model in balm_attr_data[model_type]:
				row[5] = '{0:.2f}'.format(balm_attr_data[model_type][model][0])
				row[6] = '{0:.2f}'.format(balm_attr_data[model_type][model][0] + balm_expand_data[model_type][model][0])
			row[7] = attractors
			row[8] = full_sd_size
			writer.writerow(row)
