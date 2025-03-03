##################################################
# Fichier gérant la gestion de la monnaie du jeu #
# Auteure : Marques Noémie                       #
##################################################

import pygame

# Création de la classe qui va gérer la monnaie
class Pieces (pygame.sprite.Sprite):
    def __init__(self, taille):
        super().__init__()
        self.x = 0
        self.y = 0
        self.taille = (70,70)
        self.monnaie_joueur = 100
        self.monnaie_depart = 100
        self.image_monnaie = pygame.image.load('assests/image_piece.png')
        self.image_monnaie = pygame.transform.scale(self.image_monnaie, self.taille)
        self.rect_monnaie = self.image_monnaie.get_rect()
        self.font_piece = pygame.font.Font(None, 40)
        self.font_piece = pygame.font.Font("assests/04B_30__.TTF", 40)

    def afficher_monnaie(self, surface):
        surface.blit(self.image_monnaie, (self.x, self.y))

    def afficher_nombre_pieces(self, surface):
        texte = self.font_piece.render(f"{self.monnaie_joueur}", True, (255, 255, 255)) #texte du nombre de pièce
        surface.blit(texte, (self.x + 80, self.y + 20))  # Affichage à côté de la pièce

