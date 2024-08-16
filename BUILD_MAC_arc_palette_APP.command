#!/bin/zsh

source .venv/bin/activate
pyinstaller -F main.py \
  --add-data="hot_fixes/ctk_scale_error.py:hot_fixes/" \
  --add-data="utils.py:." \
  --add-data="resources/img/dark/*:resources/img/dark/" \
  --add-data="resources/img/light/*:resources/img/light/" \
  --add-data="resources/img/icon.ico:resources/img/" \
  --collect-all sv_ttk \
  --name="Arc Palette" \
  --icon="resources/img/icon.ico" \
  --windowed --clean