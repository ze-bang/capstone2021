from tkinter import *
from tkinter import ttk, filedialog
from tkinter.filedialog import askdirectory
import os

def createWindow():
    window = Tk()
    window.title("MATHUSLA Timing Measurement GUI")
    w, h = window.winfo_screenwidth(), window.winfo_screenheight()
    window.geometry("{0}x{1}+0+0".format(w, h))
    return window, w, h

def openDirectory(folderPath, cwd):
    folderSelected = askdirectory(initialdir="{}".format(cwd), title="Please select a folder...")
    folderPath.set(folderSelected)

def selectSaveDirectory(window):
    # Set-up
    cwd = os.getcwd()
    folderPath = StringVar()
    folderPath.set(cwd)
    browseLabel = Label(window, text="Data Directory")
    browseEntry = Entry(window, textvariable=folderPath)
    browseButton = Button(window,text="Browse",command=lambda: openDirectory(folderPath, cwd))

    # Locations
    browseEntry.grid(row=0, column=1)
    browseLabel.grid(row=0, column=0)
    browseButton.grid(row=0, column=2)

    return folderPath.get()

