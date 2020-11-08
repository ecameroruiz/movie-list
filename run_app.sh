#!/bin/bash
source app_env/bin/activate
pip3 install -r requirements.txt
gunicorn app:app -b 0.0.0.0:8000