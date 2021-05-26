from tkinter import * 
from Solver import Solver
from Solver import Node
from Solver import Puzzle
import time

global puzzl , t ,j

j=0
fenetre = Tk()

but = [[1,2,3],[4,5,6],[7,8,0]]



board = [[1,2,3],[4,5,6],[7,8,0]]
t = 3;

photos=[]
for i in range(0,9):
	photos.append(PhotoImage(file="./images/"+str(i)+"a.png"))

global listPhotos , listAff
listPhotos = photos[0:9]



can=Canvas( width=150*t,height=150*t,bg='white')
can.pack( side =TOP, padx =20, pady =20)
fenetre['bg']='white'
fenetre.title (' Taquin resolution A*')

puzzl = Puzzle(board,can,listPhotos)
s = Solver(puzzl,fenetre)


def solv1():
	global s1
	s1 =Solver(puzzl,fenetre)
	s1.solve('H1')
	puzzl.board = but

def solv2():
	global solv2
	s2 = Solver(puzzl,fenetre)
	s2.solve('H2')
	puzzl.board = but

def mel():
	global puzzl
	puzzl = puzzl.shuffle()

def melanger():
	print(puzzl.board)

listAff = list([0,1,2,3,4,5,6,7,8])
listAff=[]
for row in board:
    listAff.extend(row)

menubar = Menu(fenetre)
menu = Menu(menubar, tearoff=0)
menu.add_command(label="melanger", command=mel)
menu.add_separator()
menu.add_command(label="H1", command=solv1)
menu.add_separator()
menu.add_command(label="H2", command=solv2)
menu.add_separator()
menu.add_command(label="Quitter", command=fenetre.quit)
menubar.add_cascade(label="Menu", menu=menu)

fenetre.config(menu=menubar)



for k in range(len(listPhotos)) :
    eff = can.create_image((30+ 150*(k % t)), 30+(150*( k // t)), anchor=NW, image=listPhotos[0])
    aff = can.create_image((30+ 150*(k % t)), 30+(150*( k // t)), anchor=NW ,image = listPhotos[listAff[k]])

can.pack()

fenetre.mainloop()