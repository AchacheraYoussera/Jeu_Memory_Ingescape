#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  fenetre
#  Created by Ingenuity i/o on 2024/11/05
#
# "no description"
#

import signal
import getopt
import time
from pathlib import Path
import traceback
import sys

from fenetre import *
from tkinter import*
from random import randrange
import os
import sys
from fenetre import fenetre as fenetre_classe
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(base_path, 'Carte', 'src'))

from Carte import Carte as Carte_classe
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(base_path, 'jeu', 'src'))

from jeu import jeu as jeu_classe



port = 5670
agent_name = "fenetre"
device = None
verbose = False
is_interrupted = False

short_flag = "hvip:d:n:"
long_flag = ["help", "verbose", "interactive_loop", "port=", "device=", "name="]

ingescape_path = Path("~/Documents/Ingescape").expanduser()


def print_usage():
    print("Usage example: ", agent_name, " --verbose --port 5670 --device device_name")
    print("\nthese parameters have default value (indicated here above):")
    print("--verbose : enable verbose mode in the application (default is disabled)")
    print("--port port_number : port used for autodiscovery between agents (default: 31520)")
    print("--device device_name : name of the network device to be used (useful if several devices available)")
    print("--name agent_name : published name for this agent (default: ", agent_name, ")")
    print("--interactive_loop : enables interactive loop to pass commands in CLI (default: false)")


def print_usage_help():
    print("Available commands in the terminal:")
    print("	/quit : quits the agent")
    print("	/help : displays this message")

def return_io_value_type_as_str(value_type):
    if value_type == igs.INTEGER_T:
        return "Integer"
    elif value_type == igs.DOUBLE_T:
        return "Double"
    elif value_type == igs.BOOL_T:
        return "Bool"
    elif value_type == igs.STRING_T:
        return "String"
    elif value_type == igs.IMPULSION_T:
        return "Impulsion"
    elif value_type == igs.DATA_T:
        return "Data"
    else:
        return "Unknown"

def return_event_type_as_str(event_type):
    if event_type == igs.PEER_ENTERED:
        return "PEER_ENTERED"
    elif event_type == igs.PEER_EXITED:
        return "PEER_EXITED"
    elif event_type == igs.AGENT_ENTERED:
        return "AGENT_ENTERED"
    elif event_type == igs.AGENT_UPDATED_DEFINITION:
        return "AGENT_UPDATED_DEFINITION"
    elif event_type == igs.AGENT_KNOWS_US:
        return "AGENT_KNOWS_US"
    elif event_type == igs.AGENT_EXITED:
        return "AGENT_EXITED"
    elif event_type == igs.AGENT_UPDATED_MAPPING:
        return "AGENT_UPDATED_MAPPING"
    elif event_type == igs.AGENT_WON_ELECTION:
        return "AGENT_WON_ELECTION"
    elif event_type == igs.AGENT_LOST_ELECTION:
        return "AGENT_LOST_ELECTION"
    else:
        return "UNKNOWN"

def signal_handler(signal_received, frame):
    global is_interrupted
    print("\n", signal.strsignal(signal_received), sep="")
    is_interrupted = True


def on_agent_event_callback(event, uuid, name, event_data, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, fenetre)
        # add code here if needed
    except:
        print(traceback.format_exc())


def on_freeze_callback(is_frozen, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, fenetre)
        # add code here if needed
    except:
        print(traceback.format_exc())


def click_souris(event,can,l_nombre,l_image,lp,cp,ligne,colonne,l_items,l_widgets,l_c,memoire,photos,gestion_jeu=None):

        #donne les coordonnées du click de la souris

        x,y=event.x,event.y

        ln=int(y)//lp#calcul de la ligne

        cn=int(x)//cp#calcul de la colonne

        k=ln*colonne+cn

        memoire[3]=memoire[3]+1

        score=memoire[3]

        #on vérifie si la première image est la même que la première

        changer,memoire,photos=gestion_jeu.verifie_memoire(can,l_nombre,l_image,lp,cp,ligne,colonne,l_items,memoire,photos,k)
        # if 
        if memoire[2]==1:

            for i in range(3):memoire[i]=0

        if changer==True:

            change_image=l_image[l_nombre[k]]

            can.itemconfigure(l_items[k],image=change_image)

        l_c[2].configure(text="SCORE\n"+str(score))

def jouer(fenetre,can,l_image,l_nombre,ligne,colonne,l_widgets,gestion_jeu=None):
        
        global score,memoire
        fenetres_interface=fenetre_classe()
        score=0
        image_trouvee=0
        memoire=[0,0,0,score,-1,image_trouvee]

        fenetre=fenetres_interface.nettoie_fenetre(fenetre,can,l_widgets)

        l_c[2].configure(text="SCORE\n      .")

        l_nombre=gestion_jeu.melange(l_nombre)

        for i in range(len(l_nombre)):

            l_nombre[i]=l_nombre[i]%10+1

        l_items=gestion_jeu.affiche_fond(can,l_image,l_nombre,ligne,colonne)
        igs.service_call("Whiteboard", "chat", ("La partie vient de commencer"), "")
        can.bind("<Button-1>",lambda event:\

                click_souris(event,can,l_nombre,l_image,lp,cp,ligne,colonne,l_items,l_widgets,l_c,memoire,photos,gestion_jeu))

def quitter():
        igs.service_call("Whiteboard","clear", (), "")
        fenetre.destroy()

if __name__ == "__main__":

    # catch SIGINT handler before starting agent
    signal.signal(signal.SIGINT, signal_handler)
    interactive_loop = False

    try:
        opts, args = getopt.getopt(sys.argv[1:], short_flag, long_flag)
    except getopt.GetoptError as err:
        igs.error(err)
        sys.exit(2)
    for o, a in opts:
        if o == "-h" or o == "--help":
            print_usage()
            exit(0)
        elif o == "-v" or o == "--verbose":
            verbose = True
        elif o == "-i" or o == "--interactive_loop":
            interactive_loop = True
        elif o == "-p" or o == "--port":
            port = int(a)
        elif o == "-d" or o == "--device":
            device = a
        elif o == "-n" or o == "--name":
            agent_name = a
        else:
            assert False, "unhandled option"

    igs.agent_set_name(agent_name)
    igs.log_set_console(verbose)
    igs.log_set_file(True, None)
    igs.log_set_stream(verbose)
    igs.set_command_line(sys.executable + " " + " ".join(sys.argv))

    igs.debug(f"Ingescape version: {igs.version()} (protocol v{igs.protocol()})")

    if device is None:
        # we have no device to start with: try to find one
        list_devices = igs.net_devices_list()
        list_addresses = igs.net_addresses_list()
        if len(list_devices) == 1:
            device = list_devices[0]
            igs.info("using %s as default network device (this is the only one available)" % str(device))
        elif len(list_devices) == 2 and (list_addresses[0] == "127.0.0.1" or list_addresses[1] == "127.0.0.1"):
            if list_addresses[0] == "127.0.0.1":
                device = list_devices[1]
            else:
                device = list_devices[0]
            print("using %s as de fault network device (this is the only one available that is not the loopback)" % str(device))
        else:
            if len(list_devices) == 0:
                igs.error("No network device found: aborting.")
            else:
                igs.error("No network device passed as command line parameter and several are available.")
                print("Please use one of these network devices:")
                for device in list_devices:
                    print("	", device)
                print_usage()
            exit(1)

    agent = fenetre()
    #--------déclaration des variables---------------#

    largeur,hauteur=900,700

    ligne,colonne=4,5

    l_widgets=[]

    score=0

    photos=11*[0]

    memoire=[0,0,0,score,-1]

    #lp=hauteur de chaque ligne en pixels

    #cp=largeur de chaque colonne en pixels

    lp,cp=int(hauteur/ligne),int(largeur/colonne)

    l_c=[]#liste qui contient les boutons

    #liste qui  va contenir les images

    l_nombre=ligne*colonne*[0]#liste qui va contenir des nombres

    #--------------création de la fenêtre------------#

    fenetre = Tk()
    gestion_carte=Carte_classe()

    couleur="light blue"

    titre="Jeu de Mémoire "

    taille=str(largeur+150)+'x'+str(hauteur)
    fenetres_interface=fenetre_classe()
    
    fenetres_interface.creer_fenetre(fenetre,taille,titre,couleur)

    fenetre.resizable(width=False,height=False)

    #-création du canvas qui va contenir les données-#

    can=Canvas(fenetre,width=largeur,height=hauteur)

    #le canvas contient le nombre de lignes et de colonnes

    #qui sont déclarées dans les variables

    can.grid(row=0,column=0,rowspan=ligne,columnspan=colonne)

    #affichage du fond d'écran

    #------remplissage des  listes des données-------#


    l_image=gestion_carte.liste_image(11)#contient 11 images dans cet exemple
    gestion_jeu=jeu_classe(can,l_image,ligne,colonne,lp,cp,photos)
    l_nombre=gestion_jeu.melange(l_nombre)

    for i in range(len(l_nombre)):

        l_nombre[i]=l_nombre[i]%10+1

    #liste de nombres mélangés
   
    l_items=gestion_jeu.affiche_fond(can,l_image,l_nombre,ligne,colonne)

    RE="REJOUER"

    V10='verdana 10 bold'

    V15="Il faut cliquer\ndeux fois\n consécutivement\n sur la\n même image"

    V20='verdana 20 bold'

    t1=Label(fenetre,text=V15,bg='light blue',font=V10 )

    t1.grid(row=0,column=6,sticky=W+E)

    l_c.append(t1)

    t2=Button(fenetre,text=RE,font='verdana 15 bold',width=2,bg='ivory')

    t2.bind("<Button-1>",lambda event:jouer(fenetre,can,l_image,l_nombre,ligne,colonne,l_widgets))

    t2.grid(row=1,column=6,sticky=W+E)

    l_c.append(t2)

    t3=Label(fenetre,text="SCORE\n            .",bg='orange',font=V10)

    t3.grid(row=2,column=6,sticky=W+E)

    l_c.append(t3)

    t4=Button(fenetre,text='Quitter',font='verdana 15 bold',width=2,bg='ivory',command=quitter)

    t4.grid(row=3,column=6,sticky=W+E)

    l_c.append(t4)

    jouer(fenetre,can,l_image,l_nombre,ligne,colonne,l_widgets,gestion_jeu)

    
    

    igs.observe_agent_events(on_agent_event_callback, agent)
    igs.observe_freeze(on_freeze_callback, agent)


    igs.start_with_device(device, port)
    

    # catch SIGINT handler after starting agent
    signal.signal(signal.SIGINT, signal_handler)


    fenetre.mainloop()
    if igs.is_started():
        igs.stop()
