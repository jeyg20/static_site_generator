#!/bin/bash

# Use the python interpreter within your virtual environment to run pytest as a module
python -m pytest -vsx "$@"
