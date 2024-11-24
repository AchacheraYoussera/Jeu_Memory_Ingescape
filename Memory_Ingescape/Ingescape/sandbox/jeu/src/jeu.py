#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  jeu.py
#  jeu
#  Created by Ingenuity i/o on 2024/11/16
#
# "no description"
#
import ingescape as igs
from pathlib import Path
import sys

from fenetre import *
from tkinter import*
from random import randrange
import os
import sys
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(base_path, 'fenetre', 'src'))
from fenetre import *
from fenetre import fenetre as fenetre_classe

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class jeu(metaclass=Singleton):
    def __init__(self, can, l_image, ligne, colonne, lp, cp, photos):
        self.can = can
        self.l_image = l_image
        self.ligne = ligne
        self.colonne = colonne
        self.lp = lp
        self.cp = cp
        self.photos = photos
        self.memoire = [0, 0, 0, 0, -1, 0]  # memoire pour le jeu
        self.l_items = []
        self.numimage = 0
        self.x=0
        self.y=0
     

    def Tableau(self,ligne,colonne):


        #fabrication du tableau

        tableau=ligne*[0]

        for ln in range(ligne):tableau[ln]=colonne*[0]

        return tableau     

    def affiche_fond(self,can,l_image,l_nombre,ligne,colonne):

        #affiche le fond de la première febêtre

        l_items=[]

        for i in range(ligne):

            for j in range(colonne):

                B=can.create_image(j*self.cp+self.cp/2,i*self.lp+self.lp/2,image=l_image[0])

                l_items.append(B)

        return l_items

    
    def verifie_memoire(self, can, l_nombre, l_image, lp, cp, ligne, colonne, l_items, memoire, photos, k):

        # on vérifie si la première image est la même que la première
        change = False

        if photos[l_nombre[k]] == 0 and k != memoire[4]:

            if memoire[0] == 1:

                memoire[4] = -1
                offset_x = 200.0  # Décalage horizontal entre les images
                offset_y = 200.0  # Décalage vertical entre les images

                if l_nombre[k] == l_nombre[memoire[1]]:

                    memoire[5] += 1
                    change = True
                    photos[l_nombre[k]] = 1
                    self.numimage += 1

                    # # Calcul des lignes et colonnes pour respecter la grille de 5 images par ligne
                    
                    # Calcul des coordonnées x et y
                    if self.numimage < 6:
                        self.x +=  offset_x
                        self.y = 0
                    else:
                        self.x +=  offset_x  
                        self.y = 200.00  
                    
                    

                    # Chargement de l'image
                    num_image = int(''.join(filter(str.isdigit, str(l_image[l_nombre[k]])))) - 1
                    img_name = "img" + str(num_image)
                    chemin_image = "file:///C:/Users/yssr0/Documents/Ingescape/sandbox/fenetre/src/images/" + img_name + ".PNG"
                    print(chemin_image)
                    igs.service_call("Whiteboard", "addImageFromUrl", (chemin_image, self.x, self.y), "")
                    if self.numimage == 5:
                        self.x = 0
                    igs.service_call("Whiteboard", "chat", ("Félicitation, vous avez trouvé une nouvelle image"), "")
                    if self.numimage==10:
                        igs.service_call("Whiteboard", "addText", ("Félicitation, vous avez gagné",400.00,400.00,"black"), "")
                        igs.service_call("Whiteboard","addText", ("Avec un score de : "+str(memoire[3]),450.00,450.00,"black"), "")
                        igs.service_call("Whiteboard", "chat", ("Pour rejouer, cliquez sur le bouton 'Rejouer'"), "")
                        igs.service_call("Whiteboard", "chat", ("Pour quitter, cliquez sur le bouton 'Quitter'"), "")
                        igs.service_call("Whiteboard", "chat", ("Bonne chance"), "")

                else:

                    change_image = l_image[0]
                    can.itemconfigure(l_items[memoire[1]], image=change_image)

                memoire[2] = 1
                memoire[1] = 0

            if memoire[0] == 0:

                memoire[1] = k
                memoire[0] = 1
                memoire[4] = k
                change = True

        # La fonction retourne l'autorisation de changer l'image et réinitialise la mémoire des données
        return change, memoire, photos


    def melange(self,liste):

        " remplissage aléatoire d'une liste de  nombres entiers"

        numimage=len(liste)

        for i in range(numimage):liste[i]=2

        k=0

        while k<numimage-1:

                remelange=False

                numero=randrange(0,numimage)

                for j in range(0,numimage):

                    if numero==liste[j] :remelange=True

                if remelange==False:

                    liste[k]=numero  

                    k=k+1

        return liste




