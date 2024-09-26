# Succession diagram construction

This part shows how to compare `biobalm` to `pystablemotifs` when building the succession diagram. It works similarly to the attractor benchmark, but is simpler since we use stricter resource limits.

To execute the benchmark, run the following commands:

```
./01_setup_models.sh

# Should run for a few hours.
./02a_pystablemotifs.sh

# Should run for a few minutes.
./02b_biobalm.sh
```

All benchmarks run six instances in parallel with a memory limit of 32GB and a time limit of 10 minutes. We exclude four models (`004`, `079`, `122` and `144`), where we know that the succession diagram is too large to enumerate in 10 minutes, regardless of the chosen method.

As in the case of attractors, we provide our result archives in `results-raw` (you can replace them with your own result archives if you have them) and you can then generate the result table by running `python3 process_stats.py` (after you unzip the result archives). The instructions for generating the performance figures are in the `analysis` folder.