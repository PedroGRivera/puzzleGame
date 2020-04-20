import os
import tkinter as tk
import random
import pickle
from tkinter import filedialog, Text, simpledialog
from PIL import Image, ImageTk

class Piece:
    label = ''      #Cropped image
    curX = ''       #Current X (row) position
    curY = ''       #Current Y (column) position
    finX = ''       #Final X position
    finY = ''       #final Y position

class Puzzle:
    pieces = []     #List of pieces
    dimension = ''  #Number of rows and columns
    filepath = ''   #Filepath of the initial image

root = tk.Tk()

dimension = simpledialog.askinteger("Input", "What size grid do you want?", parent=root, minvalue = 0, maxvalue = 6)
filepath = filedialog.askopenfilename()

game = Puzzle()
game.dimension = dimension
game.filepath = filepath

#Open the starting image
image = Image.open(game.filepath)

width = image.width / game.dimension
height = image.height / game.dimension

def generatePuzzle(puzzle):
    print("Generating puzzle pieces")
    for i in range(puzzle.dimension): #row
        for j in range(puzzle.dimension): #column
            tempImage = image.crop((j*width, i*height, (j+1)*width, (i+1)*height))
            tempPhoto = ImageTk.PhotoImage(tempImage)
            label = tk.Label(master = root, image=tempPhoto, anchor=tk.CENTER)
            label.photo = tempPhoto
            piece = Piece()
            piece.label = label
            piece.finX = i
            piece.finY = j
            print(str(piece.finX) + "," + str(piece.finY))
            puzzle.pieces.append(piece)


def scramblePuzzle(puzzle):
    print("Shuffling puzzle pieces")
    random.shuffle(puzzle) #Pieces shuffled
    #Update current positions
    for i in range(puzzle.dimension):
        for j in range(puzzle.dimension):
            puzzle.pieces[(puzzle.dimension)*i + j].curX = i
            puzzle.pieces[(puzzle.dimension)*i + j].curY = j


def displayPuzzle(puzzle):
    print("Displaying puzzle pieces")
    for i in range(puzzle.dimension):
        for j in range(puzzle.dimension):
            puzzle.pieces[(puzzle.dimension)*i + j].label.place(x=j*(width), y=i*(height))

# def savePuzzle(puzzle):
#     print("Saving data...")
#     pickle.dump(puzzle, str(puzzle.filepath) + ".save")
#     print("Data saved to " + str(puzzle.filepath) + ".save")

#generatePuzzle(game)
#scramblePuzzle(game)
#displayPuzzle(game)
#savePuzzle(game)

root.mainloop()