#!/bin/bash

# Set up our env var
if [[ -z "${HF_HOME}" ]]; then
  echo "HF_HOME has not been set. Please enter the directory where you want the models to be stored: "
  read model_dir
  export HF_HOME=$model_dir
else
  echo "HF_HOME is set, downloading models to ${HF_HOME}!"
fi

# Activate the virtual environment for main model caching
cd ./src

python3 -m venv ./venv

source ./venv/bin/activate

pip install -r requirements.txt

cd scripts

# Run the model caching scripts for data_toolbox
python _image_to_text_cache_models.py
python _image_triage_cache_models.py

# Setup venv for diarization and cache its model
cd ../../diarization

python3 -m venv ./venv

source ./venv/bin/activate

pip install -r requirements.txt

cd scripts

python _diarization_cache_models.py

# Setup venv for text_extractor and cache its model
cd ../../text_extractor

python3 -m venv ./venv

source ./venv/bin/activate

pip install -r requirements.txt

cd scripts

python _text_extractor_cache_models.py

# Go back to main directory and deactivate all venvs.
cd ../../../../
deactivate