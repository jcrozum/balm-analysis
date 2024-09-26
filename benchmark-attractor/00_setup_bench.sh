#!/bin/bash

# Prepare the directory for a fresh benchmark.

if [[ $(ls _run_*) ]]; then
    echo "There are existing result runs already present. Please remove them first."
    exit 2
fi

# Save the name of the machine, the current git commit and pip list 
# for future reference.
git rev-parse HEAD > _run_git_rev.txt
hostname > _run_hostname.txt
./venv/bin/pip list > _run_pip_list.txt
