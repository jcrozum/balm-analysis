#!/bin/bash

rm -rf ./venv
python3 -m venv ./venv

# Install dependencies.
pip install git+https://github.com/jcrozum/pystablemotifs