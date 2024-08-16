![image](https://github.com/user-attachments/assets/8a2e4215-93d4-4965-9604-1c49fbc23780)

# Arc Palette

Arc Palette is a community-developed application that applies advanced gradient effects to spaces in the Arc browser.



https://github.com/user-attachments/assets/4941f813-58a0-442c-8528-5540b479c1af




**IMPORTANT: Arc must be closed for changes to take effect. So, either use auto restart or close Arc, apply the theme then reopen Arc**
## Installation

In order to install Arc Palette, simply follow these steps:

### Simple Installation (recommended)
This is the easy version of the installation for users that are not experienced with applications such as Command Prompt or Powershell.

Check the [Releases](https://github.com/neurokitti/Arc_Palette/releases) tab and find your respective executable (where `ARCH` is the architecture of your machine):
- Windows: `Arc_Palette-ARCH.exe`
- Mac: `Arc_Palette-ARCH.dmg` (contains the `Arc Palette.app` executable)
- Linux: *(not supported at this time)*

Place the executable where you want (this does not have to be in the arc folder).

Then, just run the executable (double click on it).

### Script Installation (not recommended)
While this still works for now, it's not recommended now that proper executables are built for each release.

Location of installer scripts:
- Windows: `.\scripts\Win\installer\FULL_SETUP_arc_palette.bat`
- Mac: `./scripts/Mac/installer/FULL_SETUP_arc_palette.command` (note, if you want to run this script in the terminal, run `chmod +x` on the script first)
- Linux: *(not supported at this time)*

Place the script file where you want to install arc palette (this does not have to be in the arc folder).

Then, just run the script file (double click on it).

### Advanced Installation (not recommended for nonprogrammers)
This is version of the installation for more advanced users who know what they are doing when it comes to applications such as Command Prompt and Powershell.

NOTE: Mac users, if you don't already have git installed, you will be prompted to install Xcode, which contains the git program.

1. Download this GitHub repository as a zip and right-click to extract it, or clone it with the commands below:

    ```
    git clone https://github.com/neurokitti/Arc_Palette.git
    cd Arc_Palette
    ```

2. Create a virtual environment:

    ```bat
	:: Windows only
	python -m venv .venv
    call .venv\Scripts\activate
    ```

	```sh
	# Mac only
	python3 -m venv .venv
    source .venv/bin/activate
    ```
 Download https://github.com/neurokitti/Arc_API as a zip and right-click to extract it inside the Arc_Palette folder (rename `Arc_API-main` folder to `Arc_API`), or clone it with the commands below:
   ```
   git clone https://github.com/neurokitti/Arc_API.git
   ```

3. Install the required packages from `requirements.txt` and `requirements-arc-api`:

    ```bat
    :: Windows only
    pip install -r requirements.txt
    pip install -r requirements-win.txt
    pip install -r Arc_API\requirements-arc-api.txt
    ```

    ```sh
    # Mac only
    pip3 install -r requirements.txt
    pip3 install -r requirements-mac.txt
    pip3 install -r Arc_API/requirements-arc-api.txt
    ```

## Usage

You can run the program by either executing the `run_arc_palette` script file or using Python in the terminal.

Location of scripts:
- Windows: `.\scripts\Win\run_arc_palette.bat`
- Mac: `./scripts/Mac/run_arc_palette.command` (note, if you want to run this script in the terminal, run `chmod +x` on the script first)

Using Python in the terminal:

```bat
REM Windows only
call .venv\Scripts\activate
python main.py
```

```sh
# Mac only
source .venv/bin/activate
python3 main.py
```

### Advanced Build executables
If you wish to compile the executables yourself, there are scripts with the pyinstaller command already setup.

However, you must make sure that you've already done a full setup, either from **Script Installation** or from **Advanced Installation**.

Then, run the respective script file for building the executable:
- Windows: `scripts\Win\build\BUILD_BINARY_WINDOWS.ps1`
 - note, if you want to run this script in the terminal, run:
   `powershell.exe -ExecutionPolicy Bypass -File .\scripts\Win\build\BUILD_BINARY_WINDOWS.ps1`
- Mac: `scripts/Mac/build/BUILD_BINARY_MAC.command`
 - note, if you want to run this script in the terminal, run:
   `chmod +x scripts/Mac/build/BUILD_BINARY_MAC.command; ./scripts/Mac/build/BUILD_BINARY_MAC.command`

After it completes, if successful, there should be a `dist` folder created with the executable inside (where `ARCH` is the architecture of your machine):
- Windows: `dist\Arc_Palette-ARCH.exe`
- Mac: `dist/Arc_Palette-ARCH.dmg` (contains the `Arc Palette.app` executable)

### Credits:

* **Henson Liga** - *Lead Developer and Creator* - [neurokitti](https://github.com/neurokitti)

* **ash.meow** - *Backend Developer (JSON Support)* - [No GitHub Profile]

* **Valkryx** - *Frontend Developer* - [valk_ryx](https://github.com/valk-ryx)

* **Andrew Larson** - *Hobbyist Developer* - [Andrew-J-Larson](https://github.com/Andrew-J-Larson)
