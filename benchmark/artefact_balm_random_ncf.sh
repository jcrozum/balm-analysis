#!/bin/bash

# Generate a performance artefact for biobalm and random-ncf models.

if [[ $(ls _run_*) ]]; then
    echo "There are existing result runs already present. Please remove them first."
    exit 2
fi

rm -rf ./venv
python3 -m venv ./venv

# Install dependencies.
# ./venv/bin/pip install biobalm==0.2.0
./venv/bin/pip install ../../biobalm

# Apply memory limit (only works on linux).
if [[ -z "${MEMORY_LIMIT}" ]]; then
  echo "Memory limit not set. Defaulting to 32GB."
  MEMORY_LIMIT=33554432
fi

ulimit -v $MEMORY_LIMIT

# Save the name of the machine, the current git commit and pip list 
# for future reference.
git rev-parse HEAD > _run_git_rev.txt
hostname > _run_hostname.txt
./venv/bin/pip list > _run_pip_list.txt

MODEL_DIR=../models/random_ncf
TIMEOUT=1h

set -x

./venv/bin/python3 run_bench.py $TIMEOUT $MODEL_DIR bench_balm_block_attractors.py
./venv/bin/python3 run_bench.py $TIMEOUT $MODEL_DIR bench_balm_full_expand.py
./venv/bin/python3 run_bench.py $TIMEOUT $MODEL_DIR bench_balm_full_attractors.py

zip -r perf_balm_random_ncf_`hostname`.zip _run_*
