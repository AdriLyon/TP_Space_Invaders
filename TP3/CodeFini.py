# -*- coding: utf-8 -*-
"""

@authors: Adrien COVAREL Baptiste Harou

Le but de ce code sera de faire une interface graphique pour notre jeu de Space Invaders. 
On souhaite diffferentes fonctionnalites mais le but global est de pouvoir controler un vaiseai a l'aide du clavier de tirer sur des aliens
afin de les supprimer un par un, chaque alien tue augmente notre score, on possede trois vies

Etat : Nous avons reussis plusieurs points du projet : l'interface graphique, la creations des aliens dans des listes, le controle du vaisseau (deplacement + tir)
, on a aussi reussi a creer des blocs de defense qui sedetruise au fur et a mesur des tirs aliens.
Nous avons commence la gestion de vaisseau bonus mais n'avons pas eu le temps de terminer, nous n'avons pas bien gerer les nouvelles parties non plus (recommencer une partie)

"""

# Lien GITHub : https://github.com/AdriLyon/TP_Space_Invaders

from tkinter import *
from random import *
from tkinter.messagebox import showinfo, askokcancel

"--------------------------------------FONCTIONS------------------------------------"
   
def deplacerAliens(canevas,listeAliens,photoGameOver, dx=20,dy=40, vitesse=1000):
    # Cette fonction gere le deplacement des ennemis, ol faut que les trois lignes d'alien se deplace de gauche a droite, et qu'a chaque allerou retour
    # ils descendent d'un cran jusqu'a arriver au niveau des blocs de defense du vaisseau

    xPremier = 10000 #xPremier et xDernier representent les positions alien aux extremites
    xDernier = 0
    listeAliens = [ligne for ligne in listeAliens if ligne]
    _, yMin = canevas.coords(listeAliens[-1][0])
    if yMin > 590:
      # Si les aliens arrivent en bas de l'ecran alors la partie est termine
        gameOver()
    for ligne in listeAliens:
        x, _ = canevas.coords(ligne[0])             
        if x < xPremier:
            xPremier = x
        x, _ = canevas.coords(ligne[-1])          
        if x > xDernier:
            xDernier = x
    depVertical = False
    if xPremier <= 40 and dx == -20:              
        dx = 20
        depVertical = True
    if xDernier >= Largeur-40 and dx == 20:       #ces deux if test si une des deux extremite se trouvent au bout de la fenetre horizontalement
        dx =-20                                  #si oui alors on a fait un aller ou un retour donc on active le deplacement vertical pour que le bloc baisse d'un cran
        depVertical = True
    if depVertical:
        if vitesse >= 120:
            vitesse -= 50                       
        for ligne in listeAliens:
            for alien in ligne:
                canevas.move(alien,0,dy)       # on "descend" chaque alien de dy verticalement
    else:
        for ligne in listeAliens:
            for alien in ligne:
                canevas.move(alien,dx,0)        # si on ne baisse pas verticalement alors on les decales horizontalement
    canevas.after(vitesse, lambda: deplacerAliens(canevas,listeAliens,photoGameOver, dx,dy, vitesse))
    
    
def deplacerVaisseau(event):
    #Cette fonction gere le deplacement du vaissea par l'utilisateur, on veut qu'il se deplace a gauche ou a droite avec les touches "fleches" du clavier
    global PosXvaisseau, PosYvaisseau
    touche = event.keysym
    if touche == 'Right':
        if PosXvaisseau <= Largeur-50:                           # Pour aller a droite on test d'abord si le vaisseau n'est pas deja tout a droite (pareil pour la gauche)
            PosXvaisseau += 10
            canevas.coords(Vaisseau,PosXvaisseau+1,Hauteur-35)
    if touche == 'Left':
        if PosXvaisseau >= 50:
            PosXvaisseau -= 10                                    
            canevas.coords(Vaisseau,PosXvaisseau-1,Hauteur-35)
            
    
def tirer(dy,v, missile = None):
    # cette fonction gere le tir de l'utilisateur (vaisseau), on effectue plusieurs test pour s'assurer qu'un tir est deja fini afin de pouvoir en faire un autre

    global PosXvaisseau, PosYvaisseau, tirEnCours, dKill,LX,LY,missileAlien,score,listeAliens
    if not missile and not tirEnCours:
        tirEnCours = True         
        missile = canevas.create_rectangle(PosXvaisseau-3,PosYvaisseau-10,PosXvaisseau+2.2,PosYvaisseau+15,fill = "lime green")
    for i in range(0,11):
        if canevas.coords(missile)[1] <= 0:
            canevas.delete(missile)         # si le missile arrive au bout, on l'efface 
            missile = None
            tirEnCours = False
    for ligne in listeAliens:         
        for alien in ligne :
            x,y = canevas.coords(alien)
            centreMissile = ((PosXvaisseau-3)+(PosXvaisseau+2.2))/2
            if abs(x-centreMissile) <= 22 and abs(y-(canevas.coords(missile)[1])) <= 20:    # si le centre du missile est en contact avec un alien de la liste 
                canevas.delete(missile)                                                 # alors on efface le missile ET l'alien
                missile= None
                tirEnCours = False
                canevas.delete(listeAliens[listeAliens.index(ligne)][ligne.index(alien)])
                ligne.remove(alien)
                score += 10                                                                  # on a alors +10 points par alien elimine
                Texte = Label(fenetre, text = 'Score : '+ str(score))
                Texte.grid(row=0, column=0)
    if abs((canevas.coords(missile)[1]) - canevas.coords(vaisseauBonus)[1]) < 5 and abs((canevas.coords(missile)[0]) - canevas.coords(vaisseauBonus)[0]) < 25:
        canevas.move(vaisseauBonus,0,dKill)
        canevas.delete(missile)                 #si l'on arrive a tirer sur le vaisseau bonus alors on gagne 150 points
        missile = None
        tirEnCours = False 
        score += 150
        Texte = Label(fenetre, text = 'Score : '+ str(score))
        Texte.grid(row = 0, column = 0)
    else:
        canevas.move(missile,0,dy)                      #deppace le missile de "dy"
        canevas.after(v, lambda: tirer(-5,8, missile)) 
        

def tirEnnemi(dy,v,bombe = None):
    # Cette fonction gere les tirs des ennemis, notamment le fait que les tirs des aliens soient aleatoire parmi tout les aliens present
    #  on utilise notre liste d'alien cree plus tot 

    global listeAliens,PosXvaisseau,PosYvaisseau, dKill, vie
    if randint(0, 3) == 0:
        print ("tir")
        alien_aleatoire = choice(listeAliens[-1]) # on choisit au hasard l'alien qui va tirer parmi la liste alien cree plus tot
        PosXalien,PosYalien = canevas.coords(alien_aleatoire)
        boule = canevas.create_oval(PosXalien - 5,PosYalien + 55, PosXalien + 5, PosYalien + 65, fill = "red2")
        deplacerBombe(boule, dy) # on utilise la fonction deplacerBombe a chaque tir pour mettre en mouvement la bombe
    canevas.after(100, lambda: tirEnnemi(-5, 25))   



        

def deplacerBombe(boule, dy):
    # Cette fonction gere le deplacement des bombes tirees par les aliens
    # On gere aussi la perte des vies du vaisseau lorsqu'une bombe le touche
    # elle permet aussi de detecter quand une bombe entre en collision avec un bloc de defense
    # alors ce boc se detruit
    global canevas, vie, PosYvaisseau, PosXvaisseau
    canevas.move(boule, 0, -dy) 
    bx,by,_,_ = canevas.coords(boule)
    if abs(PosXvaisseau - bx) <= 10 and abs(PosYvaisseau - by) <= 20: #Test pour savoir si le vaisseau est touche
        canevas.delete(boule)
        vie -= 1                 #alors la boule est detruite et l'utilisateur perd une vie
        Texte2 = Label(fenetre, text = 'Vies : ' + str(vie))    
        Texte2.grid(row = 0, column = 6)
        if vie == 0:            # si le joueur n'a plus de vies la partie est termine
            gameOver()
    elif by > Hauteur:
        canevas.delete(boule) #Si le tir a traverse l'ecran sans toucher le vaisseau on supprime la boule
    else:
        canevas.after(40, lambda: deplacerBombe(boule, dy))
    for i in range(0,4):     # ce for test pour chaque bloc de defense si la balle de l'utilisateur en touche 1, alors il detruit cette partie du bloc
        if abs((canevas.coords(boule)[1]) - canevas.coords(defensel1[i])[1]) < 30 and abs((canevas.coords(boule)[0]) - canevas.coords(defensel1[i])[0] - 8) < 20:
            canevas.move(defensel1[i],0,dKill)
            canevas.delete(boule)
            boule = None
        elif abs((canevas.coords(boule)[1]) - canevas.coords(defensel2[i])[1]) < 30 and abs((canevas.coords(boule)[0]) - canevas.coords(defensel1[i])[0] - 8) < 20:
            canevas.move(defensel2[i], 0, dKill)
            canevas.delete(boule)
            boule = None 
        elif abs((canevas.coords(boule)[1]) - canevas.coords(defense2l1[i])[1]) < 30 and abs((canevas.coords(boule)[0]) - canevas.coords(defense2l1[i])[0] - 8) < 20:
            canevas.move(defense2l1[i],0,dKill)
            canevas.delete(boule)
            boule = None
        elif abs((canevas.coords(boule)[1]) - canevas.coords(defense2l2[i])[1]) < 30 and abs((canevas.coords(boule)[0]) - canevas.coords(defense2l2[i])[0] - 8) < 20:
            canevas.move(defense2l2[i],0,dKill)
            canevas.delete(boule)
            boule = None 
        elif abs((canevas.coords(boule)[1]) - canevas.coords(defense3l1[i])[1]) < 30 and abs((canevas.coords(boule)[0]) - canevas.coords(defense3l1[i])[0] - 8) < 20:
            canevas.move(defense3l1[i],0,dKill)
            canevas.delete(boule)
            boule = None  
        elif abs((canevas.coords(boule)[1]) - canevas.coords(defense3l2[i])[1]) < 30 and abs((canevas.coords(boule)[0]) - canevas.coords(defense3l2[i])[0] - 8) < 20:
            canevas.move(defense3l2[i],0,dKill)
            canevas.delete(boule)
            boule = None
  
  
def start(canevas,listeAliens,photoGameOver):
    # Cette fonction "lance" le jeu
    global debut

    if not debut:
        deplacerAliens(canevas, listeAliens, photoGameOver)
        canevas.bind('<Key>', deplacerVaisseau)
        canevas.bind('<space>', lambda _: tirer(-40,100)) #l'utlisateur tir a chaque fois qu'il appui sur 
        tirEnnemi(1,5)
        debut = True

def gameOver():
    canevas.delete(ALL)
    canevas.create_image(Largeur/2, Hauteur/2, image = photoGameOver) 

def Quitter():
    Verif  = askokcancel(title = "Quitter", message = "Voulez-vous vraiment quitter ?")
    if Verif == True:
        command = fenetre.destroy()

def aPropos():
    showinfo(title = "A propos", message = "Ce merveilleux jeu du Space Invaders vous est propose par Adrien COVAREL et Baptiste HAROU ( sur une idee originale du genialissime Xavier TROUILLOT")
"---------------------------------PROGRAMME--PRINCIPAL--------------------------------------------"  
#Variables 
Largeur = 800
Hauteur = 800
x = 30
y = 30
PosXvaisseau = Largeur/2      # Pour que le vaisseau soit au centre horizontalement
PosYvaisseau = Hauteur-35
tirEnCours = False
dKill = -100000000
dBonus = 100
score = 0
vie = 3
debut = False

#interface de jeu
fenetre = Tk()
fenetre.title("Space Invaders")

#Creation Canevas et affichage du score :
canevas = Canvas(fenetre,width = Largeur, height = Hauteur, bg = 'black')
Texte = Label(fenetre, text ='Score : ' + str(score))
Texte.grid(row = 0, column = 0)
Texte2 = Label(fenetre, text = 'Vies : ' + str(vie))
Texte2.grid(row = 0, column = 6)
canevas.grid(row = 1, column = 0, columnspan = 7, rowspan = 5, padx = 10, pady = 10)

#Image de fond:
photoFond = PhotoImage(file = "_espace.gif")
Fond=canevas.create_image(Largeur/2, Hauteur/2, image = photoFond)

#Creation ennemies 
photoAlien=PhotoImage(file="_Alien1.gif")
listeAliens = [] #on cree une liste pour avoir plusieurs aliens
for ligne in range(30,150, 40): #on decide faire trois lignes d'aliens
    ligneAliens = [canevas.create_image(colonne, ligne, image=photoAlien) for colonne in range(80, Largeur-80, 60)]
    listeAliens.append(ligneAliens)

#Creation Liste coordonnees Aliens
LX = []
LY = []
for k in range(0,11):
    LX.append(canevas.coords(listeAliens[0][k])[0])
    LY.append(canevas.coords(listeAliens[0][k])[1])
    

#Creation Image GameOver  
photoGameOver = PhotoImage(file = "_GameOver.gif")

#Creation Vaisseau Bonus
photoVaisseauBonus = PhotoImage(file = "_vaisseau.gif")
vaisseauBonus = canevas.create_image(750, 30, image = photoVaisseauBonus)


#Creation Vaisseau
photoVaisseau = PhotoImage(file = "_vaisseau.gif")
Vaisseau = canevas.create_image(PosXvaisseau, 765, image = photoVaisseau)
canevas.focus_set()


#Creation Boutons :
Boutton = Button(fenetre, text = " Nouvelle partie ", command = lambda: start(canevas, listeAliens, photoGameOver)) #1er bouton Fin Programme
Boutton.grid(row = 2, column = 7, padx = 10, pady = 10)

Boutton2 = Button(fenetre, text = " Quitter ", command = Quitter) #1er bouton Fin Programme
Boutton2.grid(row = 4, column = 7, padx = 10, pady = 10)
fenetre.protocol("WM_DELETE_WINDOW", Quitter)

Boutton3 = Button(fenetre, text = " A propos ", command = aPropos ) #1er bouton Fin Programme
Boutton3.grid(row = 5, column = 7, padx = 10, pady = 10)



#creation defenses: On cree 3 bloc de defenses reparti sur la largeur de la fenetre
"-----------------------------------------------BLOC1---------------------------------"
blocx1 = 100
blocx2 = 130
blocy1 = 670
blocy2 = 640

defensel1 = []
defensel2 = []
for i in range(0,120,30):
    blocl1 = canevas.create_rectangle(blocx2+i, blocy1, blocx1+i, blocy2, fill = "CadetBlue4")
    defensel1.append(blocl1)
for i in range(0,120,30):
    blocl2 = canevas.create_rectangle(blocx2+i, blocy1+30, blocx1+i, blocy2+30, fill="CadetBlue4")
    defensel2.append(blocl2)
"-----------------------------------------------------------------------------------------"

"-----------------------------------------------BLOC2---------------------------------"
blocx3 = 340
blocx4 = 370
blocy3 = 670
blocy4 = 640

defense2l1 = []
defense2l2 = []
defense2 = []
for i in range(0,120,30):
    bloc2l1 = canevas.create_rectangle(blocx4+i, blocy3, blocx3+i, blocy4, fill = "CadetBlue4")
    bloc2l2 = canevas.create_rectangle(blocx4+i, blocy3+30, blocx3+i, blocy4+30, fill = "CadetBlue4")
    defense2l1.append(bloc2l1)
    defense2l2.append(bloc2l2)
    defense2 = defense2l1 + defense2l2                    
"-----------------------------------------------------------------------------------------"

"-----------------------------------------------BLOC3---------------------------------"
blocx5 = 570
blocx6 = 600
blocy5 = 670
blocy6 = 640

defense3l1 = []
defense3l2 = []
for i in range(0,120,30):
    bloc3l1 = canevas.create_rectangle(blocx6+i, blocy5, blocx5+i, blocy6, fill = "CadetBlue4")
    defense3l1.append(bloc3l1)
for i in range(0,120,30):
    bloc3l2 = canevas.create_rectangle(blocx6+i, blocy5+30, blocx5+i, blocy6+30, fill = "CadetBlue4")
    defense3l2.append(bloc3l2)
"-----------------------------------------------------------------------------------------"

fenetre.mainloop()