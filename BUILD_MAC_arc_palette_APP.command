#!/bin/zsh

source .venv/bin/activate
pyinstaller -F main.py -n "Arc Palette" --icon="resources/img/icon.ico" --windowed --clean --add-data="resources/img/*:resources/img/" --collect-all sv_ttk
