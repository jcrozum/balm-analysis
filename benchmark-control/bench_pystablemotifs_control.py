# type: ignore
import sys
import time

import pystablemotifs
from pathlib import Path

sys.setrecursionlimit(150_000)
path = sys.argv[1]
print(f"model: {path}")

target = eval(Path(sys.argv[1].replace(".bnet", ".target.txt")).read_text())

# Import the rules in pystablemotifs.
primes = pystablemotifs.format.import_primes(path)

# Build the succession diagram in pystablemotifs
ar = pystablemotifs.AttractorRepertoire.from_primes(
    primes, MPBN_update=True
)  # MPBN_update just for faster testing
ar.summary()

print(f"{ar.fewest_attractors}, {ar.most_attractors}")

interventions_pystablemotifs = ar.reprogram_to_trap_spaces(target)
print(interventions_pystablemotifs)
print(len(interventions_pystablemotifs))
