#!/bin/bash

# If anything fails, we need to abort the script.
set -e

# Generate a performance artefact for biobalm and all easy model instances.

./00_setup_biobalm.sh
./00_setup_bench.sh

# Apply memory limit (only works on linux and cannot be done by a child script).
if [[ -z "${MEMORY_LIMIT}" ]]; then
  echo "Memory limit not set. Defaulting to 32GB."
  MEMORY_LIMIT=33554432
fi

ulimit -v $MEMORY_LIMIT

TIMEOUT=10m

set -x

./venv/bin/python3 run_bench.py $TIMEOUT models-bbm bench_balm_construction.py -p 6

zip -r perf-biobalm-`hostname`.zip _run_* 
rm -rf _run_*