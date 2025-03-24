#####################################################
# Fichier de lancement du jeu                       #
# Auteurs: Flavie BREMAND et Thomas AUBERT          #
#####################################################
from main_menu import changer_musique, changer_bruitage
from trajectoires import *
from monnaie import *
from bot import *
from main import *
import json

if __name__ == '__main__':
    Jeu().boucle_principale()
