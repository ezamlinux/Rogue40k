# Thomas sanctorum
from tkinter import *
import os
import dicoSprites

def affichage():
    x,y = 0,0
    ecran.delete(ALL)
    dicoCouleur = dicoSprites.BDD()
    for ligne in maListe:
        for elt in ligne:
            if elt in dicoCouleur:
                print(elt, dicoCouleur[elt])
                ecran.create_rectangle(x,y,x+taille,y+taille,fill = dicoCouleur[elt])
            y += taille
        y = 0
        x += taille
            
def creation():
    for k in range(20):
        maListe.append(20*[' '])
        
def modifier(event):
    # on recupere la position de la souris, on divise par la taille d'un carré
    # en recuperant que le chiffre avant la virgule
    # ce qui nous donne les coordoné dans la liste, on rajoute l'élement selectionné
    x = (event.x)//taille
    y = (event.y)//taille
    print(retour.get())
    maListe[x][y] = retour.get()
    affichage()
    
def sauvegarder():
    rep = os.getcwd()
    fichier = open('carte.txt','w')
    for ligne in maListe:
        fichier.write('{} \n'.format(str(''.join(ligne))))
    fichier.close()

#------------------------------#
##x = int(input('quel hauteur ? : '))
##y = int(input('quel longueur ? : '))

maListe = []
creation()

taille = 600//len(maListe)
root = Tk()

root.title('WorldBuilder-WIP')
root.geometry("800x600")
ecran = Canvas(root,bg='ivory',height = 600,width = 600,border = 1, relief ="raised")
ecran.grid(row =0, column =0,rowspan =2)
ecran.bind("<Button-1>", modifier)

retour = StringVar()
choix = Frame(root)
bouton1 = Radiobutton(choix, text="1", variable=retour, value='E001')
bouton2 = Radiobutton(choix, text="2", variable=retour, value='E002')
bouton3 = Radiobutton(choix, text="3", variable=retour, value='E003')
bouton4 = Radiobutton(choix, text="Acide", variable=retour, value='D001')
bouton5 = Radiobutton(choix, text="Relique", variable=retour, value='I002')
bouton6 = Radiobutton(choix, text="Breche", variable=retour, value='D002')
bouton7 = Radiobutton(choix, text="Obstacle", variable=retour, value='D004')
bouton8 = Radiobutton(choix, text="Mur", variable=retour, value='D003')
bouton9 = Radiobutton(choix, text="Sortie", variable=retour, value='S001')
bouton10 = Radiobutton(choix, text="Coffre", variable=retour, value='I001')
bouton11 = Radiobutton(choix, text="Sol", variable=retour, value=' ')

boutonSave = Button(choix, text = "Sauvegarder", command = sauvegarder)
choix.grid(row =3,column = 0,columnspan = 5)
bouton1.grid(row=0, column=0)
bouton2.grid(row=0, column=1)
bouton3.grid(row=0, column=2)
bouton4.grid(row=0, column=3)
bouton5.grid(row=0, column=4)
bouton6.grid(row=0, column=5)
bouton7.grid(row=1, column=0)
bouton8.grid(row=1, column=1)
bouton9.grid(row=1, column=2)
bouton10.grid(row=1, column=3)
bouton11.grid(row=1, column=4)
boutonSave.grid(row =2,column =1)
affichage()

root.mainloop()
