#! /bin/bash

echo "Running Price Server"

python3 -m venv venv
source ./venv/bin/activate
pip install --requirement ./requirements.txt

