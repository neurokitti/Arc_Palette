# Arc Palette

Arc Palette is a community-developed application that applies gradient effects similar to the ones seen on the macOS version of Arc on Windows

https://github.com/user-attachments/assets/131b40f2-f340-43f9-9c3c-3024be636a65

## Installation

In order to install Arc Palette, simply follow these steps:

### Simple Installation
This is the easy version of the installation for users that are not experienced with applications such as Command Prompt or Powershell.

1. Download the file in this repo named "setup.bat"

2. Open the "setup.bat" file (if it gives a warning, simply click "More info" and "Run anyway)

3. After running the batch file, you should have a window open with the Arc Palette application, you are now ready to go!

OR

### Advanced Installation
This is version of the installation for more advanced users who know what they are doing when it comes to applications such as Command Prompt and Powershell.
   
1. Clone the GitHub repository:

    ```bash
    git clone https://github.com/neurokitti/arc_gradient.git
    cd arc_gradient
    ```

2. Create a virtual environment:

    ```bash
    python -m venv myenv
    myenv\Scripts\activate  # On Windows
    # or
    source myenv/bin/activate  # On macOS/Linux
    ```

3. Install the required packages from `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

**Note:** For the best experience, make sure your Windows wallpaper settings are set to "Stretch," Arc is set to "Mica," and the theme is set to "Transparent."

![Arc Gradient Settings](https://github.com/user-attachments/assets/0a4e5dfa-b175-4b3e-b760-b2367121e7d1)

## Usage

You can run the program by either executing the **run.bat** file or using Python in the terminal:

```bash
python main.py
```

## Important Information

This program achieves its effects by changing your Windows wallpaper. However, you can still maintain your wallpaper using either Wallpaper Engine or the free and open-source alternative, [Lively Wallpaper](https://github.com/rocksdanister/lively).
