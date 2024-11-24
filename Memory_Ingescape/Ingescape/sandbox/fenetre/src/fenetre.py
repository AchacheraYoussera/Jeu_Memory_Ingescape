#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  fenetre.py
#  fenetre
#  Created by Ingenuity i/o on 2024/11/05
#
# "no description"
#
import ingescape as igs
from tkinter import*

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class fenetre(metaclass=Singleton):
    def __init__(self):
        pass
    
    def creer_fenetre(self,fenetre,taille,titre,couleur):

        #fonction qui redimensionne, donne le titre

        #et l'icône de la fenêtre ainsi que la couleur

        fenetre.geometry(taille) # redimensionne la fenêtre

        fenetre.title(titre)  # affiche le titre dans la fenêtre

        fenetre.configure(bg=couleur)# change la couleur du fond

    def nettoie_fenetre(self,fenetre,can,liste_widgets):

        #nettoie la fenetre

        can.delete(ALL)

        for w in liste_widgets:w.destroy()

        return fenetre