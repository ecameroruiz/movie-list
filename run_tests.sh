#!/usr/bin/env bash
source app_env/bin/activate
pip3 install -r requirements.txt
python -m unittest discover -s tests -p 'tests.py' -v