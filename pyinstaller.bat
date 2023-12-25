echo off

pip install --upgrade pip
pip install pyinstaller
pip install pyTelegramBotAPI
pip install getpass
pip install PyAutoGUI
pip install psutil
pip install 91act-platform
pip install speedtest
pip install geocoder
pip install subprocess32
pip install opencv-python
pip install pycopy-shutil
|pyinstaller path| -F -w -i logo.ico main.py


rmdir /s /q __pycache__
rmdir /s /q build

:cmd
pause null
