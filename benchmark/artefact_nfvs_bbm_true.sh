#!/bin/bash

# Generate a performance artefact for mts-nfvs and bbm-inputs-true models.

if [[ $(ls _run_*) ]]; then
    echo "There are existing result runs already present. Please remove them first."
    exit 2
fi

rm -rf ./venv
python3 -m venv ./venv

# Install dependencies. mtsNFVS is already in the repo.
./venv/bin/pip install biodivine_aeon==1.0.0a6
./venv/bin/pip install networkx pyeda

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

MODEL_DIR=../models/bbm-bnet-inputs-true
TIMEOUT=1h

# Number of attractors is not printed on the last line.
export OUTPUT_LINE=-2

set -x

./venv/bin/python3 run_bench.py $TIMEOUT $MODEL_DIR bench_mts_nfvs_attractors.py

zip -r perf_mts_nfvs_bbm_true_`hostname`.zip _run_*
