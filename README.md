# KeepTrackOfEverything
Keep track of where your many things are!

## What is this program?
KeepTrackOfEverything is a program that offers you the ability to create diagrams that represent the phyisical position of objects. In a **Location** you can have multiple **Places**, in a **Place** you can have multiple **Places** and/or **Objects**. You can imagine the diagrams produced by this software as the top view of a storage room with everything labeled.

## How do you run the binaries?
### Linux
After unzipping, you will need to open a terminal, go to the location of the binary, and run the command `chmod +x KeepTrackOfEverything`. Afterwards, you can run the ELF binary through the terminal or by just double-clicking it.

Please note, it might take a little while for the main window to appear.

### Windows
After unzipping the archive which contains the Windows build, you're going to have to right click and open the properties of the executable file. In the properties window, click on the checkbox next to Unblock and hit Ok. Now, you can run the software by just double-clicking the exe.

Please note, it might take a little while for the main window to appear.

### MacOS
After unzipping the app file, you can run the software by right clicking on the app file, selecting Open, and clicking the Open button on the pop-up that appears. Afterwards, you should be able to open the app file by just double-clicking on it.

If the above instructions didn't seem to work for you, try these steps:
1. Open the System Settings.
2. Go to the Privacy & Security section. 
3. Scroll all the way down.
4. You should be able to see the message `"KeepTrackOfEverything_MacOS" was blocked to protect your Mac.` and a button saying Open Anyway. Click the Open Anyway button.
5. Click the Open Anyway button on the pop-up that appears
6. Another pop-up asking for your password will appear. Enter your password and continue.

KeepTrackOfEverything should now be running. Please note, it might take a little while for the main window to appear.

## How to make the executable
### Linux
1. Install all necessary tools
    
    Debian and Debian-based distros:
    * `sudo apt install git python3-full`

    Arch Linux and Arch-based distros:
    * `sudo pacman -S git python`
2. `git clone https://github.com/DevMa7e1/KeepTrackOfEverything.git`
3. `cd KeepTrackOfEverything`
4. `python3 -m venv venv`
5. `source venv/bin/activate` (modify for your shell)
6. `pip install -r requirements.txt`
7. `pip install pyinstaller`
8. `python3 -m PyInstaller -F -n KeepTrackOfEverything main.py --hidden-import='PIL._tkinter_finder' --noconsole --collect-all ttkbootstrap`

The resulting executable can be found in the **dist** folder.

## Windows
1. Install the latest version of Python
2. [Download the source code of KeepTrackOfEverything](https://github.com/DevMa7e1/KeepTrackOfEverything/archive/refs/heads/main.zip)
3. Unzip it and go into the created folder
4. Open a new CMD window
5. Copy the path of the previously opened folder and run the command `cd *your path here*`
6. Run the command `python -m venv venv`
7. Run the command `venv\Scripts\activate`
8. Run the command `pip install -r requirements.txt`
9. Run the command `pip install pyinstaller`
10. Run the command `python -m PyInstaller -F -n KeepTrackOfEverything --noconsole main.py`

The resulting executable can be found in the **dist** folder.

## MacOS
1. [Install Homebrew](https://brew.sh/)
2. Open a terminal window
3. Run the command `brew install git python3 python-tk`
4. Run `git clone https://github.com/DevMa7e1/KeepTrackOfEverything.git`
5. Run `cd KeepTrackOfEverything`
6. Run `python3 -m venv venv`
7. Run `source venv/bin/activate`
8. Run `pip install -r requirements.txt`
9. Run `pip install pyinstaller`
10. Run `python3 -m PyInstaller -F -n KeepTrackOfEverything main.py --noconsole`

The resulting executable can be found in the **dist** folder.