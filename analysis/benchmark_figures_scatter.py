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

markers = {
    "AEON.py": "o",
    "mtsNFVS": "X",
}

marker_symbols = {
    "AEON.py": "●︎",
    "mtsNFVS": "✖",
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

stretch_factor = 11
fontsize = 14
marker_size = 25
marker_alpha = 0.85
grid_alpha = 0.25

fig = plt.figure(figsize=(8,8))
fig.set_facecolor("white")


afig = fig.subfigures(1, 1)
axd = afig.subplot_mosaic(
        [
            ["BalmTimeout", "BothTimeout"],
            ["BothFinished", "ToolTimeout"],
        ],
        gridspec_kw={
            "width_ratios": [stretch_factor, 1],
            "height_ratios": [1, stretch_factor],
        },
    )

# Add colored backgrounds.

bad_area = patches.Polygon(
    xy=[(0.001,1), (0.1,1), (360,3600), (0.001,3600)],
    closed=True,
    facecolor='#ff0000',
    alpha=0.05
)

good_area = patches.Polygon(
    xy=[(1,0.001), (1,0.1), (3600,360), (3600,0.001)],
    closed=True,
    facecolor='#00ff00',
    alpha=0.05
)

meh_area = patches.Polygon(
    xy=[(0.001,0.01), (0.001,1), (0.1,1), (360,3600), (3600,3600), (3600,360), (1,0.1), (1,0.001), (0.001,0.001)],
    closed=True,
    facecolor='#000000',
    alpha=0.05
)

axd["BothFinished"].add_patch(bad_area)
axd["BothFinished"].add_patch(good_area)
axd["BothFinished"].add_patch(meh_area)
axd["BalmTimeout"].patch.set_facecolor("#ff0000")
axd["BalmTimeout"].patch.set_alpha(0.05)
axd["ToolTimeout"].patch.set_facecolor("#00ff00")
axd["ToolTimeout"].patch.set_alpha(0.05)
axd["BothTimeout"].patch.set_facecolor("#000000")
axd["BothTimeout"].patch.set_alpha(0.05)

# Setup other global plot properties

bounds = (0.005, 3600)
axd["BothFinished"].set_xlim(bounds)
axd["BothFinished"].set_ylim(bounds)
axd["BothFinished"].set_xscale("log")
axd["BothFinished"].set_yscale("log")

axd["BothFinished"].set_xlabel(f"Competing tool runtime (log)", fontsize=fontsize)
axd["BothFinished"].set_ylabel("Biobalm runtime (log)", fontsize=fontsize)
axd["BothFinished"].tick_params(gridOn=True, grid_alpha=grid_alpha, labelsize=fontsize-2)
axd["BothFinished"].set_xticks([0.01,0.1,1,10,60,300,1800])
axd["BothFinished"].set_xticklabels(["10ms", "0.1s","1s","10s","1min","5min","0.5h"])
axd["BothFinished"].set_yticks([0.01,0.1,1,10,60,300,1800])
axd["BothFinished"].set_yticklabels(["10ms", "0.1s","1s","10s","1min","5min","0.5h"])

axd["BalmTimeout"].set_xscale("log")
axd["BalmTimeout"].sharex(axd["BothFinished"])
axd["BalmTimeout"].tick_params(
    which="both",
    labelbottom=False,
    labelleft=False,
    tick1On=False,
    tick2On=False,
    labelsize=fontsize
)
axd["BalmTimeout"].tick_params(axis="x", gridOn=True, grid_alpha=grid_alpha)
axd["BalmTimeout"].tick_params(axis="y", tick1On=True, labelleft=True)
axd["BalmTimeout"].set_ylim(-0.5,1.5)
axd["BalmTimeout"].set_yticks([0.5])
axd["BalmTimeout"].set_yticklabels([">1h"])

axd["ToolTimeout"].set_yscale("log")
axd["ToolTimeout"].sharey(axd["BothFinished"])
axd["ToolTimeout"].tick_params(
    which="both",
    labelbottom=False,
    labelleft=False,
    tick1On=False,
    tick2On=False,
    labelsize=fontsize
)
axd["ToolTimeout"].tick_params(axis="y", gridOn=True, grid_alpha=grid_alpha)
axd["ToolTimeout"].tick_params(axis="x", tick1On=True, labelbottom=True)
axd["ToolTimeout"].set_xlim(-0.5,1.5)
axd["ToolTimeout"].set_xticks([0.5])
axd["ToolTimeout"].set_xticklabels([">1h"])

axd["BothTimeout"].tick_params(
    which="both",
    labelbottom=False,
    labelleft=False,
    tick1On=False,
    tick2On=False,
    labelsize=fontsize
)
axd["BothTimeout"].set_xlim(-.5, 1.5)
axd["BothTimeout"].set_ylim(-.5, 1.5)

# Draw comparison points for AEON and mtsNFVS
for i, (tool, tool_column) in enumerate([('AEON.py', "aeon [time]"), ("mtsNFVS", "mts-nfvs [time]")]):
    color = colors[tool]
    marker = markers[tool]
    marker_symbol = marker_symbols[tool]
    
    data_balm, data_tool = results[tool_columns['biobalm[block]']], results[tool_column]
    axd["BothFinished"].scatter(
        data_tool,
        data_balm,
        alpha=marker_alpha,
        color=color,
        s=marker_size,
        marker=marker,
        label=tool,
    )
    
    boundary_points = np.logspace(np.log10(0.1), np.log10(bounds[1]), 10)
    boundary_point_values = boundary_points * 10

    boundary_points = np.concatenate(([0.001], boundary_points))
    boundary_point_values = np.concatenate(([1], boundary_point_values))
    
    axd["BothFinished"].plot(
        boundary_points,
        boundary_point_values,
        color="black",
        linestyle="dashdot",
        linewidth=2,
        alpha=0.25,
    )

    axd["BothFinished"].plot(
        boundary_point_values,
        boundary_points,
        color="black",
        linestyle="dashdot",
        linewidth=2,
        alpha=0.25,
    )

    balm_timeouts = data_tool[data_balm == float("inf")]
    axd["BalmTimeout"].scatter(
        balm_timeouts,
        np.random.rand(len(balm_timeouts), 1),
        color=color,
        alpha=marker_alpha,
        s=marker_size,
        marker=marker,
    )
    

    tool_timeouts = data_balm[data_tool == float("inf")]
    axd["ToolTimeout"].scatter(
        np.random.rand(len(tool_timeouts), 1),
        tool_timeouts,
        color=color,
        alpha=marker_alpha,
        s=marker_size,
        marker=marker,
    )

    both_timeout = (data_tool == float("inf")) & (data_balm == float("inf"))
    
    print("Balm, completed, failed", sum(data_balm < float("inf")), sum(data_balm == float("inf")))
    print("Tool, completed, failed", sum(data_tool < float("inf")), sum(data_tool == float("inf")))

    tool_easy = data_tool <= 1
    balm_easy = data_balm <= 1

    balm_slower_count = sum(
        ((10*data_tool) <= data_balm) & 
        (data_balm < float("inf")) & 
        ~(tool_easy & balm_easy)
    )

    balm_faster_count = sum(
        ((10*data_balm) <= data_tool) & 
        (data_tool < float("inf")) &
        ~(tool_easy & balm_easy)
    )
    
    same_count_hard = sum(
        ((10*data_balm) > data_tool) & 
        ((data_balm < (10*data_tool))) &
        ~(tool_easy & balm_easy)
    )
    same_count = same_count_hard + sum(tool_easy & balm_easy)
    
    balm_failed_count = sum((data_balm == float("inf")) & (data_tool < float("inf")))
    tool_failed_count = sum((data_tool == float("inf")) & (data_balm < float("inf")))
    both_failed_count = sum((data_tool == float("inf")) & (data_balm == float("inf")))

    print("Balm was slower", balm_slower_count)
    print("Balm was faster", balm_faster_count)
    print("Comparable", same_count)
    print("Balm failed", balm_failed_count)
    print("Tool failed", tool_failed_count)
    print("Both failed", both_failed_count)

    # If you change the font size, you need to manually adjust the X in i/X because the size of the label is different.
    axd["BothFinished"].annotate(
        f"{marker_symbol} {balm_slower_count}", 
        xy=(0.09, 0.73-i/25), 
        xycoords="axes fraction", 
        color=color, 
        fontweight="bold",
        fontsize=fontsize
    )
    axd["BothFinished"].annotate(
        f"{marker_symbol} {balm_faster_count}", 
        xy=(0.63, 0.15-i/25), 
        xycoords="axes fraction", 
        color=color, 
        fontweight="bold",
        fontsize=fontsize
    )
    axd["BothFinished"].annotate(
        f"{marker_symbol} {same_count}", 
        xy=(0.09, 0.15-i/25),
        xycoords="axes fraction", 
        color=color, 
        fontweight="bold",
        fontsize=fontsize
    )
    
    axd["BalmTimeout"].annotate(
        f"{marker_symbol} {balm_failed_count}", 
        xy=(0.09, 0.58-i/2.5), 
        xycoords="axes fraction", 
        color=color, 
        fontweight="bold",
        fontsize=fontsize
    )
    axd["ToolTimeout"].annotate(
        f"{marker_symbol} {tool_failed_count}", 
        xy=(0.15+i/2.5, 0.09), 
        rotation=90, 
        xycoords="axes fraction", 
        color=color, 
        fontweight="bold",
        fontsize=fontsize
    )
    axd["BothTimeout"].annotate(
        f"{marker_symbol} {both_failed_count}", 
        xy=(0.05, 0.55-i/3), 
        xycoords="axes fraction", 
        color=color, 
        fontweight="bold",
        fontsize=10
    )

    afig.subplots_adjust(hspace=0.0135, wspace=0.0135)

axd["BothFinished"].legend(loc="upper left", prop={'family': 'monospace', 'size': fontsize})
fig.savefig("./figures/combined_time_scatter_benchmarks.pdf", bbox_inches="tight")

def simple_scatter_figure(
    results,
    tool_x_name,
    tool_x_column,
    tool_y_name,
    tool_y_column,
    file_name,
    title,
):
    """
    Build a simple scatter plot comparison for two tools without any fancy font scaling or legends.
    """

    stretch_factor = 11
    fontsize = 14
    marker_size = 25
    marker_alpha = 0.85
    grid_alpha = 0.25

    fig = plt.figure(figsize=(8,8))
    fig.set_facecolor("white")


    afig = fig.subfigures(1, 1)
    axd = afig.subplot_mosaic(
            [
                ["Y-Timeout", "XY-Timeout"],
                ["XY-Finished", "X-Timeout"],
            ],
            gridspec_kw={
                "width_ratios": [stretch_factor, 1],
                "height_ratios": [1, stretch_factor],
            },
        )

    # Add colored backgrounds.

    bad_area = patches.Polygon(
        xy=[(0.001,1), (0.1,1), (360,3600), (0.001,3600)],
        closed=True,
        facecolor='#ff0000',
        alpha=0.05
    )

    good_area = patches.Polygon(
        xy=[(1,0.001), (1,0.1), (3600,360), (3600,0.001)],
        closed=True,
        facecolor='#00ff00',
        alpha=0.05
    )

    meh_area = patches.Polygon(
        xy=[(0.001,0.01), (0.001,1), (0.1,1), (360,3600), (3600,3600), (3600,360), (1,0.1), (1,0.001), (0.001,0.001)],
        closed=True,
        facecolor='#000000',
        alpha=0.05
    )

    axd["XY-Finished"].add_patch(bad_area)
    axd["XY-Finished"].add_patch(good_area)
    axd["XY-Finished"].add_patch(meh_area)
    axd["Y-Timeout"].patch.set_facecolor("#ff0000")
    axd["Y-Timeout"].patch.set_alpha(0.05)
    axd["X-Timeout"].patch.set_facecolor("#00ff00")
    axd["X-Timeout"].patch.set_alpha(0.05)
    axd["XY-Timeout"].patch.set_facecolor("#000000")
    axd["XY-Timeout"].patch.set_alpha(0.05)

    # Setup other global plot properties

    bounds = (0.005, 3600)
    axd["XY-Finished"].set_xlim(bounds)
    axd["XY-Finished"].set_ylim(bounds)
    axd["XY-Finished"].set_xscale("log")
    axd["XY-Finished"].set_yscale("log")

    axd["XY-Finished"].set_xlabel(f"{tool_x_name} runtime (log)", fontsize=fontsize)
    axd["XY-Finished"].set_ylabel(f"{tool_y_name} runtime (log)", fontsize=fontsize)
    axd["XY-Finished"].tick_params(gridOn=True, grid_alpha=grid_alpha, labelsize=fontsize-2)
    axd["XY-Finished"].set_xticks([0.01,0.1,1,10,60,300,1800])
    axd["XY-Finished"].set_xticklabels(["10ms", "0.1s","1s","10s","1min","5min","0.5h"])
    axd["XY-Finished"].set_yticks([0.01,0.1,1,10,60,300,1800])
    axd["XY-Finished"].set_yticklabels(["10ms", "0.1s","1s","10s","1min","5min","0.5h"])

    axd["Y-Timeout"].set_xscale("log")
    axd["Y-Timeout"].sharex(axd["XY-Finished"])
    axd["Y-Timeout"].tick_params(
        which="both",
        labelbottom=False,
        labelleft=False,
        tick1On=False,
        tick2On=False,
        labelsize=fontsize
    )
    axd["Y-Timeout"].tick_params(axis="x", gridOn=True, grid_alpha=grid_alpha)
    axd["Y-Timeout"].tick_params(axis="y", tick1On=True, labelleft=True)
    axd["Y-Timeout"].set_ylim(-0.5, 1.5)
    axd["Y-Timeout"].set_yticks([-0.5,0.5,1.5])
    axd["Y-Timeout"].set_yticklabels(["", ">1h", ""])

    axd["X-Timeout"].set_yscale("log")
    axd["X-Timeout"].sharey(axd["XY-Finished"])
    axd["X-Timeout"].tick_params(
        which="both",
        labelbottom=False,
        labelleft=False,
        tick1On=False,
        tick2On=False,
        labelsize=fontsize
    )
    axd["X-Timeout"].tick_params(axis="y", gridOn=True, grid_alpha=grid_alpha)
    axd["X-Timeout"].tick_params(axis="x", tick1On=True, labelbottom=True)
    axd["X-Timeout"].set_xlim(-0.5, 1.5)
    axd["X-Timeout"].set_xticks([-0.5,0.5,1.5])
    axd["X-Timeout"].set_xticklabels(["", ">1h", ""])

    axd["XY-Timeout"].tick_params(
        which="both",
        labelbottom=False,
        labelleft=False,
        tick1On=False,
        tick2On=False,
        labelsize=fontsize
    )
    axd["XY-Timeout"].set_xlim(-.5, 1.5)
    axd["XY-Timeout"].set_ylim(-.5, 1.5)
    
    data_x, data_y = results[tool_x_column], results[tool_y_column]
    axd["XY-Finished"].scatter(
        data_x,
        data_y,
        alpha=marker_alpha,
        s=marker_size,
    )
    
    boundary_points = np.logspace(np.log10(0.1), np.log10(bounds[1]), 10)
    boundary_point_values = boundary_points * 10

    boundary_points = np.concatenate(([0.001], boundary_points))
    boundary_point_values = np.concatenate(([1], boundary_point_values))
    
    axd["XY-Finished"].plot(
        boundary_points,
        boundary_point_values,
        color="black",
        linestyle="dashdot",
        linewidth=2,
        alpha=0.25,
    )

    axd["XY-Finished"].plot(
        boundary_point_values,
        boundary_points,
        color="black",
        linestyle="dashdot",
        linewidth=2,
        alpha=0.25,
    )

    y_timeouts = data_x[data_y == float("inf")]
    axd["Y-Timeout"].scatter(
        y_timeouts,
        np.random.rand(len(y_timeouts), 1),
        alpha=marker_alpha,
        s=marker_size,
    )
    

    x_timeouts = data_y[data_x == float("inf")]
    axd["X-Timeout"].scatter(
        np.random.rand(len(x_timeouts), 1),
        x_timeouts,
        alpha=marker_alpha,
        s=marker_size,
    )

    xy_timeout = (data_tool == float("inf")) & (data_balm == float("inf"))
    
    x_easy = data_x <= 1
    y_easy = data_y <= 1

    y_slower_count = sum(
        ((10*data_x) <= data_y) & 
        (data_y < float("inf")) & 
        ~(x_easy & y_easy)
    )

    y_faster_count = sum(
        ((10*data_y) <= data_x) & 
        (data_x < float("inf")) &
        ~(x_easy & y_easy)
    )
    
    same_count_hard = sum(
        ((10*data_y) > data_x) & 
        ((data_y < (10*data_x))) &
        ~(x_easy & y_easy)
    )

    same_count = same_count_hard + sum(x_easy & y_easy)
    
    y_failed_count = sum((data_y == float("inf")) & (data_x < float("inf")))
    x_failed_count = sum((data_x == float("inf")) & (data_y < float("inf")))
    xy_failed_count = sum((data_x == float("inf")) & (data_y == float("inf")))

    # If you change the font size, you need to manually adjust the X in i/X because the size of the label is different.
    axd["XY-Finished"].annotate(
        f"●︎ {y_slower_count}", 
        xy=(0.09, 0.73), 
        xycoords="axes fraction", 
        fontweight="bold",
        fontsize=fontsize
    )
    axd["XY-Finished"].annotate(
        f"●︎ {y_faster_count}", 
        xy=(0.63, 0.15), 
        xycoords="axes fraction", 
        fontweight="bold",
        fontsize=fontsize
    )
    axd["XY-Finished"].annotate(
        f"●︎ {same_count}", 
        xy=(0.09, 0.15),
        xycoords="axes fraction", 
        fontweight="bold",
        fontsize=fontsize
    )
    
    axd["Y-Timeout"].annotate(
        f"●︎ {y_failed_count}", 
        xy=(0.09, 0.4), 
        xycoords="axes fraction", 
        fontweight="bold",
        fontsize=fontsize
    )
    axd["X-Timeout"].annotate(
        f"●︎ {x_failed_count}", 
        xy=(0.3, 0.15), 
        rotation=90, 
        xycoords="axes fraction", 
        fontweight="bold",
        fontsize=fontsize
    )
    axd["XY-Timeout"].annotate(
        f"●︎ {xy_failed_count}", 
        xy=(0.05, 0.4), 
        xycoords="axes fraction", 
        fontweight="bold",
        fontsize=10
    )

    afig.subplots_adjust(hspace=0.0135, wspace=0.0135)

    fig.suptitle(title, y=0.92, fontsize=fontsize)
    fig.savefig(file_name, bbox_inches="tight")

aeon = "AEON.py"
mts = "mtsNFVS"
balm = "biobalm[block]"
for model_type in ["bbm", "nk2", "nk3", "ncf", "dense"]:
    simple_scatter_figure(
        results.loc[results['Benchmark Type'] == model_type], 
        aeon,
        tool_columns[aeon],
        balm,
        tool_columns[balm],
        f"./figures/time_scatter_{model_type}_aeon.pdf",
        f"Biobalm vs. AEON; {model_type} ensemble"
    )
    simple_scatter_figure(
        results.loc[results['Benchmark Type'] == model_type], 
        mts,
        tool_columns[mts],
        balm,
        tool_columns[balm],
        f"./figures/time_scatter_{model_type}_mts.pdf",
        f"Biobalm vs. mtsNFVS; {model_type} ensemble"
    )

