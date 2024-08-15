#!/bin/bash

# Generate a performance artefact for AEON.py and all easy model instances.

./00_setup_aeon.sh
./00_setup_bench.sh

# Apply memory limit (only works on linux and cannot be done by a child script).
if [[ -z "${MEMORY_LIMIT}" ]]; then
  echo "Memory limit not set. Defaulting to 32GB."
  MEMORY_LIMIT=33554432
fi

ulimit -v $MEMORY_LIMIT

TIMEOUT=1h

set -x

./venv/bin/python3 run_bench.py $TIMEOUT models-easy/bbm-random bench_aeon_attractors.py -p 6
./venv/bin/python3 run_bench.py $TIMEOUT models-easy/random-nk2 bench_aeon_attractors.py -p 6
./venv/bin/python3 run_bench.py $TIMEOUT models-easy/random-nk3 bench_aeon_attractors.py -p 6
./venv/bin/python3 run_bench.py $TIMEOUT models-easy/random-ncf bench_aeon_attractors.py -p 6

zip -r perf-aeon-easy-`hostname`.zip _run_*
rm -rf _run_*