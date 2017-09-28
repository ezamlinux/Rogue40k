# Thomas Sanctorum
# DEUST BC2E 2014
from tkinter import *
import os
from fonctionCombat import *

global info

#----------------Fonction de jeu--------------#
       
def bindjouer(event):
    jouer()
    
def jouer():
    """Fonction principal du jeu, reinitialise les stats et la carte"""
    global herosXY, listEnnemiTerrain, jeux, equipement
    jeux = True

    info['pv'] = 5
    herosXY = [1,1]
    listEnnemiTerrain =[]
    equipement = []
    level = chargeMap()   
    afficheMap(level, herosXY)
    sauvegardeVie()
    
## convertit le .txt en liste
def chargeMap():
    """fonction qui charge la carte 'champBataille.txt' et la converti en liste"""
    global listEnnemiTerrain, level, numcarte
    try :
        carte = open('map/{}.txt'.format(numcarte),'r')
        level = carte.readlines()
        carte.close()
    except IOError:
        # si il n'y a pu de carte, on a gagné
        numcarte = 0
        victoire()
    # on releve la position des ennemiTir pour les mettres dans une nouvelle liste
    for positionX, ligne in enumerate(level):
        for positionY, elt in enumerate(ligne):
            if elt == '2':
                listEnnemiTerrain.append([positionX,positionY])     
    # efface les caracteres invisible avant et apres chaque lignes
    for i in range(len(level)):
        level[i] = level[i].strip()

    return level
        
def afficheMap(level, herosXY):
    """affiche la carte avec la position du heros"""
    x = 0
    y = 0
    we = (w/len(level[0]))
    he = (h/len(level))
    dicoCouleur = {'1':'yellow green','2':'olive','3':'green',
                    '=':'red','+':'orchid','x':'brown','-':'black',
                    '#':'grey','H':'royal blue','c':'yellow',
                    'heros':'royal blue',' ':'ivory'}
    
    for r, ligne in enumerate(level):
        for c, elt in enumerate(ligne):
            if r == herosXY[0] and c == herosXY[1]:
                ecran.create_rectangle(x,y,x+we,y+he,fill = dicoCouleur['heros'])
            elif elt in dicoCouleur:
                ecran.create_rectangle(x,y,x+we,y+he,fill = dicoCouleur[elt])
                #ecran.create_text(x+(we/2),y+(he/2),text = elt,fill = 'violet')
            #on decale d'un carré    
            x += we
        # on saute une ligne et on repart du bord gauche
        y += he
        x = 0
        
#-----Fonction In game----#        
def champDeVision(herosXY,level,listEnnemiTerrain,info):
    """Fonction qui determine si on est dans le champ de vision d'un Ennemi"""
    posX = herosXY[0]
    posY = herosXY[1]
    # on initialise le couvert
    #(si un '#' ce trouve entre le joueur et l'ennemi, les deux en beneficie)
    couvert = False
    # on mettra les ennemis visibles dans cette liste
    listEnnemiVisible=[]
    # on test notre position par rapport aux ennemi (tireur) de la carte
    # si on ce trouve sur un meme axe(x ou y)
    # on rajoute les ennemis qui nous voient à une nouvelle liste
    # [X,Y]=  coordonnés de l'ennemi
    for XY in listEnnemiTerrain:
        visible = False
        # on test la presence d'obstacle et de couvert entre la
        # position du joueur et celle de l'ennemi
        
        # axe X
        if XY[0] == posX:
            # si le joueur ce trouve à gauche
            if posY < XY[1]:
                # les tireurs n'ont une porté que de 6 case MAX
                if XY[1]-posY <=6:
                    for elt in level[XY[0]][posY:XY[1]]:
                        if elt == '#':
                            couvert = True
                            visible = True 
                        elif elt == ' 'or elt =='=':
                            visible = True
                        else:
                            visible = False
                            break
                else:
                    break
            # si il ce trouve à droite
            else:
                if posY-XY[1] <=6:
                    for elt in level[XY[0]][XY[1] + 1:posY]:
                        if elt == '#':
                            couvert = True
                            visible = True
                        elif elt == ' ' or elt =='=':
                            visible = True
                        else:
                            visible = False
                            break
                else:
                    break
        # axe Y             
        if XY[1] == posY :
            # si le joueur ce trouve au dessus du de l'ennemi
            if posX < XY[0]:
                if XY[0]- posX <= 6:
                    for y in level[posX:XY[0]]:
                        if y[posY] == '#':
                            couvert = True
                            visible = True
                        elif y[posY] == ' 'or y[posY] =='=':
                            visible = True
                        else:
                            visible = False
                            break
                else:
                    break
            # si il ce trouve en dessous
            else:
                if posX - XY[0] <= 6:
                    for y in level[XY[0]+1:posX]:
                        if y[posY] == '#':
                            couvert = True
                            visible = True
                        elif y[posY] == ' 'or y[posY] =='=':
                            visible = True
                        else:
                            visible = False
                            break
                else:
                    break
        
        ## si y'a aucun obstacle, l'ennemi peut nous tirer dessus    
        if visible == True:
            listEnnemiVisible.append(XY)
            action.config(text='Un {} me canarde'.format(ennemi2['nom']))
            for elt in listEnnemiVisible:
                touche = False
                ennemitouche = False
                
                attaque = tir(ennemi2,info)
                # si il arrivent à nous toucher
                if attaque == True:
                    if couvert == True:
                        sauvegardeCouvert = d()
                        if sauvegardeCouvert == 6:
                            etat.config(text='Ma foi m\'a sauvé')
                        else:
                            touche = True
                    else:
                        touche = True
                else:
                    etat.config(text='Ce n\'est pas passé loin')
                    
                attaque = tir(info,ennemi2)
                #si on arrive à le toucher
                if attaque == True:
                    if couvert == True:
                        sauvegardeCouvert = d()
                        if sauvegardeCouvert == 6:
                            etatEnnemi.config(text='L\'obstacle l\' a sauvé...')
                        else : ennemitouche = True
                    else:
                        ennemitouche = True
                else:
                    etat.config(text='RATÉ !')
                if ennemitouche == True:
                    etat.config(text='BANG, un de moins !')
                    # on les efface de la carte, de la listeVisible et la listeTerrain
                    level[elt[0]] = level[elt[0]][:elt[1]]+ " " + level[elt[0]][elt[1] +1:]
                    listEnnemiVisible.remove(elt); listEnnemiTerrain.remove(elt)
                    
                elif touche ==True:
                    etat.config(text='Je suis touché !')
                    info['pv'] -= 1
                    
                    
def sauvegardeVie():
    """ affiche la vie, et effectuer un jet de sauvegarde si vie ==0"""
    vieCanvas.delete(ALL)
    couleurVie = 'black'
    if info['pv'] == 0:
        ## sauvegarde d'armure 
        x = d()
        if x >= info['svg']:
            info['pv'] += 1
            etatEnnemi.config(text='Non, je ne mourrai pas... pas encore !')
            couleurVie='red'
        else:
            defaite()
    elif info['pv'] == 2:
        couleurVie ='orange'
    elif info['pv'] <= 1:
        couleurVie ='red'
    else:
        couleurVie = 'green'
    vieCanvas.create_text(5,5,text=info['pv'],fill =couleurVie)

#----------------------Les deplacement---------------------#                
def verificationDeplacement(terrain,posX,posY,info):
    """## verifie si le deplacement est possible, sinon retourne 'None'"""
    global equipement, numcarte
    #----#
    def combat(ennemi):
        """Sous fonction de verificationDeplacement, qui represente le deroulement
           d'un combat au Corp à Corp"""
        # On attaque l'ennemi
        action.config(text='Un {} !'.format(ennemi['nom']))
        atk = CaC(info,ennemi)
        
        if atk == True:
            etat.config(text='Je l\'ai eu !')
            terrain[posX] = terrain[posX][:posY]+ " " +terrain[posX][posY +1:]
            # on remet la vie au max
            ennemi['pvCombat'] = ennemi['pv']
            return [posX, posY]
        
        # il nous attaque si on à pas su le tuer  
        else: 
            etat.config(text='J\'ai raté mon assaut')  
            jetTouche = pourToucher(ennemi['cc'],info['cc'])
            x = d()
            if x >= jetTouche:
                jetBlesse = pourBlesser(ennemi['e'],info['f'])
                if jetBlesse != None:
                    x = d()
                    if x >= jetBlesse:
                        info['pv'] -= 1
                        etatEnnemi.config(text ='Je suis touché !')
                    else: etatEnnemi.config(text ='Il m\'a loupé')
                else: etatEnnemi.config(text ='Ces armes ne me font rien')
            else: etatEnnemi.config(text ='...Lui aussi')
            return None
    #-----#
    
    #---------Interaction avec les élements-------------#
    # ennemmi 1
    if terrain [posX][posY] == '1':
        combat(ennemi1)
    
    # ennemi 2
    elif terrain [posX][posY] =='2' :
        combat(ennemi2)
    
    # ennemi 3   
    elif terrain [posX][posY] =='3' :
        combat(ennemi3)
        
    # relique 
    elif terrain[posX][posY] == '+':
        action.config(text='Une sainte Relique !')
        if info['pv'] < 5:
            etat.config(text ='Je sens sa puissance me traverser')
            info['pv'] = 5
            terrain[posX] = terrain[posX][:posY]+ " " +terrain[posX][posY +1:]
            return [posX, posY]
        else:
            return None
        
    # mur destructible
    elif terrain[posX][posY] == 'x':
        # si l'on possede une bombe
        if 'bombe' in equipement:
            action.config(text='Badoom Haha !')
            terrain[posX] = terrain[posX][:posY]+ " " +terrain[posX][posY +1:]
            equipement.remove('bombe')
            return [posX, posY]
        
        else:
            action.config(text='Ce mur semble fragile...')
            return None
        
    # coffre, permet de trouver des bombes
    elif terrain[posX][posY] == 'c':
        action.config(text ='J\'ai trouvé des explosifs')
        terrain[posX] = terrain[posX][:posY]+ " " +terrain[posX][posY +1:]
        equipement.append('bombe')
        return [posX, posY]
    
    # Riviere d'acide
    elif terrain[posX][posY] == '=':
        action.config(text ='De l\'acide !')
        x=d()
        if x ==1:
            info['pv'] -= 1
            etat.config(text='Ça me ronge !')
        else:
            etat.config(text='Meme pas mal !')
            
        return [posX, posY]
    
    # La sortie !
    elif terrain[posX][posY] == 'H':
        numcarte +=1
        jouer()
    
    # si different d'une route
    elif terrain[posX][posY] != ' ':
        return None
    
    else:
        return [posX,posY]
    
#---Touche /déplacement---#
def mouvement(event):
    """Fonction qui recupere la touche préssé
       et si toutes les conditions sont resolu, déplace le personnage"""
    global jeux
    touche = event.keysym
    # si le jeux est lancé, et que l'on est pas sur le popUp de defaite ou de victoire
    if jeux == True:
        # on efface les labels
        action.config(text ='')
        etatEnnemi.config(text='')
        etat.config(text='')
        
        dep = None # simple valeur booleene
        # on recupere la touche, et verifie si le deplacement est possible
        # (voir verificationDeplacement())
        if touche =='Right':
            dep = verificationDeplacement(level, herosXY[0], herosXY[1] +1, info)
                
        elif touche =="Left":
            dep = verificationDeplacement(level, herosXY[0], herosXY[1] -1, info)
                
        elif touche == "Up":
            dep = verificationDeplacement(level, herosXY[0] - 1, herosXY[1], info)
            
        elif touche =="Down":
            dep = verificationDeplacement(level, herosXY[0] + 1, herosXY[1], info)
                
        # si on peux ce deplacer, pourquoi s'en priver ? :)
        if dep != None:
            herosXY[0] = dep[0]
            herosXY[1] = dep[1]
            champDeVision(herosXY,level,listEnnemiTerrain,info)
            ecran.delete(ALL)
            afficheMap(level, herosXY)
        sauvegardeVie()
        
#-----------PopUp------------#
def victoire():
    global jeux
    """Pop up de victoire"""
    def bindrejouer(event):
        rejouer()
    def rejouer():
        global numcarte
        numcarte = 1
        top.destroy()
        jouer()
    jeux = False
    numcarte = 1
    top = Toplevel(root)
    top.focus()
    top.title('Victoire')
    victoireLabel = Label(top, text ='Vous avez gagnez')
    rejouerBouton =Button(top,text= '(R)ejouer',command = rejouer)
    img = PhotoImage(file="./ressource/victoire.gif")
    image = Label(top, image = img)

    image.grid(row = 1,column =1,columnspan =2)
    victoireLabel.grid(row=2,column=1,columnspan=2)
    rejouerBouton.grid(row =3,column =1)
    top.bind("<r>",bindrejouer)
    
    top.mainloop()
def defaite():
    global jeux
    """Pop up de defaite"""
    def bindrejouer(event):
        rejouer()
    def rejouer():
        top.destroy()
        jouer()
    jeux = False
    
    top = Toplevel(root)
    top.focus()
    top.title('Défaite')
    defaiteLabel = Label(top, text ='Vous avez perdu')
    rejouerBouton =Button(top,text= '(R)ecommencer',command = rejouer)
    img = PhotoImage(file="./ressource/defaite.gif")
    image = Label(top, image = img)
    
    image.grid(row = 1,column =1,columnspan =2)
    defaiteLabel.grid(row=2,column=1,columnspan=2)
    rejouerBouton.grid(row =3,column =1)
    top.bind("<r>",bindrejouer)
    
    top.mainloop()
    
def bindcredit(event):
    credit()   
def credit():
    """Pop up de credit"""
    top = Toplevel(root)
    top.title('Credits')
    Label(top, text = 'Rogue 40k').pack()
    Label(top, text = 'Un Rogue-Like basé sur Warhammer 40k').pack()
    Label(top, text = 'D\'après une idée original de :').pack()
    Label(top, text = 'Thomas Sanctorum DEUST BCEE 2014').pack()
    Label(top, text = '"Le fardeau de l\'echec est le plus terrible chatiment"').pack()
    top.mainloop()
    
def bindregles(event):
    regles()       
def regles() :
    """pop up des regles"""
    os.getcwd
    top=Toplevel()            
    top.title("Règles")
    fichier=open("ressource/regles.txt", "r")
    lecture = fichier.readlines()
    for k in lecture :
        Label(top, text=k).pack()
    fichier.close()
    top.mainloop()
        
def bindinventaire(event):
    inventaire()
def inventaire():
    """pop-up Inventaire (WIP)"""
    equipementAafficher = equipement
    top=Toplevel()            
    top.title("Inventaire")
    ecranInventaire = Canvas(top)
    ecranInventaire.pack()
    Label(top, text ="WIP").pack()
    x = 0
    y = 0
    for nbItem in range(10):
        if 'bombe' in equipementAafficher:
            ecranInventaire.create_rectangle(x,y,x+20,y+20, fill='ivory')
            ecranInventaire.create_text(x+10,y+10, text = 'B')
            # equipementAafficher.remove('bombe')
        else:
            ecranInventaire.create_rectangle(x,y,x+20,y+20, fill='grey')
        x += 20
        
    top.mainloop()

def quitter(event):
    root.quit()
    
#---------------------MAIN-----------------------------#
# Root
root = Tk()
root.title('Rogue 40k')
root.protocol("WM_DELETE_WINDOW", root.quit)

#-------------Menu---------------#   
mainMenu = Menu(root)
menuJeux = Menu(mainMenu)
menuInfo = Menu(mainMenu)

# menu Jeux
menuJeux.add_command(label='(N)ouvelle Partie',command = jouer)
menuJeux.add_command(label='(Q)uitter',command = root.quit)

#menu Info
menuInfo.add_command(label ='(R)ègles',command = regles)
menuInfo.add_command(label ='(C)redits',command = credit)

## on rajoute les menus au menu...
mainMenu.add_cascade(label = "Jeux", menu=menuJeux)
mainMenu.add_cascade(label ='A propos',menu =menuInfo)

root.config(menu = mainMenu)
#--------------------------------#
#information PJ & PNJ
info = {'cc':6,'ct':5,'f':4,'e':4,'pv':5,'nom':'Gabriel','svg':3}
equipement = []

# ennemi CaC
ennemi1 = {'nom':'Gretchin','cc':2,'ct':3,'f':2,'e':2,'pv':1,'pvCombat':1,'svg':None}
# ennemi Tireur
ennemi2 = {'nom':'BoyZ','cc':4,'ct':2,'f':3,'e':4,'pv':1,'pvCombat':1,'svg':6}
# Capitaine ennemi
ennemi3 = {'nom':'Big boss','cc':5,'ct':2,'f':5,'e':5,'pv':3,'pvCombat':3,'svg':6}

# autre variable global

jeux = False # par defaut, le jeux ne ce lance pas
numcarte = 1 # numero de carte (compteur)

#-- Interface --#
w = 800
h = 500

# ecran de jeux #
ecran = Canvas(root,width = w,height = h)
root.bind("<Key>", mouvement)

# ouvre les Toplevel
root.bind("<e>", bindinventaire)
root.bind("<c>", bindcredit)
root.bind("<r>", bindregles)
root.bind("<q>", quitter)
root.bind("<n>", bindjouer)

#----------------#
information = Frame(root)   
nom = Button(information, text = '{} '.format(info['nom']),font=("Helvetica", 18),command = inventaire)
vieCanvas = Canvas(information,width =10,height=10)
imgFace = PhotoImage(file="./ressource/faceset.gif")
face= Label(information, image = imgFace)

frameEtat = Frame(root, border = 2,relief ='ridge')
action = Label(frameEtat, text = '',width = 25,height=3,font=("Helvetica", 15))
etat = Label(frameEtat, text = '',width = 25,height=3)
etatEnnemi = Label(frameEtat, text = '',width = 25,height=3)
# grid
ecran.grid(row = 1,column = 1,columnspan = 4)

information.grid(row = 2, column = 1)
nom.grid(row = 1, column = 1)
vieCanvas.grid(row = 2, column = 1)
face.grid(row =1, column=2, rowspan = 2)

frameEtat.grid(row = 2,column = 2)
action.grid(row = 1, column = 1,columnspan = 2)
etat.grid(row = 2, column = 1)
etatEnnemi.grid(row = 2, column = 2)

#--fonction principal--#
root.mainloop()
root.destroy()
