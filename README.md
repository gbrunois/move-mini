# Classes and samples for Microbit

This project provides some classes and samples to learn programming a [micro:bit](https://microbit.org/) card with Python 
You can find more resources on 
* https://github.com/microbit-playground
* https://github.com/bbcmicrobit/micropython
* https://microbit-micropython.readthedocs.io/en/latest/

## Prerequisites

### Creating a virtual environment
On Microsoft Windows, we recommand enabling the Windows Subsystem for Linux (WSL) or use Git bash shell

Execute the command : 
```bash
pip install virtualenv
virtualenv venv
source venv/Scripts/activate
```

Note : On Microsoft Windows 10, disable python3 and python application aliases.

More information : https://www.liquidweb.com/kb/how-to-setup-a-python-virtual-environment-on-windows-10/

### Install dependencies

Execute the command : 
```bash
pip install -r requirements.txt
```

## How to test

```bash
python build.py samples/neopixel_random.py
```

