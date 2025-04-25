#####################################################
# Fichier de lancement du jeu                       #
# Auteurs: F.BREMAND et T.GIRAULT et N.MARQUES      #
#####################################################

from jeu import Jeu
from menu_joueur import *
from main_menu import boucle_menu

if __name__ == "__main__":

    # Lancement du jeu
    if boucle_menu():
        joueur, arme,sons = run_character_menu()
        jeu = Jeu(screen, joueur, arme,sons)
        jeu.boucle_principale()
