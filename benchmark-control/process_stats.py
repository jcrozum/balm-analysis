import os
import csv

# Load data for all three tools from the results folder

pystablemotifs_data = {
	"bbm": {},
}

balm_data = {
	"bbm": {},
}

all_models = {
	"bbm": set(),
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
	if tool == "balm":
		try:			
			assert len(row) == 3
			return (row[0], float(row[1]), int(row[-1]))
		except:
			return None
	if tool == "pystablemotifs":
		try:
			assert len(row) == 3
			return (row[0], float(row[1]), int(row[-1]))
		except:
			return None
	return None

# Load data from csv files

for folder in os.listdir('./results-raw'):
	if not os.path.isdir(f"./results-raw/{folder}"):
		# Folders in results-raw contain experimental datasets.
		continue
	print(" >> Processing", folder)
	for experiment in os.listdir(f"./results-raw/{folder}"):
		if not os.path.isdir(f"./results-raw/{folder}/{experiment}") or not experiment.startswith("_run_"):
			# Experiments are folders that start with _run_
			continue
		# Stats file name contains all identifying information, including tool, experiment type and model type
		stats_file = find_in_folder(f"./results-raw/{folder}/{experiment}", "_times.csv")
		
		tool = None
		if "pystablemotifs" in stats_file:
			data = pystablemotifs_data
			tool = "pystablemotifs"
		elif "balm" in stats_file:
			data = balm_data
			tool = "balm"
		else:
			raise RuntimeError("Unknown tool configuration", stats_file)

		model_type = None
		for type in ["bbm"]:
			if type in stats_file:
				model_type = type
		if model_type is None:
			raise RuntimeError("Unknown model type", stats_file)

		print("Loading...", stats_file)

		with open(f"./results-raw/{folder}/{experiment}/{stats_file}") as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			next(reader) # Skip header
			success = 0
			total = 0
			for row in reader:
				total += 1
				row_data = read_row(tool, row)
				if row_data is not None:
					success += 1
					(model, time, attr) = row_data
					model = f"{model_type}-{model}"
					# Ensure that we are not inserting duplicate data.
					assert model not in data[model_type]
					data[model_type][model] = (time, attr)					
					all_models[model_type].add(model)
				else:
					model = f"{model_type}-{row[0]}"
					all_models[model_type].add(model)					
			print(f"Successful models: {success}/{total}")

# Check that the data is ok

print("Model counts:")
for model_type in all_models:
	print(model_type, len(all_models[model_type]))

for model_type in ["bbm"]:
	with open(f'results-{model_type}.tsv', 'w') as csvfile:
		writer = csv.writer(csvfile, delimiter='\t')
		# Header
		writer.writerow([
			'model',
			'pystablemotifs [time]',
			'balm [time]',
			'minimal traps',
		])
		for model in sorted(all_models[model_type]):
			row = [ None for _ in range(4) ]
			row[0] = model
			if model in pystablemotifs_data[model_type]:
				row[1] = '{0:.2f}'.format(pystablemotifs_data[model_type][model][0])
			if model in balm_data[model_type]:
				row[2] = '{0:.2f}'.format(balm_data[model_type][model][0])
				row[3] = str(balm_data[model_type][model][1])
			writer.writerow(row)
	print(f"Data written to results-{model_type}.tsv")