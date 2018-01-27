"""Simple GUI for hashit

This program simulates in what ways you can use hashit
"""
import os
import argparse
import easygui as gui
os.sys.path.insert(0, "../..")
from hashit import new, __algorithms__, __help__, hashFile, check_
from hashit.__main__ import walk

def showhelp():
    gui.buttonbox(__help__, "HASHIT - HELP", choices=["OK"], image="../../icon.png")

def selecthash():
    return gui.choicebox("Select an hash", "HASHIT", __algorithms__)


def writetofile():
    yn = gui.ynbox("Write to file? (Recommended)")
    if yn:
        return gui.filesavebox("Save to:", "HASHIT")
    else:
        return False

def readfromfile():
    return gui.fileopenbox("Read from:", "HASHIT")

def main_():
    COMMANDS = ["hash an file", "hash files from a directory" , "hash all files and folders in a directory", "check a checksum file", "help", "exit"]
    command = gui.choicebox("Select command:", "HASHIT", COMMANDS)

    if command == COMMANDS[0]:
        filename = gui.fileopenbox("Choose a file to hash", "HASHIT")
        hashres = hashFile(filename, new(selecthash()), False)
        file = writetofile()

        gui.msgbox(hashres, "HASHIT")

    elif command == COMMANDS[1]:
        my_path = gui.diropenbox("select directory:", "HASHIT")
        files = [my_path + "/" + f for f in os.listdir(my_path) if os.path.isfile(os.path.join(my_path, f))]
        files_to_hash = gui.multchoicebox("Select files to hash:", "HASHIT", files)
        hasher =  selecthash()
        HASHED = []

        for fname in files_to_hash:
            HASHED.append(str(hashFile(fname, new(hasher), False)) + " " + fname)
        
        file = writetofile()

        if file:
            open(file, "w").write("\n".join(HASHED))
        else:
            gui.msgbox('\n\n'.join(HASHED))

    elif command == COMMANDS[2]:
        my_path = gui.diropenbox("select directory:", "HASHIT")
        files = walk(my_path)
        hasher =  selecthash()
        HASHED = []

        for fname in files:
            HASHED.append(str(hashFile(fname, new(hasher), False)) + " " + fname)
        file = writetofile()

        if file:
            open(file, "w").write("\n".join(HASHED))
        else:
            gui.msgbox('\n\n'.join(HASHED))
    
    elif command == COMMANDS[3]:
        file = readfromfile()
        hasher = new(selecthash())
        DONE = []
        
        for c in check_(file, hasher, open(file, "r").readline(), False, False, False):
            
            if isinstance(c, str):
                gui.exceptionbox("An Error has occured:\n\n        {}".format(c), "HASHIT")
            else:
                if not c["hash_check"]:
                    DONE.append("{}: FAILED".format(c["filename"]))
                else:
                    DONE.append("{}: OK".format(c["filename"]))

        gui.msgbox('\n'.join(DONE))

    elif command == COMMANDS[4]:
        showhelp()

    elif command == COMMANDS[5]:
        exit()

def main():
    while 1:
        try:
            main_()
        except Exception:
            break
    exit()

if __name__ == "__main__":
    main()