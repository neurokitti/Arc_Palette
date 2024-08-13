#!/bin/zsh

# .command files change directory, need to open to directory where script launched from
cd "${0:A:h}"

# Check if Python 3 is installed
if ! python3 -V >/dev/null 2>&1; then
    echo "Python 3 is not installed. Please install Python 3.8 or higher and try again.  PYTHON DOWNLOAD: https://www.python.org/downloads/release/python-3125/"
    read -s -k '?Press any key to continue . . .'
	exit 1
fi

echo "Downloading Arc Palette Repo..."
curl -L https://github.com/neurokitti/Arc_Palette/archive/refs/heads/main.zip -o Arc_Palette.zip
echo "Unzipping Arc Palette..."
tar -xf Arc_Palette.zip
mv Arc_Palette-main Arc_Palette
echo "Deleting Arc Palette ZIP file..."
rm Arc_Palette.zip

cd Arc_Palette

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
pip3 install -r Arc_API/requirements-arc-api.txt

echo ""
echo "Installation complete!"
echo ""
./resources/Mac/run_arc_palette.command
read -s -k '?Press any key to continue . . .'
