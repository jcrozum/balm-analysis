#!/bin/bash

rm -rf ./venv
python3 -m venv ./venv

# Install dependencies. mtsNFVS is already in the repo.
./venv/bin/pip install biodivine_aeon==1.0.0a10
./venv/bin/pip install networkx pyeda
