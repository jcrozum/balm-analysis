#!/bin/bash

rm -rf ./venv
python3 -m venv ./venv

# Install dependencies.
#./venv/bin/pip install biobalm==0.3.1
./venv/bin/pip install ../../biobalm