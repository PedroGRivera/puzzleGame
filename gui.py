import os
import tkinter as tk
from tkinter import filedialog, Text
import atexit
import math

window = tk.Tk()

####################################################################################################################################################################
###############################################################################setup################################################################################
####################################################################################################################################################################

################################ global variables ################################
#page definitions
elems = {'title':None,'newGame':None,'loadGame':None,'quitGame':None,'countMessage':None,'submitCount':None,'countEntry':None}
#background color
bg = "#00ffb1"
#text color
fg = "#4a4849"
#selected color 
selCol = "#2b8c6f"
#fonts
mainFont = ("Arial", 25)
smallFont = ("Arial", 18)

##############################placeholder variables###############################
#these variables should be replaced with the backend code once it has been finished
pieces = 2
game   = []
#game element: {'pos':[],'finish':[],'image':''}
def fillGame():
    global pieces
    global game
    #print(math.sqrt(pieces))
    for i in range(0, int(math.sqrt(pieces))):
        for j in range(0,int(math.sqrt(pieces))):
            game.append({'pos':[i,j],'finish':[i,j],'image':'C:\\Users\\Pedro\\Document\\senior\\spring\\3d\\puzzleGame\\lsu.jpg'})
    # for i in game:
    #     print(i)
            


################################   create canvas  ################################
can = tk.Canvas(master=window, width=750, height=750, bg=bg)
can.pack(fill=tk.BOTH, side=tk.LEFT,expand=True)

####################################################################################################################################################################
#############################################################################functions##############################################################################
####################################################################################################################################################################

################################ page destruction ################################
def endFun():
    global window
    try:
        window.destroy()
    except: pass
    try:
        exit()
    except: pass
atexit.register(endFun)

################################submit piece count################################
def submitCountFun():
    global pieces
    global elems
    pieces = int(elems['countEntry'].get())
    if pieces > 0 and not isinstance(math.sqrt(pieces), int):
        pieces = math.ceil(math.sqrt(pieces))**2
    #print(pieces)
    fillGame()
    gamePage()

################################ load image file  ################################
def newGameFun():
    #print("new game")
    newName = ""
    newName = tk.filedialog.askopenfilename(initialdir=".")
    newGamePageTwo()

################################select saved state################################
def loadGameFun():
    #print("load game")
    loadName = ""
    loadName = tk.filedialog.askopenfilename(initialdir=".")

####################################save state####################################
def saveState():
    #print("saving")
    pass

####################################################################################################################################################################
###############################################################################pages################################################################################
####################################################################################################################################################################

################################    game page     ################################
def gamePage():
    global elems
    for key in elems:
        try:
            elems[key].place_forget()
        except: pass
    elems.clear()
    # for i in elems:
    #     print(i)
    elems['save'] = tk.Button(master=window, font=smallFont, text="Save", bg=bg, fg=fg, activebackground=selCol, command=saveState)
    elems['save'].place(relwidth=0.2,relheight=0.05,relx=0.1,rely=0.005)
    elems['new'] = tk.Button(master=window, font=smallFont, text="New", bg=bg, fg=fg, activebackground=selCol, command=loadMain)
    elems['new'].place(relwidth=0.2,relheight=0.05,relx=0.4,rely=0.005)
    elems['quit'] = tk.Button(master=window, font=smallFont, text="Quit", bg=bg, fg=fg, activebackground=selCol, command=endFun)
    elems['quit'].place(relwidth=0.2,relheight=0.05,relx=0.7,rely=0.005)

################################ piece count page ################################
def newGamePageTwo():
    global elems
    elems['newGame'].place_forget()
    elems['loadGame'].place_forget()
    elems['countMessage'] = tk.Label(master=window, text="Please enter the number of pieces\n you would like", anchor=tk.CENTER, font=smallFont, bg=bg, fg=fg)
    elems['countMessage'].place(relwidth=0.8,relheight=0.1,relx=0.1,rely=0.3)
    elems['countEntry'] = tk.Entry(master=window, font=smallFont)
    elems['countEntry'].place(relwidth=0.5,relheight=0.05,relx=0.25,rely=0.4)
    elems['submitCount'] = tk.Button(master=window, text="Submit", anchor=tk.CENTER, font=mainFont, bg=bg, fg=fg, activebackground=selCol, command=submitCountFun)
    elems['submitCount'].place(relwidth=0.5,relheight=0.1,relx=0.25,rely=0.6)

################################    main page     ################################
def loadMain():
    global elems
    for key in elems:
        try:
            elems[key].place_forget()
        except: pass
    elems.clear()
    elems['title']    = tk.Label(master=window, text="Puzzle Creator", anchor=tk.CENTER, font=mainFont, bg=bg, fg=fg)
    elems['title'].place(relwidth=0.8,relheight=0.1,relx=0.1,rely=0.2)
    elems['newGame']  = tk.Button(master=window, text="Start a new game", anchor=tk.CENTER, font=mainFont, bg=bg, fg=fg, activebackground=selCol, command=newGameFun)
    elems['newGame'].place(relwidth=0.5,relheight=0.1,relx=0.25,rely=0.4)
    elems['loadGame'] = tk.Button(master=window, text="Load a saved game", anchor=tk.CENTER, font=mainFont, bg=bg, fg=fg, activebackground=selCol, command=loadGameFun)
    elems['loadGame'].place(relwidth=0.5,relheight=0.1,relx=0.25,rely=0.6)
    elems['quitGame'] = tk.Button(master=window, text="Quit", anchor=tk.CENTER, font=mainFont, bg=bg, fg=fg, activebackground=selCol, command=endFun)
    elems['quitGame'].place(relwidth=0.5,relheight=0.1,relx=0.25,rely=0.8)

################################    main calls    ################################
loadMain()
window.mainloop()