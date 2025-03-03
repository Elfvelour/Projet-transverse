import sys

##############################################
###### Programme Python menu principal  ######
###### Auteur: Timothée Girault         ######
###### Version: 1.0                     ######
##############################################

##############################################
# Importation des fonctions externes

import pygame
from pygame import MOUSEBUTTONDOWN

#initialisation de pygame
pygame.init()
#initialisation musique
pygame.mixer.init()
pygame.mixer.music.load("assests\The Red Sun in the Sky 100 - HQ.mp3")
pygame.mixer.music.play()
##############################################
#Constantes
hauteur=790
largeur=1520
ecran=pygame.display.set_mode((largeur,hauteur))
jaune=(255,255,0)
police=36

##############################################

#classe du menu
class Menu:

    def __init__(self):
        #defini la taille de l'écran
        self.ecran=pygame.display.set_mode((largeur,hauteur))
        #donne le nom a la page
        pygame.display.set_caption("BOW MASTER")
        #liste de bouttons
        self.boutons=[]
        #le jeux a commencé ou non
        self.en_train_de_jouer=True
    def lancerjeu(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

#classe des boutons
class Bouton:
    def __init__(self, texte, x, y, couleur, largeur, hauteur, police):
        self.texte = texte
        self.axe_x = x
        self.axe_y = y
        self.couleur = couleur
        self.largeur = largeur
        self.hauteur = hauteur
        self.action = 0
        self.police_caractere = pygame.font.Font(None, police)

    def CreationBouton(self, ecran):
        # Créer un rectangle pour le bouton
        bouton_creer = pygame.Rect(self.axe_x, self.axe_y, self.largeur, self.hauteur)
        # Dessiner le rectangle sur l'écran avec la couleur spécifiée
        pygame.draw.rect(ecran, self.couleur, bouton_creer)
        # Ajouter le texte sur le bouton
        texte_surface = self.police_caractere.render(self.texte, True, (255, 255, 255))  # Couleur du texte : blanc
        texte_rect = texte_surface.get_rect(center=bouton_creer.center)
        ecran.blit(texte_surface, texte_rect)

menu=Menu()

# Définir les paramètres du bouton
texte = "jouer"
x = 650
y = 390
couleur = (255, 0, 0)  # Rouge
largeur = 200
hauteur = 50
police = 36

#bouton jouer
mon_bouton_jouer = Bouton(texte, x, y, couleur, largeur, hauteur, police)
#bouton quitter
mon_bouton_quitter=Bouton("quitter",0,0,(255,0,0),200,50,36)

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Remplir l'écran avec une couleur de fond
    ecran.fill((0, 0, 0))  # Noir

    # Créer et affiche les boutons
    mon_bouton_jouer.CreationBouton(ecran)
    mon_bouton_quitter.CreationBouton(ecran)
    # Mettre à jour l'affichage
    pygame.display.flip()


