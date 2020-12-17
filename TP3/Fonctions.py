#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""

@author: adrien.covarel , baptiste harou
"""
from tkinter import *
import math,random
LARGEUR = 480
HAUTEUR = 320
RAYON = 15 #rayon de la balle

# position initiale au milieu
X = LARGEUR/2
Y = HAUTEUR/2

# direction 
vitesse = 5
DX = vitesse

def DeplacerAlien():
    """ D�placement d'un alien """
    global X,DX,RAYON, LARGEUR,HAUTEUR
    # rebond a droite
    if X+RAYON+DX > LARGEUR:
        X = (2* LARGEUR-RAYON)-X
        DX = -DX    
    # rebond a gauche
    if X-RAYON+DX < 0:
        X = 2*RAYON-X
        DX = -DX
    X = X+DX  
    # affichage
    Canevas.coords(Balle,X-RAYON,5,X+RAYON,5)
    # mise � jour toutes les 50 ms
    Mafenetre.after(20,DeplacerAlien)  

# Creation de la fen�tre principale
Mafenetre = Tk()
Mafenetre.title("MouvementAlien")

# Creation d'un widget Canvas
Canevas = Canvas(Mafenetre,height = HAUTEUR,width = LARGEUR,bg='black')
Canevas.pack(padx=5,pady=5)
# Creation d'un objet graphique
Balle = Canevas.create_oval(X-RAYON,10,X+RAYON,10,width=1,outline='red',fill='blue')


def DeplacerVaisseau(event):
    global PosXvaisseau, PosYvaisseau
    touche = event.keysym
    #déplacement vers la droite
    if touche == 'Right':
        if PosXvaisseau <= LARGEUR-50:
            PosXvaisseau+=10
            Canevas.coords(Vaisseau,PosXvaisseau+1,HAUTEUR-35)
    #déplacement vers la gauche
    if touche == 'Left':
       if PosXvaisseau >= 50:
            PosXvaisseau-=10
            Canevas.coords(Vaisseau,PosXvaisseau-1,HAUTEUR-35)

PosXvaisseau=LARGEUR/2
PosYvaisseau=HAUTEUR-35

#Creation du vaisseau
PhotoVaisseau = PhotoImage(file="/fs03/share/users/adrien.covarel/home/Documents/DEV-Python/TP3/_vaisseau.gif")
Vaisseau=Canevas.create_image(PosXvaisseau,765,image = PhotoVaisseau)
Canevas.focus_set()
Canevas.bind('<Key>', DeplacerVaisseau)



DeplacerAlien()
Mafenetre.mainloop()

