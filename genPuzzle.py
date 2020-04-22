import os
import tkinter as tk
import random
import pickle
from tkinter import filedialog, Text, simpledialog
from PIL import Image, ImageTk

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

root = tk.Tk()

global game
game = Puzzle()

def generatePuzzle(puzzle):
    puzzle.dimension = simpledialog.askinteger("Input", "What size grid do you want?", parent=root, minvalue = 0, maxvalue = 6)
    puzzle.filepath = filedialog.askopenfilename()
    image = Image.open(puzzle.filepath)
    puzzle.width = image.width / puzzle.dimension
    puzzle.height = image.height / puzzle.dimension
    generatePieces(puzzle, image)

def generatePieces(puzzle, image):
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

#This could use some work, some pieces kinda clip each other
def displayPuzzle(puzzle):
    print("Displaying puzzle pieces")
    for i in range (len(puzzle.pieces)):
        puzzle.pieces[i].label.place(x = puzzle.pieces[i].curY*puzzle.width, y=puzzle.pieces[i].curX*puzzle.height)

def savePuzzle(puzzle):
    print("Saving data...")
    for i in range(len(puzzle.pieces)): #clear out pictures since they can't be pickled
        puzzle.pieces[i].label = ''
    file_pi = open(puzzle.filepath + ".puz", 'wb')
    pickle.dump(puzzle, file_pi)
    print("Data saved")


#Function calls to make sure the above all works
generatePuzzle(game)
scramblePuzzle(game)
displayPuzzle(game)
savePuzzle(game)

root.mainloop()