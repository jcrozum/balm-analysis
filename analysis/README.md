# Analysis and figures

This folder contains the Python scripts and Jupyter notebooks for generating the figures presented in the paper.

In general, all paths or other options are hardcoded in the files themselves and it should be sufficient
to run them.

 > Most scripts require `matplotlib`, `scipy`, `pandas` and `numpy` to be installed.

## Benchmark figures

Benchmark figures for attractor identification, control, and SD construction:

```
python3 benchmark_figures_construction.py
python3 benchmark_figures_control.py
python3 benchmark_figures_cumulative.py
python3 benchmark_figures_scatter.py
```

## Succession diagram structure

Jupyter notebooks for generating the statistical analysis of large succession diagram ensembles (open using `python3 -m jupyter notebook`):

```
# Core figures comparing the properties of succession diagrams between random and real-world networks.
figures.ipynb
# Figures comparing the properties of succession diagrams across different sub-ensembles.
binned_figures.ipynb
# Comparison of succession diagrams for CaSQ-generated vs. other BNs from BBM.
casq_comparison.ipynb
# Supporting analysis for 95% bootstrap confidence intervals when 
# comparing real-world and random succession diagrams.
stat_analysis_bootstrap.ipynb
```