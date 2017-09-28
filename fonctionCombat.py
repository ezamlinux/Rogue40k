#### regroupe les fonctions de combat ###
from random import randint
def tir(tireur,cible):
    """Fonction de deroulement d'une phase de tir
       y = information joueur
       z = information ennemi """
    touche = 7 - tireur['ct']
    if touche != 1:
        x = d()
        if x >= touche:
            blesse = pourBlesser(cible['e'],tireur['f'])
            x = d()
            if x >= blesse:
                return True                                 
    
def CaC(joueur,cible):
    """Fonction de deroulement d'une phase d'assaut"""
    # une phase d'assaut ce deroule comme tel :
    # jet pour toucher, jet pour bléssé et jet de sauvegarde si possible          
    jetTouche = pourToucher(joueur['cc'],cible['cc'])
    x = d()
    if x >= jetTouche:
        jetBlesse = pourBlesser(joueur['e'],cible['f'])
        if jetBlesse != None:
            x = d()
            if x >= jetBlesse:
                cible['pvCombat'] -= 1 
                if cible['pvCombat'] == 0:
                    return True
                
def pourToucher(x, y):
    """fonction qui renvoie un resultat à jouer au dé :
       x = CC de la cible
       y = CC de l'attaquant"""

    
    table =[[0,1,2,3,4,5,6,7,8,9,10],
	    [1,4,4,5,5,5,5,5,5,5,5],
            [2,3,4,4,4,5,5,5,5,5,5],
            [3,3,3,4,4,4,4,5,5,5,5],
            [4,3,3,3,4,4,4,4,4,5,5],
            [5,3,3,3,3,4,4,4,4,4,4],
            [6,3,3,3,3,3,4,4,4,4,4],
            [7,3,3,3,3,3,3,4,4,4,4],
            [8,3,3,3,3,3,3,3,4,4,4],
            [9,3,3,3,3,3,3,3,3,4,4],
            [10,3,3,3,3,3,3,3,3,3,4]]


    i = table[0].index(x)
    for pos, k in enumerate(table):
        # on cherche y dans la premiere colonne
        if k[0] == y:
            resultat = table[pos][i]

    return resultat

def pourBlesser(x, y):
    """fonction qui renvoie un resultat à jouer au dé :
       x endurance de la cible
       y force de l'attaquant"""

    
    table =[[0,1,2,3,4,5,6,7,8,9,10],
	    [1,4,5,6,6,'-','-','-','-','-','-'],
            [2,3,4,5,6,6,'-','-','-','-','-'],
            [3,2,3,4,5,6,6,'-','-','-','-'],
            [4,2,2,3,4,5,6,6,'-','-','-'],
            [5,2,2,2,3,4,5,6,6,'-','-'],
            [6,2,2,2,2,3,4,5,6,6,'-'],
            [7,2,2,2,2,2,3,4,5,6,6],
            [8,2,2,2,2,2,2,3,4,5,6],
            [9,2,2,2,2,2,2,2,3,4,5],
            [10,2,2,2,2,2,2,2,2,3,4]]


    i = table[0].index(x)
    for pos, k in enumerate(table):
        # on cherche y dans la premiere colonne
        if k[0] == y:
            resultat = table[pos][i]
            
    # intouchable        
    if resultat == '-':
        return None
    
    return resultat

def d():
    """ fonction qui renvoit le resultat d'un lancer de dé
     à 6 faces """
    
    r = randint(1, 7)

    return r
