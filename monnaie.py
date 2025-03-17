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
        self.bouton_x = 1900
        self.bouton_y = 20

        #ajout d'un bouton de l'ulti
        self.image_coffre_ferme = pygame.image.load("assests/coffre_ferme.png")
        self.image_coffre_ouvert = pygame.image.load("assests/coffre_ouvert.png")

        self.image_bouton = self.image_coffre_ferme
        self.image_bouton = pygame.transform.scale(self.image_bouton, (211, 157))  # Ajuste la taille du bouton
        self.rect_bouton = self.image_bouton.get_rect(topright=(self.bouton_x, self.bouton_y))

        self.coffre_ouvert = False

    def afficher_monnaie(self, surface):
        surface.blit(self.image_monnaie, (self.x, self.y))

    def afficher_nombre_pieces(self, surface):
        texte = self.font_piece.render(f"{self.monnaie_joueur}", True, (255, 255, 255)) #texte du nombre de pièce
        surface.blit(texte, (self.x + 80, self.y + 20))  # Affichage à côté de la pièce

    def afficher_bouton(self, surface): #affichage de la phrase
        surface.blit(self.image_bouton, self.rect_bouton)
        texte = self.font_piece.render("Barre espace pour l'ulti", True, (255, 255, 255))
        surface.blit(texte, (self.bouton_x - 780, self.bouton_y - 10))
        texte_2 = self.font_piece.render("100 pieces", True, (221, 226, 63))
        surface.blit(texte_2, (self.bouton_x - 300, self.bouton_y + 150))

    def ulti(self, jeu):
        if self.monnaie_joueur >= 100 and not self.coffre_ouvert:
            self.monnaie_joueur -= 100  # Retirer 100 pièces
            self.image_bouton = self.image_coffre_ouvert  # Afficher le coffre ouvert
            self.image_bouton = pygame.transform.scale(self.image_bouton, (211, 157))  # Ajuste la taille du bouton
            self.rect_bouton = self.image_bouton.get_rect(topright=(self.bouton_x, self.bouton_y))
            self.coffre_ouvert = True
            #jeu.ulti_perso()

    def verifier_clic(self, event, jeu):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.ulti(jeu)

    def verif_coffre(self):
        if self.monnaie_joueur >= 100 and self.coffre_ouvert:
            self.image_bouton = self.image_coffre_ferme  # Afficher le coffre fermé
            self.image_bouton = pygame.transform.scale(self.image_bouton, (211, 157))  # Ajuste la taille du bouton
            self.rect_bouton = self.image_bouton.get_rect(topright=(self.bouton_x, self.bouton_y))
            self.coffre_ouvert = False