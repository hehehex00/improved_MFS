#!/bin/sh

# Linux / MacOS

# Create the virtual environment ensuring to specify the correct version
python3.11 -m venv myvenv
source myvenv/bin/activate

# Install Python packages
pip install .
cd src
pip install -r requirements.txt
pip install -r requirements-dev.txt

export SL_ANALYTICS_PATH=./analytics/
export LOG_ANALYTICS=False
echo "To enable log analytics, type 'export LOG_ANALYTICS=True'"