#####################################################
# Fichier de gestion du bot                         #
# Auteurs : Flavie BREMAND et Thomas AUBERT         #
#####################################################

import pygame

class Bot(pygame.sprite.Sprite):
    def __init__(self, x,y, taille):
        super().__init__()
        self.rect = pygame.Rect(x, y, taille[0], taille[1])
        self.image = pygame.Surface(taille)
        self.image.fill((110, 30, 240))  # Bleu

    def affichage(self, surface):
        surface.blit(self.image, self.rect)
