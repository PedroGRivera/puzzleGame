import os
import tkinter as tk
import random
import pickle
from tkinter import filedialog, Text, simpledialog
from PIL import Image, ImageTk

class Piece:
    def __init__(self):
        self.label = ''
        self.left = ''
        self.upper = ''
        self.right = ''
        self.lower = ''
        self.curX = ''       #Current X (row) position
        self.curY = ''       #Current Y (column) position
        self.finX = ''       #Final X position
        self.finY = ''       #final Y position

class Puzzle:
    def __init__(self):
        self.pieces = []
        self.dimension = 0
        self.filepath = ''
        self.width = ''
        self.height = ''

root = tk.Tk()

dimension = 4 #simpledialog.askinteger("Input", "What size grid do you want?", parent=root, minvalue = 0, maxvalue = 6)
filepath = 'LSU-Logo.png' #filedialog.askopenfilename()

global game
game = Puzzle()
game.dimension = dimension
game.filepath = filepath

#Open the starting image
image = Image.open(game.filepath)

game.width = image.width / game.dimension
game.height = image.height / game.dimension

def generatePuzzle(puzzle):
    print("Generating puzzle pieces")
    for i in range(puzzle.dimension): #row
        for j in range(puzzle.dimension): #column
            piece = Piece()
            (piece.left, piece.upper, piece.right, piece.lower) = (j*puzzle.width, i*puzzle.height, (j+1)*puzzle.width, (i+1)*puzzle.height)
            tempImage = image.crop((piece.left, piece.upper, piece.right, piece.lower))
            tempPhoto = ImageTk.PhotoImage(tempImage)
            label = tk.Label(master = root, image=tempPhoto, anchor=tk.CENTER)
            label.photo = tempPhoto
            piece.label = label
            piece.finX = i
            piece.finY = j
            puzzle.pieces.append(piece)


def scramblePuzzle(puzzle):
    print("Shuffling puzzle pieces")
    random.shuffle(puzzle.pieces) #Pieces shuffled
    #Update current positions
    for i in range(puzzle.dimension):
        for j in range(puzzle.dimension):
            puzzle.pieces[(puzzle.dimension)*i + j].curX = i
            puzzle.pieces[(puzzle.dimension)*i + j].curY = j


def displayPuzzle(puzzle):
    print("Displaying puzzle pieces")
    # for i in range(puzzle.dimension):
    #     for j in range(puzzle.dimension):
    #         puzzle.pieces[(puzzle.dimension)*i + j].label.place(x=j*(width), y=i*(height))

    for i in range (len(puzzle.pieces)):
        puzzle.pieces[i].label.place(x = puzzle.pieces[i].curY*puzzle.width, y=puzzle.pieces[i].curX*puzzle.height)

def savePuzzle(puzzle):
    print("Saving data...")

    for i in range(len(puzzle.pieces)): #clear out pictures since they can't be pickled
        puzzle.pieces[i].label = ''

    file_pi = open(filepath + ".puz", 'wb')
    pickle.dump(puzzle, file_pi)
    print("Data saved")

generatePuzzle(game)
scramblePuzzle(game)
displayPuzzle(game)
savePuzzle(game)

root.mainloop()