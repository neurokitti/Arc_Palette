#!/bin/zsh

# .command files change directory, need to open to directory where script launched from
cd "${0:A:h}"

# Go to repo's root directory where everything is setup
cd ../..

echo "Downloading Arc_API..."
curl -L https://github.com/neurokitti/Arc_API/archive/refs/heads/main.zip -o Arc_API.zip
echo "Unzipping Arc_API..."
tar -xf Arc_API.zip
mv Arc_API-main Arc_API
echo "Deleting Arc_API ZIP file..."
rm Arc_API.zip

echo "Creating venv..."
python3 -m venv .venv
echo "Activating venv..."
source .venv/bin/activate

echo "Installing requirements..."
pip3 install -r requirements.txt
pip3 install -r requirements-mac.txt
pip3 install -r Arc_API/requirements-arc-api.txt

deactivate

echo ""
echo "Installation complete!"


read -s -k '?Press any key to continue . . .'
