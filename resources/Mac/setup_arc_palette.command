#!/bin/zsh

# .command files change directory, need to open to directory where script launched from
cd "${0:A:h}"

# Go to repo's root directory where everything is setup
cd ../..

echo "Cloning Arc_API..."
git clone https://github.com/neurokitti/Arc_API.git
echo "creating venv..."
python3 -m venv .venv
echo "activating venv..."
source .venv/bin/activate
echo "installing requirements..."
pip3 install -r requirements.txt
pip3 install -r Arc_API/requirements-arc-api.txt

echo ''
echo "Installation complete!"


read -s -k '?Press any key to continue . . .'
