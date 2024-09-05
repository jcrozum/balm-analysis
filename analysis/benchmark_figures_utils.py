import pandas as pd

def load_combined_data(result_files):
    combined = None
    for (model_type, file_name) in result_files.items():
        table = pd.read_csv(file_name, sep='\t', header=0)
        table.fillna(float("inf"), inplace=True)
        table.insert(0, "Benchmark Type", model_type)
        print(f"Loaded {len(table)} models in category {model_type}")
        if combined is None:
            combined = table
        else:
            combined = pd.concat([combined, table])
    return combined