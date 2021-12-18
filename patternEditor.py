

import sys
import time
import sys

if (sys.version_info.major != 3):
	sys.exit('WARNING: Only tested in Python 3.x')

try:
	import tkinter
	from tkinter import *
	from tkinter import messagebox
	# from tkinter.tix import *			# tooltips	# doesn't work 
except ImportError:
    sys.exit('Please run `pip3 install --user tkinter` to run CozmoCommander') 

try:
	import argparse
except ImportError:
	sys.exit('Please run `pip3 install --user argparse` to run CozmoCommander') 

#------------------------------------------------------------------------------
def rectCoords (row, col):
	x1 = marginWidth + col * (marginWidth + squareSize)
	y1 = marginWidth + row * (marginWidth + squareSize)
	x2 = x1 + squareSize
	y2 = y1 + squareSize
	return ((x1,y1,x2,y2))
#------------------------------------------------------------------------------
def findRect(x,y):

	found = (-1,-1)
	for row in range (8):
		for col in range (8):
			(x1,y1,x2,y2) = rectCoords (row, col)
			if (x > x1) and (y > y1) and (x < x2) and (y < y2):
				found = (row,col)
				
	return (found)
#------------------------------------------------------------------------------
def clicked (event):
	found = findRect (event.x, event.y)
	# print (found)
	(row,col) = found
	index = row * 8 + col
	if (brush == -1):
		color = colors [index]
		color = color + 1
		color = color % 4
		colors [index] = color
		colorName = colorNames[color]
	else:
		colors [index] = brush
		colorName = colorNames[brush]
	MapCanvas.create_rectangle (rectCoords (row, col), fill = colorName)
#------------------------------------------------------------------------------
def buttonColor (myColor):
	global brush
	brush = myColor
#------------------------------------------------------------------------------
def printResult():
	global colors
	global colorChars
	pattern = ""
	for index in range (64):
		number = colors[index]
		pattern = pattern + colorChars[number]

	print (pattern)
#------------------------------------------------------------------------------
def findInArray (array, toFind):
	found = False
	position = -1
	for index1 in range(len(array)):
		if toFind == array[index1]:
			position = index1
	
	return position
#------------------------------------------------------------------------------


# some definitions 
colorNames = ["black", "red", "blue", "#FFCCFF"]
colorChars = ["0", "r", "b", "p"]
colors = ([0] * 8) * 8
squareSize = 50
marginWidth = 10
frameHeight = 100
brush = 1

# see if we got a parameter and convert the string back to array
if len(sys.argv) > 1:
	index = 0
	colorString = sys.argv[1]
	for colorChar in colorString:
		temp = findInArray (colorChars, colorChar)
		if (temp != -1):
			colors[index] = temp 
			# print (colorChars[colors[index]], end = '')
		index = index +1
	print ("")

# set up the window
WindowWidth = 8*squareSize + 9*marginWidth
WindowHeight = WindowWidth + frameHeight

top = tkinter.Tk()
top.title("RMTT pattern editor")
top.geometry(str (WindowWidth) + "x" + str (WindowHeight + 10))
buttonWindow = Frame (top, width = WindowWidth, height = frameHeight)
buttonWindow.pack(side = TOP)
MapCanvas = Canvas (top, width=WindowWidth, height=WindowHeight)
MapCanvas.pack(side = TOP)
MapCanvas.bind ('<Button-1>', clicked)

# define some buttons

bButtonBlack = Button(buttonWindow, text=colorNames[0], bg = colorNames[0], fg = "white", command= lambda: buttonColor (0))
bButtonBlack.pack(side = LEFT)

bButtonRed = Button(buttonWindow, text=colorNames[1], bg = colorNames[1], fg = "white", command= lambda: buttonColor (1))
bButtonRed.pack(side = LEFT)

bButtonBlue = Button(buttonWindow, text=colorNames[2], bg = colorNames[2], fg = "white", command= lambda: buttonColor (2))
bButtonBlue.pack(side = LEFT)

bButtonPurple = Button(buttonWindow, text="purple", bg = colorNames[3], command= lambda: buttonColor (3))
bButtonPurple.pack(side = LEFT)

bButtonSwitch = Button(buttonWindow, text="switch", command= lambda: buttonColor (-1))
bButtonSwitch.pack(side = LEFT)

bButtonPrint = Button(buttonWindow, text="print", command= printResult)
bButtonPrint.pack(side = LEFT)

# draw squares
squares = []
count = 0
for row in range (8):
	y = row * marginWidth
	for col in range (8):
		
		square = MapCanvas.create_rectangle (rectCoords (row, col), fill = colorNames[colors[count]])
		squares.append (square)
		count = count + 1
		

# show the window
top.mainloop()

printResult()