#!/bin/bash

# The tested limit was 2^24kB 33_554_432kB ~ 33GB
if [[ -z "${MEMORY_LIMIT}" ]]; then
  echo "Please set env. variable MEMORY_LIMIT appropriate for your system (number, in kB)."
  exit 1
fi

ulimit -v $MEMORY_LIMIT

./venv/bin/python3 run_bench.py 1h ../models/bbm-bnet-inputs-true bench_sd_expand_bfs.py
./venv/bin/python3 run_bench.py 1h ../models/bbm-bnet-inputs-true bench_sd_expand_min.py
./venv/bin/python3 run_bench.py 1h ../models/bbm-bnet-inputs-true bench_sd_expand_scc.py
./venv/bin/python3 run_bench.py 1h ../models/bbm-bnet-inputs-true bench_sd_expand_attr.py

./venv/bin/python3 run_bench.py 1h ../models/bbm-bnet-inputs-true bench_sd_attractors_full.py
./venv/bin/python3 run_bench.py 1h ../models/bbm-bnet-inputs-true bench_sd_attractors_scc.py
./venv/bin/python3 run_bench.py 1h ../models/bbm-bnet-inputs-true bench_sd_attractors_simplified.py
./venv/bin/python3 run_bench.py 1h ../models/bbm-bnet-inputs-true bench_sd_attractors_minimal.py