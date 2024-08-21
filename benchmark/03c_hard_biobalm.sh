#!/bin/bash

# Generate a performance artefact for biobalm and all hard model instances.

./00_setup_biobalm.sh
./00_setup_bench.sh

# Apply memory limit (only works on linux and cannot be done by a child script).
if [[ -z "${MEMORY_LIMIT}" ]]; then
  echo "Memory limit not set. Defaulting to 32GB per process."
  MEMORY_LIMIT=67108864
fi

ulimit -v $MEMORY_LIMIT

TIMEOUT=1h

set -x

./venv/bin/python3 run_bench.py $TIMEOUT models-hard/bbm-random bench_balm_block_attractors.py -p 2
./venv/bin/python3 run_bench.py $TIMEOUT models-hard/random-nk2 bench_balm_block_attractors.py -p 2
./venv/bin/python3 run_bench.py $TIMEOUT models-hard/random-nk3 bench_balm_block_attractors.py -p 2
./venv/bin/python3 run_bench.py $TIMEOUT models-hard/random-ncf bench_balm_block_attractors.py -p 2

./venv/bin/python3 run_bench.py $TIMEOUT models-hard/bbm-random bench_balm_full_expand.py -p 2
./venv/bin/python3 run_bench.py $TIMEOUT models-hard/random-nk2 bench_balm_full_expand.py -p 2
./venv/bin/python3 run_bench.py $TIMEOUT models-hard/random-nk3 bench_balm_full_expand.py -p 2
./venv/bin/python3 run_bench.py $TIMEOUT models-hard/random-ncf bench_balm_full_expand.py -p 2

./venv/bin/python3 run_bench.py $TIMEOUT models-hard/bbm-random bench_balm_full_attractors.py -p 2
./venv/bin/python3 run_bench.py $TIMEOUT models-hard/random-nk2 bench_balm_full_attractors.py -p 2
./venv/bin/python3 run_bench.py $TIMEOUT models-hard/random-nk3 bench_balm_full_attractors.py -p 2
./venv/bin/python3 run_bench.py $TIMEOUT models-hard/random-ncf bench_balm_full_attractors.py -p 2

zip -r perf-biobalm-hard-`hostname`.zip _run_* models-easy 
rm -rf _run_*