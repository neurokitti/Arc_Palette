#Requires -Version 5.1
# You can run this file with the "BUILD_BINARY_WINDOWS.bat" script, or use extract the command from the .bat to use manually to launch this script

# .ps1 files change directory, need to open to directory where script launched from
Set-Location $PSScriptRoot

# Go to repo's root directory where everything is setup
Set-Location ..\..\..

# Activating the virtual environment
. .\.venv\Scripts\activate

# change details here
$NAME = "Arc Palette"
$DESCRIPTION = "Arc Palette is a community-developed application that applies advanced gradient effects to spaces in the Arc browser."
$VERSION = "2.0"
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

# pyinstaller main.py --onefile --clean --noconfirm \
#   --windowed \
#   --collect-all sv_ttk \
#   --add-data="utils.py;." \
#  --add-data="${IMGLIGHTPATH}/*;${IMGLIGHTPATH}/" \
#  --add-data="${IMGDARKPATH}/*;${IMGDARKPATH}/" \
#  --add-data="${ICONPATH};${IMGPATH}/" \
#  --name="${NAME}" \
#  --icon="${ICONPATH}"

# WARNING: Nuitka requires the non-store install of Python to work properly!!!

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
