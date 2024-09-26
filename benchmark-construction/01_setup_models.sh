#!/bin/bash

# For this test, we only consider BBM models, with one instance per model.
rm -rf models-bbm
mkdir models-bbm
cp -r ../models/bbm-bnet-inputs-true/*.bnet models-bbm/

# Remove the three largest succession diagrams, since neither can be computed
# fully by either tool (at least not quick enough).
rm ./models-bbm/004.bnet
rm ./models-bbm/079.bnet
rm ./models-bbm/144.bnet