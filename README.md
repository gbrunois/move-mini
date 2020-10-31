# Classes and samples for Microbit

This project provides some classes and samples to learn programming a [micro:bit](https://microbit.org/) card with Python 

You can find more resources on 
* https://github.com/microbit-playground
* https://github.com/bbcmicrobit/micropython
* https://microbit-micropython.readthedocs.io/en/latest/


## Prerequisites

### Recommanded environment

Use Microsoft Visual Studio Code with these extensions:
* [Python] (https://github.com/Microsoft/vscode-python)
* [Device Simulator Express] (https://github.com/microsoft/vscode-python-devicesimulator)

Or use PyCharm with [pseudo-microbit](https://mryslab.github.io/pseudo-microbit/install)

### Creating a virtual environment

#### Windows

On Microsoft Windows, we recommand enabling the Windows Subsystem for Linux (WSL) or use Git bash shell

Execute these commands : 
```bash
pip install virtualenv
virtualenv venv
source venv/Scripts/activate
```

Note : On Microsoft Windows 10, disable python3 and python application aliases.

More information : https://www.liquidweb.com/kb/how-to-setup-a-python-virtual-environment-on-windows-10/

#### Linux
Execute these commands : 
```bash
pip install virtualenv
virtualenv venv
source venv/bin/activate
```

### Install dependencies

Execute the command : 
```bash
pip install -r requirements.txt
```

## How to build and flash

Build and flash

```bash
python build.py <your_program.py>
```

Watch for changes

```bash
python build.py --watch <your_program.py>
```

No flashing

```bash
python build.py --no-flash --output=out <your_program.py>
```

The build program uses [uflash](https://uflash.readthedocs.io/en/latest/) for flashing the BBC micro:bit.
It's not possible to import external python modules with uflash. External files have to be embedded in the main file. For that, you can use this template :

```python
# <Includes>
from external_modules.move_mini import *
# </Includes>
```

All importations between <Includes> tag will be embedded in the main file.

Another solution is to use [microFS](https://microfs.readthedocs.io/en/latest/). The disavantage with this is you neet to put each dependency manually after flashing the micro:bit

### Memory issue

micro:bit have limited memory capacity. Python program should be minified to avoid memory issue. For more information : http://docs.micropython.org/en/latest/reference/constrained.html#flash-memory
