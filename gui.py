from tkinter import *
import guiHelperFunctions as gui

# Create application window
window, w, h = gui.createWindow()
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
leftFrame = Frame(window,bg="BLUE")
rightFrame = Frame(window,bg="RED")
leftFrame.grid(row=0,column=0)
rightFrame.grid(row=0,column=1)

# Create browse button for choosing file save location
folderPath = gui.selectSaveDirectory(leftFrame)

# Main loop to open GUI window
window.mainloop()