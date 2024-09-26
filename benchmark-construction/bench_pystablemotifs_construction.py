# type: ignore
import sys
import time

import pystablemotifs
from biodivine_aeon import BooleanNetwork

sys.setrecursionlimit(150_000)
path = sys.argv[1]
print(f"model: {path}")

# Import the rules in pystablemotifs.
primes = pystablemotifs.format.import_primes(path)

# Build the succession diagram in pystablemotifs
ar = pystablemotifs.AttractorRepertoire.from_primes(
    primes, MPBN_update=True
)  # MPBN_update just for faster testing
at.summary()

print(f"{ar.fewest_attractors}, {ar.most_attractors}")