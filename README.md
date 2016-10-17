# Classic-Snake-HD
Classic snake game written in Python3 and Pygame.

*Note:
I made this as my first game, mainly to evaluate pygame and to get my head around gamedev. As of now, I'll not continue with pygame for any type of game development as it limited my capabilities a lot of what my original idea was for the game and if I do another game in the future, I'll use a different programming language.*

## Screenshot

![Screenshot of version 1.0](/screenshot.png?raw=true "Screenshot of version 1.0")

## How to install and run

### Windows
Download the zip-package from [CLICK HERE](https://github.com/renegadevi/Classic-Snake-HD/releases), extract it and run the game. It is auto-generated with the tool Pyinstaller and has only been tested on Windows 7 and Windows 10 in a virtual machine. When I tried with Windows 10, you need to have Visual C++ Redistributable installed to fix the common MSVCP110.dll problem.

### macOS
Check so you have Python 3 and pygame installed, then just download the repo and run the main.py script.

```sh
# Install brew
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
# Install python 3
brew install python3
# Install pygame
pip3 install pygame
# Change to downloaded zip/cloned folder
cd ~/Downloads/Classic-Snake-HD-master
# run the game.
python3 main.py
```

### Linux (Ubuntu 16.10)
Has been tested on Ubuntu 16.10. It's very simple, download the zip or clone it,
then open a terminal inside the downloaded folder 'Classic-Snake-HD-master' and
execute these commands.
```sh
sudo apt-get install python3-pip
python3 -m pip install pygame
python3 main.py
```

## Built with Open-source

- Python3 – https://www.python.org
- Pygame – https://github.com/xamox/pygame

## License

This project is licensed under the MIT License - see the LICENSE file for details

### Font

This project uses the font **Bowlby One SC** and is licensed under the SIL Open Font License (OFL).  
