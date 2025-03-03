import sys

##############################################
###### Programme Python menu principal  ######
###### Auteur: Timothée Girault         ######
###### Version: 1.0                     ######
##############################################

##############################################
# Importation des fonctions externes

import pygame
#initialisation de pygame
pygame.init()
#initialisation musique
pygame.mixer.init()
pygame.mixer.music.load("The Red Sun in the Sky 100 - HQ.mp3")
pygame.mixer.music.play()
##############################################
#Constantes
hauteur=500
largeur=500
ecran=pygame.display.set_mode((largeur,hauteur))
jaune=(255,255,0)
police=36

##############################################


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

    def ajout_boutons(self,bouton):
        self.boutons.append(bouton)

    def lancer_jeu(self):
        while self.en_train_de_jouer:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.en_train_de_jouer = False
                    pygame.quit()
                    sys.exit()

#Classe pour les boutons
class bouton:

    def __initialistion__(self,texte,x,y,couleur,largeur,hauteur):
        self.texte=texte
        self.axe_x=x
        self.axe_y=y
        self.couleur=couleur
        self.largeur=largeur
        self.hauteur=hauteur
        self.action=0
        self.police_caractere=pygame.font.Font(None,police)

    def CreationBouton(self):
        bouton_creer=pygame.Rect((self.axe_x,self.axe_y,self.largeur,self.hauteur))
        pygame.draw.rect(ecran,jaune,bouton_creer)





menu=Menu()
mon_bouton=bouton()
menu.ajout_boutons(mon_bouton)
#lancement du menu
menu.lancer_jeu()