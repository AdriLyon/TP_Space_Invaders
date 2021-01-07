from Tkinter import *
from random import *

"--------------------------------------FONCTIONS------------------------------------"
   
def deplacerAliens(canevas,listeAliens,photoGameOver, dx=20,dy=40, vitesse=1000):
    xPremier = 10000
    xDernier = 0
    listeAliens = [ligne for ligne in listeAliens if ligne]
    _, yPlusBas = canevas.coords(listeAliens[-1][0])
    if yPlusBas>590:
        canevas.create_image(Largeur/2,Hauteur/2,image=photoGameOver)
        listeAliens=[]
    for ligne in listeAliens:
        x, _ = canevas.coords(ligne[0])
        if x < xPremier:
            xPremier = x
        x, _ = canevas.coords(ligne[-1])
        if x > xDernier:
            xDernier = x
    deplacementVertical = False
    if xPremier <= 40 and dx==-20:
        dx=20
        deplacementVertical = True
    if xDernier >= Largeur-40 and dx==20:
        dx=-20
        deplacementVertical = True
    if deplacementVertical:
        if vitesse >= 120:
            vitesse -= 50
        for ligne in listeAliens:
            for alien in ligne:
                canevas.move(alien,0,dy)
    else:
        for ligne in listeAliens:
            for alien in ligne:
                canevas.move(alien,dx,0)
    canevas.after(vitesse, lambda: deplacerAliens(canevas,listeAliens,photoGameOver, dx,dy, vitesse))
    
    
def deplacerVaisseau(event):
    global PosXvaisseau, PosYvaisseau
    touche = event.keysym
    if touche == 'Right':
        if PosXvaisseau <= Largeur-50:
            PosXvaisseau+=10
            canevas.coords(Vaisseau,PosXvaisseau+1,Hauteur-35)
    if touche == 'Left':
        if PosXvaisseau >= 50:
            PosXvaisseau-=10
            canevas.coords(Vaisseau,PosXvaisseau-1,Hauteur-35)
            
    
def tirer(dy,v, missile=None):
    global PosXvaisseau, PosYvaisseau, tirEnCours, dKill,LX,LY,missileAlien,score,listeAliens
    if not missile and not tirEnCours:
        tirEnCours = True         
        missile=canevas.create_rectangle(PosXvaisseau-3,PosYvaisseau-10,PosXvaisseau+2.2,PosYvaisseau+15,fill="lime green")
    for i in range(0,11):
        if canevas.coords(missile)[1] <= 0:
            canevas.delete(missile)
            missile=None
            tirEnCours = False
    for i in range(0,4):
        if abs((canevas.coords(missile)[1])-canevas.coords(defense2[i])[1])<30 and abs((canevas.coords(missile)[0])-canevas.coords(defense2[i])[0]-8)<20:
            canevas.move(defense2[i],0,dKill)
            canevas.delete(missile)
            missile=None
            tirEnCours = False
        elif abs((canevas.coords(missile)[1])-canevas.coords(defense2l1[i])[1])<30 and abs((canevas.coords(missile)[0])-canevas.coords(defense2l1[i])[0]-8)<20:
            canevas.move(defense2l1[i],0,dKill)
            canevas.delete(missile)
            missile=None
            tirEnCours = False 
        elif abs((canevas.coords(missile)[1])-canevas.coords(defense2l2[i])[1])<30 and abs((canevas.coords(missile)[0])-canevas.coords(defense2l2[i])[0]-8)<20:
            canevas.move(defense2l2[i],0,dKill)
            canevas.delete(missile)
            missile=None
            tirEnCours = False   
        elif abs((canevas.coords(missile)[1])-canevas.coords(defense3l1[i])[1])<30 and abs((canevas.coords(missile)[0])-canevas.coords(defense3l1[i])[0]-8)<20:
            canevas.move(defense3l1[i],0,dKill)
            canevas.delete(missile)
            missile=None
            tirEnCours = False
        elif abs((canevas.coords(missile)[1])-canevas.coords(defense3l2[i])[1])<30 and abs((canevas.coords(missile)[0])-canevas.coords(defense3l2[i])[0]-8)<20:
            canevas.move(defense3l2[i],0,dKill)
            canevas.delete(missile)
            missile=None
            tirEnCours = False 
    for ligne in listeAliens:         
        for alien in ligne :
            x,y=canevas.coords(alien)
            centreMissile=((PosXvaisseau-3)+(PosXvaisseau+2.2))/2
            if abs(x-centreMissile)<=22 and abs(y-(canevas.coords(missile)[1]))<=20:
                canevas.delete(missile)
                missile= None
                tirEnCours = False
                canevas.delete(listeAliens[listeAliens.index(ligne)][ligne.index(alien)])
                ligne.remove(alien)
                score+=10
                txt1 = Label(fenetre, text ='Score : '+ str(score))
                txt1.grid(row=0, column=0)
    if abs((canevas.coords(missile)[1])-canevas.coords(vaisseauBonus)[1])<5 and abs((canevas.coords(missile)[0])-canevas.coords(vaisseauBonus)[0])<25:
        canevas.move(vaisseauBonus,0,dKill)
        canevas.delete(missile)
        missile=None
        tirEnCours = False 
        score+=150
        txt1 = Label(fenetre, text ='Score : '+ str(score))
        txt1.grid(row=0, column=0)
    else:
        canevas.move(missile,0,dy)
        canevas.after(v, lambda: tirer(-5,8, missile)) 
        

def tirEnnemi(dy,v):
    global listeAliens,PosXvaisseau,PosYvaisseau, vie
    if randint(0, 3) == 0:
        print "tir"
        alien_aleatoire=choice(listeAliens[-1]) # on choisit au hasard l'alien qui va tirer
        PosXalien,PosYalien=canevas.coords(alien_aleatoire)
        boule=canevas.create_oval(PosXalien-5,PosYalien+55,PosXalien+5,PosYalien+65,fill="red2")
        deplacerBombe(boule, dy)
    canevas.after(100, lambda: tirEnnemi(-5,25))    

        

def deplacerBombe(boule, dy):
    global canevas, vie, PosYvaisseau, PosXvaisseau
    canevas.move(boule,0,-dy)
    bx,by,_,_=canevas.coords(boule)
    if abs(PosXvaisseau-bx)<=10 and abs(PosYvaisseau-by)<=20:
        canevas.delete(boule)
        vie-=1
        txt2 = Label(fenetre, text ='Vies : '+ str(vie))
        txt2.grid(row=0, column=6)
    elif by > Hauteur:
        canevas.delete(boule)
    else:
        canevas.after(40, lambda: deplacerBombe(boule, dy))
  
  
def start(canevas,listeAliens,photoGameOver):
    global started
    if not started:
        deplacerAliens(canevas,listeAliens,photoGameOver)
        canevas.bind('<Key>', deplacerVaisseau)
        canevas.bind('<space>', lambda _: tirer(-40,100))
        tirEnnemi(1,5)
        started = True
        
"---------------------------------PROGRAMME--PRINCIPAL--------------------------------------------"  
#Variables 
Largeur=800
Hauteur=800
x=30
y=30
PosXvaisseau=Largeur/2
PosYvaisseau=Hauteur-35
tirEnCours = False
dKill=-100000000
dBonus=100
score=0
vie=3
started=False

#interface de jeu
fenetre=Tk()
fenetre.title("Space Invaders")

#Creation Canevas et affichage du score :
canevas=Canvas(fenetre,width=Largeur,height=Hauteur,bg='black')
txt1 = Label(fenetre, text ='Score : '+ str(score))
txt1.grid(row=0, column=0)
txt2 = Label(fenetre, text ='Vies : '+ str(vie))
txt2.grid(row=0, column=6)
canevas.grid(row=1, column=0, columnspan=7, rowspan=5, padx=10, pady =10)

#Image de fond:
photoFond=PhotoImage(file="/fs03/share/users/adrien.covarel/home/Documents/DEV-Python/TP3/_espace.gif")
Fond=canevas.create_image(Largeur/2,Hauteur/2,image=photoFond)

#Creation ennemies 
photoAlien=PhotoImage(file="/fs03/share/users/adrien.covarel/home/Documents/DEV-Python/TP3/_Alien1.gif")
listeAliens = [] #on cree une liste pour avoir plusieurs aliens
for ligne in xrange(30,150, 40): #on decide faire trois lignes d'aliens
    ligneAliens = [canevas.create_image(colonne, ligne, image=photoAlien) for colonne in xrange(80, Largeur-80, 60)]
    listeAliens.append(ligneAliens)

#Creation Liste coordonnees Aliens
LX=[]
LY=[]
for k in range(0,11):
    LX.append(canevas.coords(listeAliens[0][k])[0])
    LY.append(canevas.coords(listeAliens[0][k])[1])
    

#Creation Image GameOver  
photoGameOver=PhotoImage(file="/fs03/share/users/adrien.covarel/home/Documents/DEV-Python/TP3/_GameOver.gif")

#Creation Vaisseau Bonus
photoVaisseauBonus=PhotoImage(file="/fs03/share/users/adrien.covarel/home/Documents/DEV-Python/TP3/_vaisseau.gif")
vaisseauBonus=canevas.create_image(750,30,image=photoVaisseauBonus)


#Creation Vaisseau
photoVaisseau=PhotoImage(file="/fs03/share/users/adrien.covarel/home/Documents/DEV-Python/TP3/_vaisseau.gif")
Vaisseau=canevas.create_image(PosXvaisseau,765,image=photoVaisseau)
canevas.focus_set()


#Creation Boutons :
bout1 = Button(fenetre, text=" Nouvelle partie ",command=lambda: start(canevas,listeAliens,photoGameOver)) #1er bouton Fin Programme
bout1.grid(row=2, column=7, padx=10, pady =10)

bout2 = Button(fenetre, text=" Quitter ",command=fenetre.destroy) #1er bouton Fin Programme
bout2.grid(row=4, column=7, padx=10, pady =10)


#creation defenses:
"-----------------------------------------------BLOC1---------------------------------"
blocx1=100
blocx2=130
blocy1=670
blocy2=640

defensel1=[]
defensel2=[]
for i in range(0,120,30):
    blocl1=canevas.create_rectangle(blocx2+i,blocy1,blocx1+i,blocy2,fill="CadetBlue4")
    defensel1.append(blocl1)
for i in range(0,120,30):
    blocl2=canevas.create_rectangle(blocx2+i,blocy1+30,blocx1+i,blocy2+30,fill="CadetBlue4")
    defensel2.append(blocl2)
"-----------------------------------------------------------------------------------------"

"-----------------------------------------------BLOC2---------------------------------"
blocx3=340
blocx4=370
blocy3=670
blocy4=640

defense2l1=[]
defense2l2=[]
defense2=[]
for i in range(0,120,30):
    bloc2l1=canevas.create_rectangle(blocx4+i,blocy3,blocx3+i,blocy4,fill="CadetBlue4")
    bloc2l2=canevas.create_rectangle(blocx4+i,blocy3+30,blocx3+i,blocy4+30,fill="CadetBlue4")
    defense2l1.append(bloc2l1)
    defense2l2.append(bloc2l2)
    defense2=defense2l1+defense2l2                    
"-----------------------------------------------------------------------------------------"

"-----------------------------------------------BLOC3---------------------------------"
blocx5=570
blocx6=600
blocy5=670
blocy6=640

defense3l1=[]
defense3l2=[]
for i in range(0,120,30):
    bloc3l1=canevas.create_rectangle(blocx6+i,blocy5,blocx5+i,blocy6,fill="CadetBlue4")
    defense3l1.append(bloc3l1)
for i in range(0,120,30):
    bloc3l2=canevas.create_rectangle(blocx6+i,blocy5+30,blocx5+i,blocy6+30,fill="CadetBlue4")
    defense3l2.append(bloc3l2)
"-----------------------------------------------------------------------------------------"

fenetre.mainloop()