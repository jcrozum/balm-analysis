#!/bin/bash

# If anything fails, we need to abort the script.
set -e

# Generate a performance artefact for mts-nfvs and all hard model instances.

./00_setup_mts_nfvs.sh
./00_setup_bench.sh

# Apply memory limit (only works on linux and cannot be done by a child script).
if [[ -z "${MEMORY_LIMIT}" ]]; then
  echo "Memory limit not set. Defaulting to 32GB per process."
  MEMORY_LIMIT=67108864
fi

ulimit -v $MEMORY_LIMIT


# Number of attractors is not printed on the last line.
export OUTPUT_LINE=-2

TIMEOUT=1h

set -x

./venv/bin/python3 run_bench.py $TIMEOUT models-hard/bbm-random bench_mts_nfvs_attractors.py -p 2
./venv/bin/python3 run_bench.py $TIMEOUT models-hard/random-nk2 bench_mts_nfvs_attractors.py -p 2
./venv/bin/python3 run_bench.py $TIMEOUT models-hard/random-nk3 bench_mts_nfvs_attractors.py -p 2
./venv/bin/python3 run_bench.py $TIMEOUT models-hard/random-ncf bench_mts_nfvs_attractors.py -p 2
./venv/bin/python3 run_bench.py $TIMEOUT models-hard/random-dense bench_mts_nfvs_attractors.py -p 2

zip -r perf-mts-nfvs-hard-`hostname`.zip _run_*
rm -rf _run_*

rm ./mtsNFVS/python/networks/*
rm ./mtsNFVS/python/predata/*
rm ./mtsNFVS/python/results/*