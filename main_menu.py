
##############################################
###### Programme Python menu principal  ######
###### Auteur: Timothée Girault         ######
###### Version: 1.5                    ######
##############################################

##############################################
# Importation des fonctions externes

import pygame
import math
import time
#initialisation de pygame
pygame.init()
clock = pygame.time.Clock()
#initialisation musique
pygame.mixer.init()
pygame.mixer.music.load("assests/sons/The Red Sun in the Sky 100 - HQ.mp3")
pygame.mixer.music.play(-1)
##############################################
#Constantes
hauteur=790
largeur=1530
ecran=pygame.display.set_mode((largeur,hauteur))
police=36
logo_para=pygame.image.load("assests/images/menup/logo_paraV2.png")
fond_ecran=pygame.image.load("assests/images/menup/backgroundV2.png")
logo_jeux=pygame.image.load("assests/images/menup/logo_jeux.png")
action_bouton1=True
##############################################

#classe du menu
class Menu:

    def __init__(self):
        #defini la taille de l'écran
        self.ecran=pygame.display.set_mode((largeur,hauteur))
        #donne le nom a la page
        pygame.display.set_caption("BOW MASTER")
        #liste de boutons
        self.boutons=[]
        #le jeux a commencé ou non
        self.en_train_de_jouer=True
    def lancerjeu(self):
        # Remplir l'écran avec une couleur de fond
        ecran.fill('white')  # blanc
        mon_bouton_parametre.CreationBouton(ecran)
        ecran.blit(fond_ecran, (0, 0))
        ecran.blit(logo_jeux, ((largeur-700)/2,80 ))
        # Créer et affiche les boutons
        mon_bouton_jouer.CreationBouton(ecran)
        mon_bouton_quitter.CreationBouton(ecran)
        ecran.blit(logo_para, (1470, 730))
        print(mon_bouton_jouer.BoutonClique())
        # Mettre à jour l'affichage
        pygame.display.flip()

#classe des boutons
class Bouton:
    def __init__(self, texte, x, y, couleur,hauteur,longueur,police,action):
        self.texte = texte
        self.axe_x = x
        self.axe_y = y
        self.couleur = couleur
        self.hauteur = hauteur
        self.longueur = longueur
        self.action = action
        self.police_caractere =pygame.font.Font("assests/images/affichage/04B_30__.TTF", 40)

    def CreationBouton(self, ecran):

        # Ajouter le texte sur le bouton
        texte_surface = self.police_caractere.render(self.texte, True, 'white')  # Couleur du texte : blanc

        # Créer un rectangle pour le bouton
        bouton_creer = pygame.Rect(self.axe_x, self.axe_y,self.hauteur,self.longueur)

        # Dessiner le rectangle sur l'écran avec la couleur spécifiée
        pygame.draw.rect(ecran, self.couleur, bouton_creer)
        texte_rectangle = texte_surface.get_rect(center=bouton_creer.center)

        #animation du bouton
        if self.couleur == 'red':
            if self.BoutonClique():
                pygame.draw.rect(ecran,'dark red', bouton_creer,0,5)
            else:
                pygame.draw.rect(ecran, 'red', bouton_creer, 0, 5)
        ecran.blit(texte_surface, texte_rectangle)


    def BoutonClique(self):
        pos_souris=pygame.mouse.get_pos()
        clique_gauche=pygame.mouse.get_pressed()[0]
        bouton_creer=pygame.Rect(self.axe_x, self.axe_y, 300, 50)
        if clique_gauche and bouton_creer.collidepoint(pos_souris):
            return True
        else:
            return False

def changer_musique(musique):
    pygame.mixer.music.stop()
    pygame.mixer.music.load(musique)
    pygame.mixer.music.play(-1)

def changer_bruitage(bruitage):
    son=pygame.mixer.Sound(bruitage)
    son.play()
    time.sleep(1)
    son.stop()



menu=Menu()

# Définir les paramètres du bouton
texte = "jouer"
x = (largeur-300)/2
y = (hauteur-70)/2
couleur = 'red'  # Rouge
police = 36
hauteur_b = 300
longueur_b = 70
x_p=largeur-60
y_p=hauteur-60

#bouton jouer
mon_bouton_jouer = Bouton(texte, x, y, couleur,hauteur_b,longueur_b, police,action_bouton1)
#bouton quitter
mon_bouton_quitter=Bouton("quitter",x,y+120,'red',300,70,36,True)
#bouton parametre
mon_bouton_parametre=Bouton("",x_p,y_p,'white',50,50,36,True)

# Boucle principale
running = True
while running:
    Menu.lancerjeu(self=menu)
    if mon_bouton_jouer.BoutonClique() and action_bouton1==True:
        action_bouton1=False
        changer_musique("assests/sons/chill.wav")
    if mon_bouton_quitter.BoutonClique()==True:
        running = False
    if mon_bouton_parametre.BoutonClique()==True:
        changer_bruitage("assests/sons/bruitage_bouton.mp3")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False




