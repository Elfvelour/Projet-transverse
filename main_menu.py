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
    def __init__(self, texte, x, y, couleur, police,action):
        self.texte = texte
        self.axe_x = x
        self.axe_y = y
        self.couleur = couleur
        self.action = action
        self.police_caractere = pygame.font.Font(None, police)

    def CreationBouton(self, ecran):

        # Ajouter le texte sur le bouton
        texte_surface = self.police_caractere.render(self.texte, True, 'white')  # Couleur du texte : blanc

        # Créer un rectangle pour le bouton
        bouton_creer = pygame.Rect(self.axe_x, self.axe_y,200,50)

        # Dessiner le rectangle sur l'écran avec la couleur spécifiée
        pygame.draw.rect(ecran, self.couleur, bouton_creer)
        texte_rectangle = texte_surface.get_rect(center=bouton_creer.center)

        #animation du bouton
        if self.BoutonClique():
            pygame.draw.rect(ecran,'dark red', bouton_creer,0,5)
        else:
            pygame.draw.rect(ecran, 'red', bouton_creer, 0, 5)
        ecran.blit(texte_surface, texte_rectangle)


    def BoutonClique(self):
        pos_souris=pygame.mouse.get_pos()
        clique_gauche=pygame.mouse.get_pressed()[0]
        bouton_creer=pygame.Rect(self.axe_x, self.axe_y, 200, 50)
        if clique_gauche and bouton_creer.collidepoint(pos_souris) and self.action:
            return True
        else:
            return False



menu=Menu()

# Définir les paramètres du bouton
texte = "jouer"
x = 650
y = 310
couleur = 'red'  # Rouge
police = 36

#bouton jouer
mon_bouton_jouer = Bouton(texte, x, y, couleur, police,True)
#bouton quitter
mon_bouton_quitter=Bouton("quitter",650,390,'red',36,True)

# Boucle principale
running = True
while running:
    # Remplir l'écran avec une couleur de fond
    ecran.fill('white')  # Noir

    # Créer et affiche les boutons
    mon_bouton_jouer.CreationBouton(ecran)
    mon_bouton_quitter.CreationBouton(ecran)
    print(mon_bouton_jouer.BoutonClique())
    # Mettre à jour l'affichage
    pygame.display.flip()
    if mon_bouton_quitter.BoutonClique()==True:
        running = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False




