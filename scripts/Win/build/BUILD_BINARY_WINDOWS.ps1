#Requires -Version 7
# You can run this file with the "BUILD_BINARY_WINDOWS.bat" script, or use extract the command from the .bat to use manually to launch this script

# .ps1 files change directory, need to open to directory where script launched from
Set-Location $PSScriptRoot

# Go to repo's root directory where everything is setup
Set-Location ..\..\..

# Activating the virtual environment
. .\.venv\Scripts\activate

# path to app config json, to read from
$appConfigJson = "app_config.json"
$configInfo = $(Get-Content $appConfigJson)

# change details in the config, not here
$VERSION = $(Write-Output $configInfo | python -c 'import json,sys;print(json.load(sys.stdin)["VERSION"])')
$NAME = $(Write-Output $configInfo | python -c 'import json,sys;print(json.load(sys.stdin)["NAME"])')
$DESCRIPTION = $(Write-Output $configInfo | python -c 'import json,sys;print(json.load(sys.stdin)["DESCRIPTION"])')
$IMGPATH = "res/img"
$IMGLIGHTPATH = "${IMGPATH}/light"
$IMGDARKPATH = "${IMGPATH}/dark"
$ICONPATH = "${IMGPATH}/icon.ico"

# recommended not to change
$binariesFolderPath = "dist"

# don't touch, this is generated
$osIsARM = $env:PROCESSOR_ARCHITECTURE -match '^arm.*'
$osIs64Bit = [System.Environment]::Is64BitOperatingSystem
# architecture is required for generating of binary name
$osArch = $(
    if ($osIsARM) { 'arm' } else { 'x' }
) + $(
    if ($osIs64Bit) { '64' } elseif (-Not $osIsARM) { '86' }
) # = x86 | x64 | arm | arm64
$binaryName = "$($NAME.replace(' ', '_'))-${osArch}"

# Former compiler: pyinstaller build command

# # create temp files
# $pyinstallerVersionYAML = "metadata.yml"
# @"
# Version: ${VERSION}
# CompanyName: 
# FileDescription: ${DESCRIPTION}
# InternalName: ${NAME}
# LegalCopyright: 
# OriginalFilename: ${binaryName}.exe
# ProductName: ${NAME}
# Translation:
#   - langID: 0
#     charsetID: 1200
#   - langID: 1033
#     charsetID: 1252
# "@ | Out-File $pyinstallerVersionYAML -Encoding UTF8
# $pyinstallerFileVersionINFO = "file_version_info.txt"
# create-version-file $pyinstallerVersionYAML --outfile $pyinstallerFileVersionINFO
#
# pyinstaller main.py --onefile --clean --noconfirm \
#   --windowed \
#   --collect-all sv_ttk \
#   --add-data="utils.py;." \
#   --add-data="${IMGLIGHTPATH}/*;${IMGLIGHTPATH}/" \
#   --add-data="${IMGDARKPATH}/*;${IMGDARKPATH}/" \
#   --add-data="${ICONPATH};${IMGPATH}/" \
#   --version-file "${pyinstallerFileVersionINFO}" \
#   --name="${NAME}" \
#   --icon="${ICONPATH}"
# # remove temp files
# rm -f $pyinstallerVersionYAML
# rm -f $pyinstallerFileVersionINFO

# WARNING: Nuitka requires the non-"Microsoft Store" install of Python to work properly!!!

# Note: This will auto download/cache the required compiler and linker for Nuitka if one or both are not available on the computer
nuitka main.py --onefile --windows-console-mode=attach --remove-output --assume-yes-for-downloads --follow-imports `
  --enable-plugin=tk-inter `
  --windows-icon-from-ico="${ICONPATH}" `
  --include-data-files="${ICONPATH}=${ICONPATH}" `
  --include-data-dir="${IMGLIGHTPATH}=${IMGLIGHTPATH}" `
  --include-data-dir="${IMGDARKPATH}=${IMGDARKPATH}" `
  --file-version="${VERSION}" --product-version="${VERSION}" `
  --file-description="${DESCRIPTION}" `
  --product-name="${NAME}" `
  --output-filename="${binaryName}" `
  --output-dir="${binariesFolderPath}"

deactivate
