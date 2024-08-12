# Arc Palette

Arc Palette is a community-developed application that applies gradient effects similar to the ones seen on the macOS version of Arc on Windows



https://github.com/user-attachments/assets/63bdb73e-7459-4170-a98f-2b29670de21b



**IMPORTANT: arc must be closed for changes to take effect. so close arc, apply the theme then reopen arc**
## Installation

In order to install Arc Palette, simply follow these steps:

### Simple Installation
This is the easy version of the installation for users that are not experienced with applications such as Command Prompt or Powershell.

1. Download the file in this repo named "full_setup.bat"

2. Open the "full_setup.bat" file in the folder you want the application in (if it gives a warning, simply click "More info" and "Run anyway)

3. After running the batch file, you should have a window open with the Arc Palette application, you are now ready to go!

OR

### Advanced Installation
This is version of the installation for more advanced users who know what they are doing when it comes to applications such as Command Prompt and Powershell.
   
1. Clone the GitHub repository:

    ```
    git clone https://github.com/neurokitti/Arc_Palette.git
    cd Arc_Palette
    ```

2. Create a virtual environment:

    ```
    python -m venv .venv
    .venv\Scripts\activate  # On Windows
    # or
    source .venv/bin/activate  # On macOS/Linux
    ```
 Clone the Arc_API repository:
   ```
   git clone https://github.com/neurokitti/Arc_API.git
   ```

3. Install the required packages from `requirements.txt` and `requirements-arc-api`:

    ```
    pip install -r requirements.txt
    pip install -r Arc_API/requirements-arc-api.txt
    ```

## Usage

You can run the program by either executing the **run.bat** file or using Python in the terminal:

```bash
python main.py
```
