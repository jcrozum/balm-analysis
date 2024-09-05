import matplotlib.pyplot as plt
import matplotlib.gridspec as grid_spec
import matplotlib.patches as patches
from matplotlib.colors import CenteredNorm
import pandas as pd
import numpy as np
from benchmark_figures_utils import load_combined_data

result_files = {
    "bbm": "../benchmark/results-bbm.tsv",
    "dense": "../benchmark/results-dense.tsv",
    "nk2": "../benchmark/results-nk2.tsv",
    "nk3": "../benchmark/results-nk3.tsv",
    "ncf": "../benchmark/results-ncf.tsv"
}

colors = {
    "mtsNFVS": "#DDAA33",
    "AEON.py": "#BB5566",
    "biobalm[block]": "#66aadd",
    "biobalm[full]": "#004488",
}

results = load_combined_data(result_files)
print(results.head())

# Maps the tool name to the name of the column in the result data.
tool_columns = {
    "AEON.py": "aeon [time]",
    "mtsNFVS": "mts-nfvs [time]",
    "biobalm[full]": "balm-full-total [time]",
    "biobalm[block]": "balm-block [time]",
}

fontsize=14

gs = (grid_spec.GridSpec(30,60))

fig = plt.figure(figsize=(8,4))
fig.set_facecolor("white")

ax_zoomed = fig.add_subplot(gs[:,:])
mini_offset=(19,39)
mini_size=(10,20)
ax_full = fig.add_subplot(gs[mini_offset[0]:(mini_offset[0] + mini_size[0]),mini_offset[1]:(mini_offset[1] + mini_size[1])])

# Add a "fake" label that looks like a "title" for the legend and is
# aligned with tool names.
ax_zoomed.scatter(-1,-1,label="Failed benchmarks",alpha=0.0)

# Draw all data in both plots:

total_benchmarks = len(results)
for i, (tool, column) in enumerate(tool_columns.items()):
	data = results[column].sort_values()
	successes = sum(data < float("inf"))
	attempts = len(data)
	ax_zoomed.hlines(
		y=successes,
		xmin=0,
		xmax=3600,
		color=colors[tool],
		linestyle=(i * 3, (5,5)),
	)
	ax_zoomed.step(
		data, 
		np.arange(len(data)), 
		color=colors[tool],
		label=f'{tool}:{attempts-successes}',		
	)
	ax_full.step(
		data, 
		np.arange(len(data)), 
		color=colors[tool],	
	)

zoom_xbounds = (1, 3600)
zoom_ybounds = (13400, total_benchmarks)

zoom_rect = patches.Rectangle(
	xy=(zoom_xbounds[0], zoom_ybounds[0]),
	width=zoom_xbounds[1] - zoom_xbounds[0],
	height=zoom_ybounds[1] - zoom_ybounds[0],
	edgecolor='#000000',
	facecolor='#ffffff',
	linestyle='--'
)

full_rect = patches.Rectangle(
	xy=(0,0),
	width=3600,
	height=total_benchmarks,
	color="#000000",
	alpha=0.1,
)

ax_full.add_patch(full_rect)
ax_full.add_patch(zoom_rect)

ax_zoomed.set_xscale("log")
ax_zoomed.set_xlabel("Runtime (log)", fontsize=fontsize)
ax_zoomed.set_ylabel("Completed benchmarks", fontsize=fontsize)
ax_zoomed.set_xlim((1, 3600))
ax_zoomed.set_ylim((13400, total_benchmarks))
ax_zoomed.set_yticks([13250,13750,14250,14750,15250,15750,16250,total_benchmarks])
ax_zoomed.set_xticks([1,10,60,300,3600])
ax_zoomed.set_xticklabels(["1s","10s","1min","5min","1h"], fontsize=fontsize)

ax_full.set_xscale("log")
ax_full.set_xticks([])
ax_full.set_yticks([])
ax_full.set_xlim((0.01, 3600))
ax_full.set_ylim((0, total_benchmarks))

ax_zoomed.legend(prop={'family': 'monospace'}, loc=(0.657,0.38))

fig.savefig('./figures/completed_full_with_zoom.pdf', bbox_inches="tight")

def simple_cumulative_figure(
	results,
	tool_columns,
	tool_colors,
	file_name,
	title,
):
	"""
	Build a cumulative figure without all the bells and whistles of the "main" figure,
	i.e. just the figure with automated bounds and styling, no "zoom", etc.
	"""

	fig, ax = plt.subplots(1, 1, figsize=(8, 4))
	fig.set_facecolor("white")

	ax.scatter(-1,-1,label="Failed benchmarks",alpha=0.0)

	total_benchmarks = len(results)
	for i, (tool, column) in enumerate(tool_columns.items()):
		data = results[column].sort_values()
		successes = sum(data < float("inf"))
		attempts = len(data)
		ax.hlines(
			y=successes,
			xmin=0,
			xmax=3600,
			color=colors[tool],
			linestyle=(i * 3, (5,5)),
		)
		ax.step(
			data, 
			np.arange(len(data)), 
			color=colors[tool],
			label=f'{tool}:{attempts-successes}',		
		)

	ax.set_xscale("log")
	ax.set_xlabel("Runtime (log)")
	ax.set_ylabel("Completed benchmark models")
	ax.set_xticks([1,10,60,300,3600])
	ax.set_xticklabels(["1s","10s","1min","5min","1h"])

	ax.legend(prop={'family': 'monospace'})

	plt.title(title)
	fig.savefig(file_name, bbox_inches="tight")

simple_cumulative_figure(results, tool_columns, colors, './figures/completed_full.pdf', 'Completed benchmarks (all ensembles)')
simple_cumulative_figure(results.loc[results['Benchmark Type'] == 'bbm'], tool_columns, colors, './figures/completed_ensemble_bbm.pdf', 'BBM; randomized constant inputs')
simple_cumulative_figure(results.loc[results['Benchmark Type'] == 'nk2'], tool_columns, colors, './figures/completed_ensemble_nk2.pdf', 'Random critical N-K; K=2')
simple_cumulative_figure(results.loc[results['Benchmark Type'] == 'nk3'], tool_columns, colors, './figures/completed_ensemble_nk3.pdf', 'Random critical N-K; K=3')
simple_cumulative_figure(results.loc[results['Benchmark Type'] == 'ncf'], tool_columns, colors, './figures/completed_ensemble_ncf.pdf', 'Random nested canalyzing')
simple_cumulative_figure(results.loc[results['Benchmark Type'] == 'dense'], tool_columns, colors, './figures/completed_ensemble_dense.pdf', 'Random dense')
