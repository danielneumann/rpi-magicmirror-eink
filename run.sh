#!/bin/bash
source .venv/bin/activate
#python3 main.py -c "0 */6 * * *"
python3 main.py -c "* * * * *"
run
