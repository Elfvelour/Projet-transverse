
##############################################
###### Programme Python menu principal  ######
###### Auteur : Timothée Girault         ######
###### Version: 1.9                     ######
##############################################

##############################################
# Importation des fonctions externes
import ctypes
import pygame

from menu_joueur import run_character_menu

#initialisation de pygame
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
# Permet de désactiver la mise à l'échelle de l'ordinateur
ctypes.windll.user32.SetProcessDPIAware()
##############################################
#Constantes
hauteur,largeur=1024,1920
action_bouton1=True
action=False
#defini la taille de l'écran
ecran=pygame.display.set_mode((largeur,hauteur),pygame.RESIZABLE)
#donne le nom a la page
pygame.display.set_caption("BOW MASTER")

# Définir les paramètres du bouton jouer
texte = "jouer"
x = (largeur-300)/2
y = (hauteur-300)
couleur = 'red'  # Rouge
police_b = 40
hauteur_b = 70
longueur_b = 300
#paramètre bouton paramètre
x_p=1860
y_p=930

##############################################
#initialisation musique
pygame.mixer.music.load("assests/sons/The Red Sun in the Sky 100 - HQ.mp3")
pygame.mixer.music.play(-1)

#chargements des textures
logo_ecran=pygame.image.load("assests/images/menup/logo.png")
logo_para=pygame.image.load("assests/images/menup/logo_paraV2.png")
fond_ecran=pygame.image.load("assests/images/menup/ia_raw.jpg")
logo_ar=pygame.image.load("assests/images/menup/back_bouton.png")
fond_jeu=pygame.image.load("assests/images/menup/fond_jeu_partie.png")
#met le logo du jeu en haut à gauche à la place du logo pygame
pygame.display.set_icon(logo_ecran)

#classe du menu
class Menu:

    def __init__(self):
        self.running=True
        self.musique=Musique()
        #liste de boutons
        self.boutons=[#bouton jouer
             #Bouton(texte, x, y, couleur,hauteur_b,longueur_b, police_b,action_bouton1),
             #bouton quitter
             #Bouton("quitter",x,y+120,'red',300,70,police_b,True),
            #bouton parametre
            #Bouton("",x_p,y_p,'white',50,50,police_b,True)
            ]
        #le jeu a commencé ou non
        self.en_train_de_jouer=False

    @staticmethod
    # lance le menu principal sans les boutons de la fonction affichage_menu_bouton
    def lancerjeuV3():
        # Remplir l'écran avec une couleur de fond
        ecran.fill('white')  # blanc
        #creation des boutons paramètre et retour en arrière
        mon_bouton_parametre.CreationBouton(ecran)
        mon_bouton_ar.CreationBouton(ecran)
        ecran.blit(fond_ecran, (0, 0))
        ecran.blit(logo_para, (x_p,y_p))

#classe des boutons
class Bouton:
    def __init__(self, texte, x, y, couleur,longueur,hauteur,police,action):
        self.texte = texte
        self.axe_x = x
        self.axe_y = y
        self.couleur = couleur
        self.hauteur = hauteur
        self.longueur = longueur
        self.action = action
        self.police_caractere =pygame.font.Font("assests/images/affichage/04B_30__.TTF", police)

    def CreationBouton(self, ecran):

        # Ajouter le texte sur le bouton
        texte_surface = self.police_caractere.render(self.texte, True, 'white')  # Couleur du texte : blanc

        # Créer un rectangle pour le bouton
        bouton_creer = pygame.Rect(self.axe_x, self.axe_y,self.longueur,self.hauteur)

        # Dessiner le rectangle sur l'écran avec la couleur spécifiée
        pygame.draw.rect(ecran, self.couleur, bouton_creer,border_radius=10)
        pygame.draw.rect(ecran, "black", (self.axe_x, self.axe_y,self.longueur,self.hauteur), 2,border_radius=10)
        texte_rectangle = texte_surface.get_rect(center=bouton_creer.center)

        #animation du bouton
        if self.couleur == 'red':
            if self.BoutonClique():
                pygame.draw.rect(ecran,'dark red', bouton_creer,2,10)
            else:
                pygame.draw.rect(ecran, 'red', bouton_creer, 2, 10)
        #affiche le bouton
        ecran.blit(texte_surface, texte_rectangle)
    @staticmethod
    def Menu_parametre():
        color=(128, 128, 128)
        pygame.draw.rect(ecran, color,pygame.Rect(560,50,800,900),border_radius=10)
        mon_bouton_musique.CreationBouton(ecran)

    #verifie si le clique gauche de la souris clique sur le bouto,
    def BoutonClique(self):
        pos_souris=pygame.mouse.get_pos()
        clique_gauche=pygame.mouse.get_pressed()[0]
        bouton_creer=pygame.Rect(self.axe_x, self.axe_y, 300, 70)
        if clique_gauche and bouton_creer.collidepoint(pos_souris):
            return True
        else:
            return False

    #gère les évènements du menu principal
    def Evenement(self):
        #si on clique le bouton "jouer", on lance la musique chill et le menu des personnages
        if mon_bouton_jouer.BoutonClique() and mon_bouton_jouer.action == True:
            mon_bouton_jouer.action = False
            musique.jouer_musique('chill')
        #si on clique sur le bouton quitter cela fait quitter le jeu
        if mon_bouton_quitter.BoutonClique():
            return False
        # si on clique le bouton paramètre, on lance le bruitage de bouton
        if mon_bouton_parametre.BoutonClique() and mon_bouton_parametre.action==True:
            mon_bouton_parametre.action=False
            musique.jouer_bruitage('clique')
        #si on clique sur le bouton revenir en arrière, on peut revenir au menu principal
        if mon_bouton_ar.BoutonClique() and self.action == False:
            self.action=True

        #if mon_bouton_musique.BoutonClique():
            #Musique.ChangementdeMusique(self.texte)
class Musique:
    #bibliothèque des sons
    def __init__(self):
        self.bruitage={
            'clique':pygame.mixer.Sound("assests/sons/bruitage_bouton2.mp3"),
            'potion':pygame.mixer.Sound("assests/sons/potion_bruit.mp3"),

        }
        #bibliothèque des chansons
        self.chansons={
            'chill':"assests/sons/chill.wav",
            'musique_c':"assests/sons/The Red Sun in the Sky 100 - HQ.mp3",
        }
    #elle lance des bruitages pour le jeu comme un lancer de potion
    def jouer_bruitage(self,nom) :
        if nom in self.bruitage:
            self.bruitage[nom].stop()  # Arrêter le son s'il est déjà en cours de lecture
            self.bruitage[nom].play()
    #elle lance une musique
    def jouer_musique(self,nom):
        pygame.mixer.music.load(self.chansons[nom])
        pygame.mixer.music.play(-1)
    #change les musiques lorsque qu'on appuie sur le bouton musique
    def ChangementdeMusique(self):
        i=0
        if i>=len(self.chansons):
            i=0
        else:
            i=i+1
            pygame.mixer.music.load(self.chansons[i])
            pygame.mixer.music.play(-1)


#verifie les différents évènements pour chaque bouton
def verif_boutons():
    Bouton.Evenement(mon_bouton_jouer)
    Bouton.Evenement(mon_bouton_quitter)
    Bouton.Evenement(mon_bouton_parametre)
    Bouton.Evenement(mon_bouton_musique)
#affiche les boutons et le logo du menu principal
def affichage_menu_bouton():
    # Créer et affiche les boutons jouer et quitter
    mon_bouton_jouer.CreationBouton(ecran)
    mon_bouton_quitter.CreationBouton(ecran)

def affichage_menu():
    Menu.lancerjeuV3()
    action_para=mon_bouton_parametre.action
    #on affiche les boutons tant qu'on n'appuie pas sur le bouton jouer pour lancer le jeu (on a action=True pour chaque bouton par défaut).
    if mon_bouton_jouer.action == True:
        affichage_menu_bouton()
    else:
        #si on appuie sur jouer, on peut revenir en arrière grace au bouton en arrière
        ecran.blit(logo_ar, (0, 0))
    verif_boutons()

    # si on appuie sur jouer cela fait lancer le jeu
    if mon_bouton_jouer.action == False and action_para == True:
        return True

    #si on appuie sur quitter cela fait quitter le jeu
    if Bouton.Evenement(mon_bouton_quitter) == False and action_para == True:
        return False
# vérifie quand on clique sur le logo paramètre la page se lancer
def verif_para():
    action_para=mon_bouton_parametre.action
    #si on appuie sur le logo paramètre, on peut lancer, changer la musique et mettre en pause le jeu
    if action_para == False:
        Bouton.Menu_parametre()
        ecran.blit(logo_ar, (0, 0))




#bouton jouer
mon_bouton_jouer = Bouton(texte, x, y, couleur,longueur_b,hauteur_b, police_b,action_bouton1)
#bouton quitter
mon_bouton_quitter=Bouton("quitter",x,y+120,couleur,longueur_b,hauteur_b,police_b,True)
#bouton paramètre
mon_bouton_parametre=Bouton("",x_p,y_p,'white',60,60,police_b,True)
#bouton retour en arrière
mon_bouton_ar=Bouton("",0,0,'white',50,50,police_b,True)
#bouton pour changer de musique
mon_bouton_musique=Bouton("Musique",700,500,'white',longueur_b,hauteur_b,police_b,True)
#bouton pour quitter le menu paramètre
mon_bouton_ar2=Bouton("",560,50,'white',50,50,police_b,True)

#initialisation de la classe musique dans la boucle
musique=Musique()


# Boucle principale
running = True
while running:
    affichage_menu()
    verif_para()
    pygame.display.flip()
    #boucle tant qu'on n'a pas appuyé sur le bouton quitter (running=False)
    if affichage_menu() == False:
        running = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

