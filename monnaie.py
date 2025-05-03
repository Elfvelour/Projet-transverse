##################################################
# Fichier gérant la gestion de la monnaie du jeu #
# Auteure : Marques Noémie                       #
##################################################

import pygame
from joueur import *

# Création de la classe qui va gérer la monnaie
class Pieces (pygame.sprite.Sprite):
    def __init__(self, taille):
        super().__init__()
        #Affichage du compteur de pièce
        self.x = 0
        self.y = 0
        self.taille = (70,70)
        self.monnaie_joueur = 100
        self.monnaie_depart = 100
        self.image_monnaie = pygame.image.load('assets/images/affichage/image_piece.png')
        self.image_monnaie = pygame.transform.scale(self.image_monnaie, self.taille)
        self.rect_monnaie = self.image_monnaie.get_rect()
        self.font_piece = pygame.font.Font(None, 40)
        self.font_piece = pygame.font.Font("assets/images/affichage/04B_30__.TTF", 40)
        self.bouton_x = 1900
        self.bouton_y = 20

        #ajout d'un bouton de l'ulti, animation coffre ouvert et fermé
        self.image_coffre_ferme = pygame.image.load("assets/images/affichage/coffre_ferme.png")
        self.image_coffre_ouvert = pygame.image.load("assets/images/affichage/coffre_ouvert.png")

        self.image_bouton = self.image_coffre_ferme
        self.image_bouton = pygame.transform.scale(self.image_bouton, (211, 157))  # Ajuste la taille du bouton
        self.rect_bouton = self.image_bouton.get_rect(topright=(self.bouton_x, self.bouton_y))

        #Etat du coffre au lancement du jeu
        self.coffre_ouvert = False

        #temps de recharge pour le bonus de pièce
        self.dernier_ulti = 0  # temps en ms
        self.temps_cooldown = 10000  # 10 secondes en ms


    def afficher_monnaie(self, surface):  #affichage de l'image de pièce
        surface.blit(self.image_monnaie, (self.x, self.y))

    def afficher_nombre_pieces(self, surface):  #affichage du nombe de pièce
        texte = self.font_piece.render(f"{self.monnaie_joueur}", True, (255, 255, 255)) #texte du nombre de pièce
        surface.blit(texte, (self.x + 80, self.y + 20))  # Affichage à côté de la pièce

    def afficher_bouton(self, surface): #affichage du bouton boost
        surface.blit(self.image_bouton, self.rect_bouton)
        texte = self.font_piece.render("Barre espace pour Boost", True, (255, 255, 255))
        surface.blit(texte, (self.bouton_x - 780, self.bouton_y - 10))
        texte_2 = self.font_piece.render("Attendre 3 tirs", True, (221, 226, 63))
        surface.blit(texte_2, (self.bouton_x - 500, self.bouton_y + 150))
        if self.coffre_ouvert and pygame.time.get_ticks() - self.dernier_ulti >= 1000:  #Affichage du coffre en fonction du temps
            self.image_bouton = self.image_coffre_ferme  #coffre fermé si l'ulti pas utilisé depuis un certain temps
            self.image_bouton = pygame.transform.scale(self.image_bouton, (211, 157))
            self.rect_bouton = self.image_bouton.get_rect(topright=(self.bouton_x, self.bouton_y))
            self.coffre_ouvert = False  #coffre ouvert si bouton cliqué et temps de couldown

    def ulti(self, jeu): #gestion du boost de pièce et de l'affichage du coffre
        temps_actuel = pygame.time.get_ticks()
        if temps_actuel - self.dernier_ulti >= self.temps_cooldown:
            jeu.joueur.degat += 10
            self.image_bouton = self.image_coffre_ouvert  #changement du coffre fermé en ouvert
            self.image_bouton = pygame.transform.scale(self.image_bouton, (211, 157))
            self.rect_bouton = self.image_bouton.get_rect(topright=(self.bouton_x, self.bouton_y))
            self.coffre_ouvert = True
            self.dernier_ulti = temps_actuel

    def verifier_clic(self, event, jeu):  #vérification de l'activation de l'ulti, si espace est appuyé
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.ulti(jeu)

    def verif_coffre(self):
        if self.monnaie_joueur >= 100 and self.coffre_ouvert:
            self.image_bouton = self.image_coffre_ferme  # Afficher le coffre fermé
            self.image_bouton = pygame.transform.scale(self.image_bouton, (211, 157))  # Ajuste la taille du bouton
            self.rect_bouton = self.image_bouton.get_rect(topright=(self.bouton_x, self.bouton_y))
            self.coffre_ouvert = False

