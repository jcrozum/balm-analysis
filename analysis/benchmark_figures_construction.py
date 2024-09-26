import matplotlib.pyplot as plt
import matplotlib.gridspec as grid_spec
import matplotlib.patches as patches
from matplotlib.colors import CenteredNorm
import pandas as pd
import numpy as np
from benchmark_figures_utils import load_combined_data
from benchmark_figures_cumulative import simple_cumulative_figure
from benchmark_figures_scatter import simple_scatter_figure

result_files = {
    "bbm": "../benchmark-construction/results-bbm.tsv",
}

colors = {
    "pystablemotifs": "#BB5566",
    "biobalm": "#66aadd",
}

results = load_combined_data(result_files)
print(results.head())

# Maps the tool name to the name of the column in the result data.
tool_columns = {
    "pystablemotifs": "pystablemotifs [time]",
    "biobalm": "balm [time]",
}


simple_cumulative_figure(
    results, 
    tool_columns, 
    colors, 
    './figures/construction_cumulative.pdf', 
    'Completed SD construction benchmarks'
)
simple_scatter_figure(
    results, 
    "pystablemotifs",
    tool_columns["pystablemotifs"],
    "biobalm",
    tool_columns["biobalm"],
    f"./figures/construction_scatter.pdf",
    f"Biobalm vs. pystablemotifs; SD construction"
)