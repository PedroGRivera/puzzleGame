import pickle
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

def displayPuzzle(puzzle):
    print("Displaying puzzle pieces")

    for i in range (len(puzzle.pieces)):
        puzzle.pieces[i].label.place(x = puzzle.pieces[i].curY*puzzle.width, y=puzzle.pieces[i].curX*puzzle.height) 

def loadPuzzle():
    file_pi = open(filepath + ".puz", 'rb')
    global puzzle 
    puzzle = pickle.load(file_pi)
    image = Image.open(puzzle.filepath)

    for i in range(len(puzzle.pieces)): #remake pictures from dimensions
        tempImage = image.crop((puzzle.pieces[i].left, puzzle.pieces[i].upper, puzzle.pieces[i].right, puzzle.pieces[i].lower))
        tempPhoto = ImageTk.PhotoImage(tempImage)
        label = tk.Label(master = root, image=tempPhoto, anchor=tk.CENTER)
        label.photo = tempPhoto
        puzzle.pieces[i].label = label

    print("Puzzle save data opened")

root = tk.Tk()

filepath = 'LSU-Logo.png'

loadPuzzle()

displayPuzzle(puzzle)

root.mainloop()