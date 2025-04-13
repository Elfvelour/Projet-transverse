#####################################################
# Fichier de lancement du jeu                       #
# Auteurs: Flavie BREMAND et Timothée GIRAULT       #
#####################################################

import pygame
from jeu import Jeu
from menu_joueur import *
from main_menu import *

if __name__ == "__main__":
    # Initialisation Pygame
    pygame.init()

    # Création de la fenêtre avant tout chargement d'image
    screen = pygame.display.set_mode((1920, 1010))
    pygame.display.set_caption("BowMaster")

    # Lancement du jeu
    while True :
        lancement = affichage_menu()
        verif_para()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                lancement = False
                pygame.quit()
        if lancement == False :
            joueur, arme = run_character_menu()
            jeu = Jeu(screen, joueur, arme)
            jeu.boucle_principale()
        elif lancement == 3 :   #3 est la valeur que retourne la fonction si on appuie sur le bouton quitter
            break

