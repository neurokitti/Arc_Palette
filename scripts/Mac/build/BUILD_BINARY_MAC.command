#!/bin/zsh
# You don't want to double click to run, you may need to run "chmod +x BUILD_BINARY_MAC.command" before attepting to run in the terminal

# .command files change directory, need to open to directory where script launched from
cd "${0:A:h}"

# Go to repo's root directory where everything is setup
cd ../../..

# Activating the virtual environment
source .venv/bin/activate

# change details here
NAME="Arc Palette"
DESCRIPTION="Arc Palette is a community-developed application that applies advanced gradient effects to spaces in the Arc browser."
VERSION="2.0"
IMGPATH="res/img"
IMGLIGHTPATH="${IMGPATH}/light"
IMGDARKPATH="${IMGPATH}/dark"
ICONPATH="${IMGPATH}/icon.ico"

# recommended not to change
binariesFolderPath="dist"

# don't touch, this is generated
osIsARM=$(/usr/bin/arch | grep -q '^arm.*' && echo 0 || echo 1)
osIs64Bit=$(uname -m | grep -q '.*64$' && echo 0 || echo 1)
# architecture is required for generating of binary name
osArch="$(
    [ 0 -eq $osIsARM ] && echo 'arm' || echo 'x'
)$(
    [ 0 -eq $osIs64Bit ] && echo '64' || $([ 0 -ne $osIsARM ] && echo '86')
)"
binaryName="${NAME// /_}-${osArch}"

# Nuitka BROKEN: See https://doc.qt.io/qtforpython-6/deployment/deployment-nuitka.html#nuitka-issue-on-macos

# Note: This will auto download/cache the required compiler and linker for Nuitka if one or both are not available on the computer
#nuitka main.py --macos-create-app-bundle --remove-output --assume-yes-for-downloads --follow-imports \
#  --enable-plugin=tk-inter \
#  --macos-app-icon="${ICONPATH}" \
#  --include-data-files="${ICONPATH}=${ICONPATH}" \
#  --include-data-dir="${IMGLIGHTPATH}=${IMGLIGHTPATH}" \
#  --include-data-dir="${IMGDARKPATH}=${IMGDARKPATH}" \
#  --file-version="${VERSION}" --product-version="${VERSION}" \
#  --file-description="${DESCRIPTION}" \
#  --product-name="${NAME}" --macos-app-name="${NAME}" \
#  --output-filename="${NAME}" \
#  --output-dir="${binariesFolderPath}"
# package the .APP into a .DMG
#mkdir "binaries/${binaryName}"
#mv "binaries/${NAME}.app" "binaries/${binaryName}/${NAME}.app"
#hdiutil create -srcfolder "binaries/${binaryName}" "binaries/${binaryName}.dmg"
#rm -rf "binaries/${binaryName}"

# Have to keep using pyinstaller for the interim, which has less options... #### TODO Might need to do more --collect-all ...
pyinstaller main.py --onefile --clean --noconfirm \
  --windowed \
  --collect-all sv_ttk \
  --add-data="hot_fixes/*:hot_fixes/" \
  --add-data="utils.py:." \
  --add-data="${IMGLIGHTPATH}/*:${IMGLIGHTPATH}/" \
  --add-data="${IMGDARKPATH}/*:${IMGDARKPATH}/" \
  --add-data="${ICONPATH}:${IMGPATH}/" \
  --name="${NAME}" \
  --icon="${ICONPATH}"
# remove previous package if it exists in directory
if [ -f "dist/${binaryName}.dmg" ]; then
    rm -f "dist/${binaryName}.dmg"
fi
# package the .APP into a .DMG
mkdir "dist/${binaryName}"
mv "dist/${NAME}.app" "dist/${binaryName}/${NAME}.app"
hdiutil create -srcfolder "dist/${binaryName}" "dist/${binaryName}.dmg"
rm -rf "dist/${binaryName}"

deactivate
