##################################################
# Fichier gérant la gestion de la monnaie du jeu #
# Auteur : Marques Noémie                        #
##################################################
import pygame

class Pieces (pygame.sprite.Sprite):
    def __init__(self, taille):
        super().__init__()
        self.x = 0
        self.y = 10
        self.taille = taille
        self.monnaie_joueur = 100
        self.jauge_monnaie = (0,0,0,50)

    def afficher(self, surface) :
        pygame.draw.rect(surface,(0,0,255), self.jauge_monnaie)