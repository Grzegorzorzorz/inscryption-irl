# Card pack generator

The aim of this project is to automate the tedious process of taking and
aligning cards on a page for printing. Originally intended for playing
Inscryption IRL with friends, though it's generic enough you should be able
to use it for anything :)

## Installation

I only have a Linux machine, but this project should work on other platforms.
If you need any support, feel free to drop an issue; I'll get back to you
eventually.

### System dependencies

You'll need to install the following for the program to run properly:

| Dependency                                                 | Version      |
| ---------------------------------------------------------- | ------------ |
| [Python](https://www.python.org/downloads/)                | >=`3.7.0`    |
| [ImageMagick](https://imagemagick.org/script/download.php) | >=`7.1.1-25` |

### Setting up the environment

First create a virtual environment:
```bash
python -m venv venv
```

Then enter it:
```bash
source venv/bin/activate
```

Finally, install script dependencies:
```bash
python -m pip install -r requirements.txt
```

You should now be ready to go!

## Usage
