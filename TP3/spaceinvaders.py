#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 08:40:41 2020

@author: harou
"""

from tkinter import Tk, Label, messagebox, Button, Canvas, PhotoImage, Entry, StringVar
from tkinter.messagebox import askokcancel
mw = Tk()
mw.title('Space Invaders')
mw.geometry('850x500')


score= Label(mw, text='score : ')
score.grid(row=0, column=0, sticky='W')
life= Label(mw, text='lifes : ')
life.grid(row=0, column=8, sticky='N')
photo=PhotoImage(file="fond.gif")
canvas1= Canvas(mw, width=752, height= 500, bg='white')
imagefond= canvas1.create_image(376,250, image=photo)
canvas1.grid(row=1, column=0, rowspan=5, columnspan=10, sticky='W')

buttonRejouer = Button(mw, text='Rejouer', command=mw.destroy)# fonction qui permet de relancer une partie)
buttonRejouer.grid(row=2,column=10, sticky='E')
   

    


def quitter():
    Verif= askokcancel(title='Quitter', message='voulez vous vraiment quitter?')    
    if Verif == True:
        command=mw.destroy()
                       
buttonQuitt = Button(mw, text="Quitter", fg='red', command= quitter );
buttonQuitt.grid(row=4, column=10, sticky='E')

mw.protocol("WM_DELETE_WINDOW", quitter)



mw.mainloop()