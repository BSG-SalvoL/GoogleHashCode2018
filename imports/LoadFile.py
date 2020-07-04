from tkinter import *
from tkinter.filedialog import askopenfilename as openfile
import sys


def loadfile():
    path = openfile()
    root = Tk()
    root.withdraw()
    try:
        file = open(path, "rt")
    except IOError:
        print("Error Opening: ", path)
        sys.exit(-1)
    else:
        return file


def loadinput():
    cont = 0
    mappa = ""
    rides = []
    file = loadfile()
    for line in file:
        if cont == 0:
            mappa = line
        else:
            rides.append(line)
        cont += 1
    file.close()
    return file.name, mappa, rides
