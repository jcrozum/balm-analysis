#!/bin/bash

# The purpose of this script is to compute an "artefact" that can be used 
# to compare the performance of `biobalm` between versions consistently.

# Note that even though we try to limit the evaluation as much as possible,
# the whole process will still typically require several hours.

# Also note that on laptops (and improperly built desktops :D), the
# temperature of the environment can have a measurable impact on performance
# and we are not doing any special variance analysis... always measure
# in a reasonably consistent conditions.

# The script will setup its own virtual environment in which Python
# dependencies will be installed.

# This script does not perform any correctness checking, but it could be 
# a good idea to validate that the results that were computed successfully
# actually match between versions.

if [[ $(ls _run_*) ]]; then
    echo "There are existing result runs already present. Please remove them first."
    exit 2
fi

# if git diff-index --quiet HEAD --; then
#     echo "No uncommitted changes. Installing biobalm..."
# else
#     echo "There are uncommitted changes. Please commit or stash them."
#     exit 2
# fi

rm -rf ./venv
python3 -m venv ./venv

# Install biobalm and dependencies.
./venv/bin/pip install biodivine_aeon==1.0.0a6


# Apply memory limit.
# The tested limit was 2^25kB 33_554_432kB ~ 33GB
if [[ -z "${MEMORY_LIMIT}" ]]; then
  #echo "Please set env. variable MEMORY_LIMIT appropriate for your system (number, in kB)."
  #exit 1
  echo "Memory limit not set. Defaulting to 32GB."
  MEMORY_LIMIT=33554432
fi

ulimit -v $MEMORY_LIMIT

# Save the name of the machine, the current git commit and pip list 
# for future reference.
git rev-parse HEAD > _run_git_rev.txt
hostname > _run_hostname.txt
./venv/bin/pip list > _run_pip_list.txt

MODEL_DIR=../models/random_nk3
TIMEOUT=1h

set -x

# Benchmark minimal expansion (this ignores motif-avoidant attractors).
./venv/bin/python3 run_bench.py $TIMEOUT $MODEL_DIR bench_aeon_attractors.py

zip -r perf_aeon_random_nk3_`hostname`.zip _run_*
