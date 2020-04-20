import pickle
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

game = pickle.load()