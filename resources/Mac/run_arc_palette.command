#!/bin/zsh

# .command files change directory, need to open to directory where script launched from
cd "${0:A:h}"

# Go to repo's root directory where everything is setup
cd ../..

# Activating the virtual environment (optional step)
source .venv/bin/activate

# Running the Python script
python3 main.py

# Deactivating the virtual environment (optional step)
deactivate
