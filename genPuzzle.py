import os
import tkinter as tk
import random
from tkinter import filedialog, Text, simpledialog
from PIL import Image, ImageTk

class Piece:
    label = ''
    currentPos = ''
    finalPos = ''

class Puzzle:
    pieces = []
    dimension = ''
    filepath = ''

root = tk.Tk()

dimension = simpledialog.askinteger("Input", "What size grid do you want?", parent=root, minvalue = 0, maxvalue = 6)
filepath = tk.filedialog.askopenfilename(initialdir=".")

game = Puzzle()
game.dimension = dimension
game.filepath = filepath

width = image.width / dimension
height = image.height / dimension

#Open the starting image
image = Image.open(game.filepath)

print("Generating puzzle pieces")
for i in range(game.dimension): #row
    for j in range(game.dimension): #column
        tempImage = image.crop((j*width, i*height, (j+1)*width, (i+1)*height))
        tempPhoto = ImageTk.PhotoImage(tempImage)
        label = tk.Label(master = root, image=tempPhoto, anchor=tk.CENTER)
        label.photo = tempPhoto
        piece = Piece()
        piece.label = label
        piece.finalPos = str(i) + "," +str(j)
        print(piece.finalPos)
        game.pieces.append(piece)

print("Shuffling puzzle pieces")
random.shuffle(game.pieces)

print("Displaying puzzle pieces")
for i in range(game.dimension):
    for j in range(game.dimension):
        print("Current pos: " + str(i) + "," +str(j))
        print("Final pos: " + game.pieces[(game.dimension)*i + j].finalPos)
        game.pieces[(game.dimension)*i + j].label.place(x=j*(width), y=i*(height))

root.mainloop()