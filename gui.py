import os
import tkinter as tk
from tkinter import filedialog, Text
import atexit

window = tk.Tk()

################################ global variables ################################
#page definitions
title = None
newGame = None
loadGame = None
quitGame = None
countMessage = None
submitCount = None
countEntry = None
pieces = 2

#background color
bg = "#00ffb1"
#text color
fg = "#4a4849"
#selected color 
selCol = "#2b8c6f"
#font
mainFont = ("Arial", 25)
smallFont = ("Arial", 18)

################################callback functions################################
def submitCountFun():
    global countEntry
    global pieces
    pieces = int(countEntry.get())
    if pieces > 0 and pieces % 2 != 0:
        pieces += 1
    print(pieces)
def newGamePageTwo():
    global newGame
    global loadGame
    global countMessage
    global pieces
    global submitCount
    global countEntry
    newGame.place_forget()
    loadGame.place_forget()
    countMessage = tk.Label(master=window, text="Please enter the number of pieces\n you would like (must be even)", anchor=tk.CENTER, font=smallFont, bg=bg, fg=fg)
    countMessage.place(relwidth=0.8,relheight=0.1,relx=0.1,rely=0.3)
    countEntry = tk.Entry(master=window, font=smallFont)
    countEntry.place(relwidth=0.5,relheight=0.05,relx=0.25,rely=0.4)
    submitCount = tk.Button(master=window, text="Submit", anchor=tk.CENTER, font=mainFont, bg=bg, fg=fg, activebackground=selCol, command=submitCountFun)
    submitCount.place(relwidth=0.5,relheight=0.1,relx=0.25,rely=0.6)

def newGameFun():
    print("new game")
    newName = ""
    newName = tk.filedialog.askopenfilename(initialdir=".")
    print(newName)
    #send to backend to generate image
    newGamePageTwo()
    
def loadGameFun():
    print("load game")
    loadName = ""
    loadName = tk.filedialog.askopenfilename(initialdir=".")
    print(loadName)
    #send to backend to load in image

def endFun():
    global window
    try:
        window.destroy()
    except: pass
    try:
        exit()
    except: pass

atexit.register(endFun)


################################   create canvas  ################################
can = tk.Canvas(master=window, width=750, height=750, bg=bg)
can.pack(fill=tk.BOTH, side=tk.LEFT,expand=True)

################################    main page     ################################
def loadMain():
    global title
    global newGame
    global loadGame
    global quitGame
    title = tk.Label(master=window, text="Puzzle Creator", anchor=tk.CENTER, font=mainFont, bg=bg, fg=fg)
    title.place(relwidth=0.8,relheight=0.1,relx=0.1,rely=0.2)
    newGame = tk.Button(master=window, text="Start a new game", anchor=tk.CENTER, font=mainFont, bg=bg, fg=fg, activebackground=selCol, command=newGameFun)
    newGame.place(relwidth=0.5,relheight=0.1,relx=0.25,rely=0.4)
    loadGame = tk.Button(master=window, text="Load a saved game", anchor=tk.CENTER, font=mainFont, bg=bg, fg=fg, activebackground=selCol, command=loadGameFun)
    loadGame.place(relwidth=0.5,relheight=0.1,relx=0.25,rely=0.6)
    quitGame = tk.Button(master=window, text="Quit", anchor=tk.CENTER, font=mainFont, bg=bg, fg=fg, activebackground=selCol, command=endFun)
    quitGame.place(relwidth=0.5,relheight=0.1,relx=0.25,rely=0.8)




loadMain()


window.mainloop()