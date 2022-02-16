from tkinter import *
import tkinter.messagebox as tkmb

fenetre = Tk()

def clavier(event):
	global coords

	touche = event.keysym

	if touche == "Up":
		coords = (coords[0], coords[1] - 10)
	if touche == "Down":
		coords = (coords[0], coords[1] + 10)
	if touche == "Right":
		coords = (coords[0] + 10, coords[1])
	if touche == "Left":
		coords = (coords[0] - 10, coords[1])

	canvas.coords(rectangle, coords[0], coords[1], coords[0] + 25, coords[1] + 25)

canvas = Canvas(fenetre, width=250, height=250, bg='ivory')

coords = (0, 0)

rectangle = canvas.create_rectangle(0, 0, 25, 25, fill='violet')

canvas.focus_set()
canvas.bind("<Key>", clavier)
canvas.pack()

fenetre.mainloop()