#!/bin/bash
pyenv virtualenv tc2r_env
pyenv activate tc2r_env
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python -m ipykernel install --user --name my_jupyter_env --display-name "tc2r_env"