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
LARGEUR=752
HAUTEUR=500

score= Label(mw, text='score : ')
score.grid(row=0, column=0, sticky='W')
life= Label(mw, text='lifes : ')
life.grid(row=0, column=8, sticky='N')
photo=PhotoImage(file="fond.gif")
canvas1= Canvas(mw, width=752, height= 500, bg='white')
imagefond= canvas1.create_image(377,251, image=photo)
canvas1.grid(row=1, column=0, rowspan=5, columnspan=10, sticky='W')


def rejouer():
    DeplacerAlien()


buttonRejouer = Button(mw, text='Rejouer', command=rejouer)# fonction qui permet de relancer une partie)
buttonRejouer.grid(row=2,column=10, sticky='E')
   
X=LARGEUR
Y=HAUTEUR
RAYON = 15 #rayon de la balle
distance_alien=5

vitesse = 5
DX = vitesse

def DeplacerAlien():
    """ D�placement d'un alien """
    global X,Y,DX,RAYON, LARGEUR,HAUTEUR
    # rebond a droite
    if X+RAYON+DX > LARGEUR:
        X = (2* LARGEUR-RAYON)-X
        DX = -DX    
    # rebond a gauche
    if X-RAYON+DX < 0:
        Y=Y+100
        X = 2*RAYON-X
        DX = -DX
        if Y>900:
            verif=askokcancel(title='Partie terminé', message=' La partie est terminé')
            if verif==True:
                rejouer()
                
    X = X+DX 
    
    # affichage
    canvas1.coords(Balle,X-RAYON,Y-495,X+RAYON,Y-490)
    # mise � jour toutes les 50 ms
    mw.after(20,DeplacerAlien)
   
Balle = canvas1.create_oval(X-RAYON,500,X+RAYON,500,width=1,outline='red',fill='red')

def DeplacerVaisseau(event):
    global PosXvaisseau, PosYvaisseau
    touche = event.keysym
    #déplacement vers la droite
    if touche == 'Right':
        if PosXvaisseau <= LARGEUR-50:
            PosXvaisseau+=10
            canvas1.coords(Vaisseau,PosXvaisseau+1,HAUTEUR-35)
    #déplacement vers la gauche
    if touche == 'Left':
       if PosXvaisseau >= 50:
            PosXvaisseau-=10
            canvas1.coords(Vaisseau,PosXvaisseau-1,HAUTEUR-35)
            
            
PosXvaisseau=LARGEUR/2
PosYvaisseau=HAUTEUR-35

#Creation du vaisseau
PhotoVaisseau = PhotoImage(file="/home/harou/Documents/CS-DEV/spaceinvaders/_vaisseau.gif")
Vaisseau=canvas1.create_image(PosXvaisseau,765,image = PhotoVaisseau)
canvas1.focus_set()
canvas1.bind('<Key>', DeplacerVaisseau)            
            

def quitter():
    Verif= askokcancel(title='Quitter', message='voulez vous vraiment quitter?')    
    if Verif == True:
        command=mw.destroy()
                       
buttonQuitt = Button(mw, text="Quitter", fg='red', command= quitter );
buttonQuitt.grid(row=4, column=10, sticky='E')

mw.protocol("WM_DELETE_WINDOW", quitter)


mw.mainloop()