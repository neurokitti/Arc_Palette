![image](https://github.com/user-attachments/assets/8a2e4215-93d4-4965-9604-1c49fbc23780)

# Arc Palette

Arc Palette is a community-developed application that applies gradient effects similar to the ones seen on the macOS version of Arc on Windows



https://github.com/user-attachments/assets/4941f813-58a0-442c-8528-5540b479c1af




**IMPORTANT: arc must be closed for changes to take effect. so close arc, apply the theme then reopen arc**
## Installation

In order to install Arc Palette, simply follow these steps:

### Simple Installation
This is the easy version of the installation for users that are not experienced with applications such as Command Prompt or Powershell.

Check the [Releases](https://github.com/neurokitti/Arc_Palette/releases) tab, and find your respective installer script:
- Windows: `WINDOWS_arc_palette_full_setup.bat`
- Mac: `MAC_arc_palette_full_setup.command`
- Linux: (not supported at this time)

Place the script file where you want to install arc palette (this does not have to be in the arc folder).

Then, just run the file (double click on it).

### Advanced Installation
This is version of the installation for more advanced users who know what they are doing when it comes to applications such as Command Prompt and Powershell.
   
1. Download this GitHub repository as a zip and right-click to extract it, or clone it with the commands below:

    ```
    git clone https://github.com/neurokitti/Arc_Palette.git
    cd Arc_Palette
    ```

2. Create a virtual environment:

    ```bat
	:: Windows only
	python -m venv .venv
    .venv\Scripts\activate
    ```
	
	```sh
	# Mac/Linux only
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
    pip install -r Arc_API\requirements-arc-api.txt
	```
	
	```sh
	# Mac/Linux only
    pip3 install -r requirements.txt
    pip3 install -r Arc_API/requirements-arc-api.txt
    ```

## Usage

You can run the program by either executing the `run_arc_palette` script file or using Python in the terminal.

Location of script:
- Windows: `.\resources\Windows\run_arc_palette.bat`
- Mac/Linux: `./resources/Mac/run_arc_palette.command`

Using Python in the terminal:

	```bat
	REM Windows only
	.venv\Scripts\activate 
    python main.py
	```

	```sh
	# Mac/Linux only
	source .venv/bin/activate
	python3 main.py
	```
