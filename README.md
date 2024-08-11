# Arc Gradient

Arc Gradient is a community-developed application that applies gradient effects to your Arc browser theme.

https://github.com/user-attachments/assets/131b40f2-f340-43f9-9c3c-3024be636a65

## Installation

To install the Arc Gradient application, follow these steps:

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