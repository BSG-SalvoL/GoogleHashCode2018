import tkinter as tk
from tkinter.filedialog import asksaveasfilename
import sys


def output_file(output=""):
    path = asksaveasfilename(title='Export Output Filename',
                             defaultextension='.in',
                             filetypes=(("in Files", "*.in"), ("All Files", ".*")))
    root = tk.Tk()
    root.withdraw()
    try:
        file = open(path, "wt")
    except IOError:
        print("Error Opening: ", path)
        sys.exit(-1)
    else:
        file.write(output)
        file.close()


def create_output(cars=[]):
    line = ""
    for car in cars:
        car_num, rides = car.get_taken_rides()
        line += str(car_num) + " "
        for ride in rides:
            line += str(ride) + " "
        line += "\n"
    return line
