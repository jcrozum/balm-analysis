#!/bin/bash

rm -rf ./venv
python3 -m venv ./venv

# Install dependencies.
./venv/bin/pip install biodivine_aeon==1.0.0a10