#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  Carte.py
#  Carte
#  Created by Ingenuity i/o on 2024/11/04
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


class Carte(metaclass=Singleton):
    def __init__(self):
        pass

    def creer_item(self,tim):

        "creation d'un item "

        p1=PhotoImage(file=tim+'.PNG')

        return p1

    def liste_image(self,nombre):

        # Fonction qui permet de creer un liste qui

        #     comporte un nombre de photos

        items=nombre*['']

        for i in range(nombre):

                tim='images/img'+str(i)

                items[i]=self.creer_item(tim)

        return items           

    def taille_photo(self,photo):

        largeur=photo.width()

        hauteur=photo.height()

        return largeur,hauteur 

