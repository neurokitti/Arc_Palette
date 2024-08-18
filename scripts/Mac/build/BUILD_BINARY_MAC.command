#!/bin/zsh
# You don't want to double click to run, you may need to run "chmod +x BUILD_BINARY_MAC.command" before attepting to run in the terminal

# .command files change directory, need to open to directory where script launched from
cd "${0:A:h}"

# Go to repo's root directory where everything is setup
cd ../../..

# Activating the virtual environment
source .venv/bin/activate

# path to app config json, to read from
appConfigJson="app_config.json"
configInfo=$(cat "${appConfigJson}")

# change details in the config, not here
VERSION=$(echo "${configInfo}" | python -c 'import json,sys;print(json.load(sys.stdin)["VERSION"])')
NAME=$(echo "${configInfo}" | python -c 'import json,sys;print(json.load(sys.stdin)["NAME"])')
DESCRIPTION=$(echo "${configInfo}" | python -c 'import json,sys;print(json.load(sys.stdin)["DESCRIPTION"])')
IMGPATH="res/img"
IMGLIGHTPATH="${IMGPATH}/light"
IMGDARKPATH="${IMGPATH}/dark"
ICONPATH="${IMGPATH}/icon.icns"

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

# # Note: This will auto download/cache the required compiler and linker for Nuitka if one or both are not available on the computer
# nuitka main.py --macos-create-app-bundle --remove-output --assume-yes-for-downloads --follow-imports \
#   --enable-plugin=tk-inter \
#   --macos-app-icon="${ICONPATH}" \
#   --include-data-files="${ICONPATH}=${ICONPATH}" \
#   --include-data-dir="${IMGLIGHTPATH}=${IMGLIGHTPATH}" \
#   --include-data-dir="${IMGDARKPATH}=${IMGDARKPATH}" \
#   --file-version="${VERSION}" --product-version="${VERSION}" --macos-app-version="${VERSION}" \
#   --file-description="${DESCRIPTION}" \
#   --product-name="${NAME}" --macos-app-name="${NAME}" \
#   --output-filename="${NAME}" \
#   --output-dir="${binariesFolderPath}"
# # package the .APP into a .DMG
# mkdir "${binariesFolderPath}/${binaryName}"
# mv "${binariesFolderPath}/${NAME}.app" "${binariesFolderPath}/${binaryName}/${NAME}.app"
# hdiutil create -srcfolder "${binariesFolderPath}/${binaryName}" "${binariesFolderPath}/${binaryName}.dmg"
# rm -rf "${binariesFolderPath}/${binaryName}"

# Have to keep using pyinstaller for the interim

# create temp files
pyinstallerVersionYAML="metadata.yml"
cat > "${pyinstallerVersionYAML}" <<- EOM
Version: ${VERSION}
CompanyName: 
FileDescription: ${DESCRIPTION}
InternalName: ${NAME}
LegalCopyright: 
OriginalFilename: ${NAME}.app
ProductName: ${NAME}
Translation:
  - langID: 0
    charsetID: 1200
  - langID: 1033
    charsetID: 1252
EOM
pyinstallerFileVersionINFO="file_version_info.txt"
create-version-file "${pyinstallerVersionYAML}" --outfile "${pyinstallerFileVersionINFO}"

# remove previous package if it exists in directory
if [ -f "${binariesFolderPath}/${binaryName}.dmg" ]; then
    rm -f "${binariesFolderPath}/${binaryName}.dmg"
fi

pyinstaller main.py --onefile --clean --noconfirm \
  --windowed \
  --collect-all sv_ttk \
  --add-data="utils.py:." \
  --add-data="${IMGLIGHTPATH}/*:${IMGLIGHTPATH}/" \
  --add-data="${IMGDARKPATH}/*:${IMGDARKPATH}/" \
  --add-data="${ICONPATH}:${IMGPATH}/" \
  --version-file "${pyinstallerFileVersionINFO}" \
  --name="${NAME}" \
  --icon="${ICONPATH}"
# package the .APP into a .DMG
mkdir "${binariesFolderPath}/${binaryName}"
mv "${binariesFolderPath}/${NAME}.app" "${binariesFolderPath}/${binaryName}/${NAME}.app"
hdiutil create -srcfolder "${binariesFolderPath}/${binaryName}" "${binariesFolderPath}/${binaryName}.dmg"
# remove temp files
rm -f "${pyinstallerVersionYAML}"
rm -f "${pyinstallerFileVersionINFO}"
rm -rf "${binariesFolderPath}/${binaryName}"

deactivate
