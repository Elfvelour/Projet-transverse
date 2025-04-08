#####################################################
# Fichier de lancement du jeu                       #
# Auteurs: Flavie BREMAND et Timothée GIRAULT       #
#####################################################

import pygame
from jeu import Jeu
from menu_joueur import *

if __name__ == "__main__":
    # Initialisation Pygame
    pygame.init()

    # Création de la fenêtre avant tout chargement d'image
    screen = pygame.display.set_mode((1920, 1010))
    pygame.display.set_caption("BowMaster")

    # Lancement du jeu
    joueur, arme = run_character_menu()
    jeu = Jeu(screen, joueur, arme)
    jeu.boucle_principale()