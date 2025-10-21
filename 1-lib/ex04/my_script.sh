#!/bin/bash

set -e

python3.12 -m venv django_venv

django_venv/bin/pip install --upgrade pip setuptools wheel
django_venv/bin/pip install -r requirement.txt --only-binary :all:

echo "Virtual environment 'django_venv' is ready."
echo "Activating..."
source ./django_venv/bin/activate
