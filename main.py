#####################################################
# Fichier de lancement du jeu                       #
# Auteurs: Flavie BREMAND et ...                    #
#####################################################

import pygame
from trajectoires import *

class Sol(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0, 800, 1920, 300)

    def affichage(self, surface):
        pygame.draw.rect(surface, (0, 200, 100), self.rect)


if __name__ == '__main__':
    Jeu().boucle_principale()
