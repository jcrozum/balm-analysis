# Attractor benchmarking

This folder (together with the `models` directory) contains all resources necessary to reproduce
the benchmark analysis of the biobalm paper. Each benchmark has a script to run it and produces
a `.zip` file with complete tool outputs as well as a summary `.csv` table.

The artefact is valid for Linux Debian and should provide all custom or not generally available
dependencies (other dependencies are downloaded from PyPI through `pip`). The tested tools should 
also work on other operating systems, but we do not provide any automation for such cases.

Finally, the official testing was performed on a Ryzen 5800X CPU locked to `4.7Ghz` with 
`128GB` of RAM, but each benchmark only uses a single core and has a memory limit of `<32GB`.
After the initial pre-testing, we further separated the benchmark instances into "easy" 
and "hard": For "easy" instances, we run up to six benchmarks in parallel to speed up the
analysis, since these generally consume very little resources (`<1m` runtime, `<1GB` RAM). 
For "hard" instances, we only run up to two benchmarks in parallel, as these can actually
exhaust the prescribed memory limits. Also note that the testing results can consume a non-trivial 
amount of disk space (`10GB` should be sufficient), since we also output the succession 
diagrams as `pickle` files.

 > Note that `mts-nfvs` is non-deterministic, meaning that the performance can change depending
 > on internal randomized decisions taken by the tool. As such, individual benchmark results 
 > may not be fully reproducible, but should reflect an overall trend.

 > If you don't have enough RAM, you can set the environmental variable `MEMORY_LIMIT` to a
 > custom value (in kB) that will be used instead. For example, to limit memory usage to 8GB,
 > run `export MEMORY_LIMIT=8388608` in the terminal where you'll be running the tests.

 > Interpreting test results: Note that due to the rather wide variety of used technologies,
 > our benchmark script cannot always distinguish between a successful and a failed run, especially
 > if out of memory error occurs. What this means in practice is that even if a benchmark has 
 > a recorded "completion time", it does not necessarily mean the result is valid. We solve this 
 > by further filtering the data when generating individual performance figures (each benchmark 
 > prints enough information to indicate a success/failure). 

 > Also note that when memory limit is exceeded, `mts-nfvs` can sometimes output an incomplete
 > result, meaning the number of attractors is under-counted. We solve this issue by comparing
 > the result with the remaining tools in the instances where at least one other tool finished.

## 1. Model preparation

Before running any benchmarks, we first prepare the testing data.

Tested models:
 - 230 models from the BBM dataset. If applicable, we sample up to 128 unique input valuations.
   * Model BBM-144 is excluded from testing, since it has more than one billion fixed-point attractors, 
   which isn't feasible with any of the tested tools (estimated using AEON.py).
   * Including randomized input valuations, this amounts to 13089 "easy" instances and 919 "hard" instances.
 - Critical random NK models with `K=2`, sizes `N=10,20,40,80,160,320,640,1280,2560`. For each size, 
   100 models are sampled using `pystablemotifs`. (see `generate_random_nk.py`)
   * We consider every model with 160 or more variables as hard, giving 400 "easy" instances and 500 "hard" instances.
 - Critical random NK models with `K=3`, sizes `N=10,20,40,80,160,320,640,1280,2560`. For each size, 
   100 models are sampled using `pystablemotifs`. (see `generate_random_nk.py`)
   * We consider every model with 160 or more variables as hard, giving 400 "easy" instances and 500 "hard" instances.
 - Random networks with nested canalyzing functions, sizes `N=10,20,40,80,160,320,640,1280,2560`. For each size, 
   we consider 100 models. (see `generate_random_ncfs.py`)
   * We consider every model with 160 or more variables as hard, giving 400 "easy" instances and 500 "hard" instances.
 - Dense random models, originally used for the evaluation of `mts-nfvs`. These have `N=100,200,200` and 
   20 instances for each size.
   * All 60 of these models are considered "hard".

Overall, this gives 14291 "easy" model instances and 2479 "hard" models.

To prepare the test models, please run:

```
# First unzip BBM model data.
(cd ../models; unzip bbm-bnet-inputs-random-128)
# Then run a script to copy relevant models into the benchmarks directory.
./01_setup_models.sh
```

This will delete any existing model folders and copy all relevant model instances from `../models` into separate
`models-easy` and `models-hard` directories.

## 2. Easy benchmarks

Next, you can execute the easy benchmark instances. This should still take several hours to complete, simply due 
to the number of models that needs to be tested.

```
./02a_easy_aeon.sh
./02b_easy_mts_nfvs.sh
./02c_easy_biobalm.sh
```

Each script should create a dedicated Python virtual environment and install its dependencies there. After
the script is finished, it should produce a `perf-*.zip` file with all the raw outputs for individual model
categories. For each model category, a summary table with runtimes is also constructed (this is later used 
to generate the performance figures). The `biobalm` archive also contains the full succession diagrams for 
all successfully expanded models (for each `.bnet` file, there should be a corresponding `.pickle` file).

## 3. Hard benchmarks

Similarly, you can execute the hard benchmark instances. These tests are quite complex and each can take up
to several days to complete, depending on the number of timeouts.

```
./03a_hard_aeon.sh
./03b_hard_mts_nfvs.sh
./03c_hard_biobalm.sh
```

As before, this should produce `perf-*.zip` archives with raw outputs, summary tables, and in the case
of `biobalm`, the full succession diagrams.

## 4. Result processing

We already provide our own results in the `results-raw` directory. To process the provided results, 
simply unzip all the archives in this directory, and run `python3 process_stats.py`. This should automatically
match tools with their results, exclude outputs that are incomplete due to out-of-memory errors, and process
the results into `results-*.tsv` tables (our result tables are also included for completeness).

If you want to process your own results, simply replace the zip files in `results-raw` with your own
data, extract the zip files, and run `python3 process_stats.py`. You should see that the result tables
have been updated with the new data.

Note that it is not required to have all data present to perform the analysis. You can also obtain partial
results if the `results-raw` only contains data for certain tools or certain datasets (e.g. you only ran
the easy benchmarks).

## Other

Finally, we list several commands that are useful for testing individual models. Note that you only
need to create and activate the environment once assuming you are using a single tool (if you are
testing multiple tools, you'll need to recreate the environment between runs, or manually create an
environment with all tools).

```
./00_setup_aeon.sh # Create virtual environment with biodivine_aeon
source /venv/bin/activate

# Perform attractor detection.
python3 bench_aeon_attractors.py PATH_TO_MODEL
```

```
./00_setup_mts_nfvs.sh # Create virtual environment with mts-nfvs
source /venv/bin/activate

# Perform attractor detection.
python3 bench_mts_nfvs_attractors.py PATH_TO_MODEL
```

```
./00_setup_biobalm.sh # Create virtual environment with biobalm
source /venv/bin/activate

# Perform simplified expansion and attractor detection.
python3 bench_balm_block_attractors.py PATH_TO_MODEL
# Perform full expansion and save result.
python3 bench_balm_full_expand.py PATH_TO_MODEL
# Perform attractor detection on the fully expanded SD (requires that full_expand is executed before).
python3 bench_balm_full_attractors.py PATH_TO_MODEL
```