import os
import random
import pickle
import tkinter as tk
from tkinter import filedialog, Text, simpledialog
import atexit
import math
from PIL import Image, ImageTk


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
xlFont = ("Arial", 30)
pieces = 2
game = None
image = ""
selections = []



################################   create canvas  ################################
can = tk.Canvas(master=window, width=750, height=750, bg=bg)
can.pack(fill=tk.BOTH, side=tk.LEFT,expand=True)


####################################################################################################################################################################
##############################################################################backend###############################################################################
####################################################################################################################################################################

class Piece:
    def __init__(self):
        self.label = ''     #label holds the puzzle piece itself, may need to change this to button if we use buttons later
        self.left = ''      #left, upper, right, lower are needed to crop the piece
        self.upper = ''
        self.right = ''
        self.lower = ''
        self.curX = ''       #Current X (row) position
        self.curY = ''       #Current Y (column) position
        self.finX = ''       #Final X position
        self.finY = ''       #final Y position

class Puzzle:
    def __init__(self):
        self.pieces = []    #list of all puzzle pieces
        self.dimension = 0  #puzzle dimensions set by the user
        self.filepath = ''  #location of the base image
        self.width = ''     #widht and height, needed to generate piece dimensions
        self.height = ''

def generatePuzzle(puzzle):
    global pieces
    global image
    puzzle.dimension = int(math.sqrt(pieces)) #simpledialog.askinteger("Input", "What size grid do you want?", parent=root, minvalue = 0, maxvalue = 6)
    puzzle.filepath  = image   #filedialog.askopenfilename()
    image = Image.open(puzzle.filepath)
    puzzle.width = image.width / puzzle.dimension
    puzzle.height = image.height / puzzle.dimension
    generatePieces(puzzle, image)

def addSelection(x):
    global selections
    global game
    selections.append(x)
    if(len(selections) >= 2):
        a = selections[0]
        b = selections[1]
        selections = []

        print(str(game.pieces[(game.dimension)*a[0] + a[1]].curX) + " : " + str(game.pieces[(game.dimension)*a[0] + a[1]].curY) + "  " + str(b) )
        print(str(game.pieces[(game.dimension)*b[0] + b[1]].curX) + " : " + str(game.pieces[(game.dimension)*b[0] + b[1]].curY) + "  " + str(a))

        game.pieces[(game.dimension)*a[0] + a[1]].curX = b[0]
        game.pieces[(game.dimension)*a[0] + a[1]].curY = b[1]
        game.pieces[(game.dimension)*b[0] + b[1]].curX = a[0]
        game.pieces[(game.dimension)*b[0] + b[1]].curY = a[1]
        game.pieces[(game.dimension)*a[0] + a[1]].label.configure(command=lambda i=b[0],j=b[1]: addSelection([i,j]))
        game.pieces[(game.dimension)*b[0] + b[1]].label.configure(command=lambda i=a[0],j=a[1]: addSelection([i,j]))
        hold = Piece()
        hold = game.pieces[(game.dimension)*a[0] + a[1]]
        game.pieces[(game.dimension)*a[0] + a[1]] = game.pieces[(game.dimension)*b[0] + b[1]]
        game.pieces[(game.dimension)*b[0] + b[1]] = hold

        
        print(str(game.pieces[(game.dimension)*a[0] + a[1]].curX) + " : " + str(game.pieces[(game.dimension)*a[0] + a[1]].curY) )
        print(str(game.pieces[(game.dimension)*b[0] + b[1]].curX) + " : " + str(game.pieces[(game.dimension)*b[0] + b[1]].curY) )

        if(validatePuzzle(game)):
            for i in range (len(game.pieces)):
                try:
                    game.pieces[i].label.place_forget()
                except:
                    pass
            elems['congrats'] = tk.Label(master=window, text="Puzzle Complete!", anchor=tk.CENTER, font=xlFont, bg=bg, fg=fg)
            elems['congrats'].place(relwidth=0.8,relheight=0.25,relx=0.1,rely=0.4)
        else:
            gamePage()

def addSelectionLoad(x):
    global game
    i = int(x / game.dimension)
    j = int(x % game.dimension)
    addSelection([i,j])

def generatePieces(puzzle, image):
    print("Generating puzzle pieces")
    for i in range(puzzle.dimension): #row
        for j in range(puzzle.dimension): #column
            piece = Piece()
            (piece.left, piece.upper, piece.right, piece.lower) = (j*puzzle.width, i*puzzle.height, (j+1)*puzzle.width, (i+1)*puzzle.height)
            tempImage = image.crop((piece.left, piece.upper, piece.right, piece.lower))
            tempPhoto = ImageTk.PhotoImage(tempImage)

            label = tk.Button(master = window, image=tempPhoto, anchor=tk.CENTER, command=lambda i=i,j=j: addSelection([i,j]))
            label.photo = tempPhoto
            piece.label = label
            piece.finX = i
            piece.curX = i
            piece.finY = j
            piece.curY = j
            puzzle.pieces.append(piece)

def scramblePuzzle(puzzle):
    print("Shuffling puzzle pieces")
    random.shuffle(puzzle.pieces) #Pieces shuffled
    #Update current positions
    for i in range(puzzle.dimension):
        for j in range(puzzle.dimension):
            puzzle.pieces[(puzzle.dimension)*i + j].curX = i
            puzzle.pieces[(puzzle.dimension)*i + j].curY = j
            puzzle.pieces[(puzzle.dimension)*i + j].label.configure(command=lambda i=i,j=j: addSelection([i,j]))

#This could use some work, some pieces kinda clip each other
# def displayPuzzle(puzzle):
#     print("Displaying puzzle pieces")
#     for i in range (len(puzzle.pieces)):
#         puzzle.pieces[i].label.place(x = puzzle.pieces[i].curY*puzzle.width, y=puzzle.pieces[i].curX*puzzle.height)

def savePuzzle(puzzle):
    for i in range (len(game.pieces)):
            try:
                game.pieces[i].label.place_forget()
            except:
                print("piece kill fail: " + str(i))
    print("Saving data...")
    for i in range(len(puzzle.pieces)): #clear out pictures since they can't be pickled
        puzzle.pieces[i].label = ''
    file_pi = open(puzzle.filepath + ".puz", 'wb')
    pickle.dump(puzzle, file_pi)
    print("Data saved")

#Might be an issue here with the way I wrote it syntactically. Logically it works
def loadPuzzle(filepath):
    global game

    file_pi = open(filepath, 'rb')
    game = pickle.load(file_pi)
    image = Image.open(game.filepath)

    for i in range(len(game.pieces)): #remake pictures from dimensions
        tempImage = image.crop((game.pieces[i].left, game.pieces[i].upper, game.pieces[i].right, game.pieces[i].lower))
        tempPhoto = ImageTk.PhotoImage(tempImage)
        label = tk.Button(master = window, image=tempPhoto, anchor=tk.CENTER, command=lambda i=i: addSelectionLoad(i))
        label.photo = tempPhoto
        game.pieces[i].label = label

    print("Puzzle save data opened")
    print(game.pieces)
    gamePage()

#Checks if puzzle is finished or not. Returns bool
def validatePuzzle(puzzle):
    for i in range(len(puzzle.pieces) - 1):
        if ((puzzle.pieces[i].curX != puzzle.pieces[i].finX) or (puzzle.pieces[i].curY != puzzle.pieces[i].finY)):
            return False
    return True

#Function calls to make sure the above all works
# game = Puzzle()
# generatePuzzle(game)
# scramblePuzzle(game)
# displayPuzzle(game)
# savePuzzle(game)
# root.mainloop()

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
    global game
    pieces = int(elems['countEntry'].get())
    if pieces > 0 and not isinstance(math.sqrt(pieces), int):
        pieces = math.ceil(math.sqrt(pieces))**2
    #print(pieces)
    game = Puzzle()
    generatePuzzle(game)
    scramblePuzzle(game)
    gamePage()

################################ load image file  ################################
def newGameFun():
    #print("new game")
    global image
    newName = ""
    newName = tk.filedialog.askopenfilename(initialdir=".")
    newGamePageTwo()
    image = newName

################################select saved state################################
def loadGameFun():
    #print("load game")
    loadName = ""
    loadName = tk.filedialog.askopenfilename(initialdir=".")
    loadPuzzle(loadName)

####################################save state####################################
def saveState():
    global game
    #print("saving")
    savePuzzle(game)
    loadMain()

####################################################################################################################################################################
###############################################################################pages################################################################################
####################################################################################################################################################################

################################    game page     ################################
def gamePage():
    global elems
    global game
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

    for i in range (len(game.pieces)):
        try:
            game.pieces[i].label.place_forget()
        except:
            pass
    for i in range (len(game.pieces)):
        game.pieces[i].label.place(x = game.pieces[i].curY*game.width+100, y=game.pieces[i].curX*game.height+100)
    

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
    global game
    for key in elems:
        try:
            elems[key].place_forget()
        except:
            print("elem kill fail: " + key)
    try:
        print(game.pieces)
        for i in range (len(game.pieces)):
            try:
                game.pieces[i].label.place_forget()
            except:
                print("piece kill fail: " + str(i))
    except: pass
    elems.clear()
    elems['title']    = tk.Label(master=window, text="Puzzle Creator", anchor=tk.CENTER, font=mainFont, bg=bg, fg=fg)
    elems['title'].place(relwidth=0.8,relheight=0.1,relx=0.1,rely=0.2)
    elems['newGame']  = tk.Button(master=window, text="Start a new game", anchor=tk.CENTER, font=mainFont, bg=bg, fg=fg, activebackground=selCol, command=newGameFun)
    elems['newGame'].place(relwidth=0.5,relheight=0.1,relx=0.25,rely=0.4)
    elems['loadGame'] = tk.Button(master=window, text="Load a saved game", anchor=tk.CENTER, font=mainFont, bg=bg, fg=fg, activebackground=selCol, command=lambda: loadGameFun())
    elems['loadGame'].place(relwidth=0.5,relheight=0.1,relx=0.25,rely=0.6)
    elems['quitGame'] = tk.Button(master=window, text="Quit", anchor=tk.CENTER, font=mainFont, bg=bg, fg=fg, activebackground=selCol, command=endFun)
    elems['quitGame'].place(relwidth=0.5,relheight=0.1,relx=0.25,rely=0.8)


################################    main calls    ################################
loadMain()
window.mainloop()


