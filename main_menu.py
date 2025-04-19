
##############################################
###### Programme Python menu principal  ######
###### Auteur : Timothée Girault        ######
###### Version: 2.3                     ######
##############################################

##############################################
# Importation des fonctions externes
import ctypes
import pygame
import time
#initialisation de pygame
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
# Permet de désactiver la mise à l'échelle de l'ordinateur
ctypes.windll.user32.SetProcessDPIAware()
##############################################
#Constantes
hauteur,largeur=1010,1920
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
couleur =  (230, 170, 80)# jaune moutarde
police_b = 40
hauteur_b = 70
longueur_b = 300
#paramètre bouton paramètre
x_p=1860
y_p=930
#paramètre pour les boutons de changements de musiques
x_white=1100
y_white=250
#paramètre des crédits
y_credit=500

##############################################
#initialisation musique
pygame.mixer.music.load("assests/sons/super-ambiance.mp3")
pygame.mixer.music.play(-1)

#chargements des textures
logo_ecran=pygame.image.load("assests/images/menup/logo.png")
logo_para=pygame.image.load("assests/images/menup/logo_paraV2.png")
fond_ecran=pygame.image.load("assests/images/menup/logoia3.jpg")
logo_ar=pygame.image.load("assests/images/menup/back_bouton.png")
fond_jeu=pygame.image.load("assests/images/menup/fond_jeu_partie.png")
logo_next=pygame.image.load("assests/images/menup/Forward_button_white2.png")
logo_next_inverse=pygame.image.load("assests/images/menup/Forward_buttonwhite_inverse.png")
logo_pause=pygame.image.load("assests/images/menup/pause4.png")
logo_play=pygame.image.load("assests/images/menup/play3.png")

#met le logo du jeu en haut à gauche à la place du logo pygame
pygame.display.set_icon(logo_ecran)

#creation des images cliquables
image_rect = logo_next.get_rect() # création de la zone cliquable
image_rect.topleft = (x_white, y_white) # Position de l'image sur l'écran
image_rect_2 = logo_next_inverse.get_rect()
image_rect_2.topleft = (x_white-500, y_white)

#creation de la variable globale pour arrêter et jouer de la musique
switch_musique=True
##############################################

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
        pygame.draw.rect(ecran, "black", (self.axe_x, self.axe_y, self.longueur, self.hauteur), 2, border_radius=10)
        texte_rectangle = texte_surface.get_rect(center=bouton_creer.center)

        #animation du bouton
        if self.couleur == couleur:
            if self.BoutonClique():
                pygame.draw.rect(ecran,(255, 215, 0), bouton_creer,border_radius=10) #jaune doré
                pygame.draw.rect(ecran, "black", (self.axe_x, self.axe_y, self.longueur, self.hauteur), 2, border_radius=10)
            else:
                pygame.draw.rect(ecran, self.couleur, bouton_creer,border_radius=10)
                pygame.draw.rect(ecran, "black", (self.axe_x, self.axe_y, self.longueur, self.hauteur), 2, border_radius=10)
        #affiche le bouton
        ecran.blit(texte_surface, texte_rectangle)

    @staticmethod
    # créer le menu paramètre
    def Menu_parametre():
        global switch_musique
        couleur_param=(0,0,0,192)#noir transparent
        taille_param=(560,50,800,900)# paramètre du rectangle paramètre
        surface_param=pygame.Surface(pygame.Rect(taille_param).size,pygame.SRCALPHA)# création de la surface translucide
        pygame.draw.rect(surface_param, couleur_param,surface_param.get_rect())# création du rectangle
        ecran.blit(surface_param, taille_param)# mise à jour de l'écran
        ecran.blit(logo_next, (x_white,y_white))# affiche du logo next
        ecran.blit(logo_next_inverse, (x_white-500,y_white))# affiche du logo retour en arrière pour la musique
        switch_musique = bascule_musique(switch_musique)# gère les évènements des boutons play et pause et les affiches

        # Création de la zone de texte pour les crédits
        police=pygame.font.Font("assests/images/affichage/04B_30__.TTF", 45)

        # affichage des crédits
        texte_1 =police.render("Credits", True,"white") # affichage du texte
        position_texte = (taille_param[0] + 275, taille_param[1] + y_credit)  # Position du texte dans le rectangle
        ecran.blit(texte_1, position_texte)

        texte_2 = police.render("Timothee Noemie Flavie", True, "white")
        position_texte = (taille_param[0] + 10, taille_param[1] + y_credit+100)
        ecran.blit(texte_2, position_texte)

        texte_3 = police.render("Raphael Thomas", True,"white")
        position_texte = (taille_param[0] + 125, taille_param[1] + y_credit+200)
        ecran.blit(texte_3, position_texte)


    #verifie si le clic gauche de la souris clique sur le bouton
    def BoutonClique(self):
        pos_souris=pygame.mouse.get_pos()
        clique_gauche=pygame.mouse.get_pressed()[0]
        bouton_creer=pygame.Rect(self.axe_x, self.axe_y, 300, 70)
        if clique_gauche and bouton_creer.collidepoint(pos_souris):
            return True
        else:
            return False

    # gère les évènements du menu principal
    def Evenement(self):
        #si on clique le bouton "jouer", on lance le menu des personnages
        if mon_bouton_jouer.BoutonClique() and mon_bouton_jouer.action == True:
            mon_bouton_jouer.action = False
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

class Musique:
    #bibliothèque des sons
    def __init__(self):
        self.bruitage={
            'clique':pygame.mixer.Sound("assests/sons/bruitage_bouton2.mp3"),
            'potion':pygame.mixer.Sound("assests/sons/potion_bruit.mp3"),

        }
        #bibliothèque des chansons
        self.chansons={
            'super_ambiance': "assests/sons/super-ambiance.mp3",
            'Lo-Fi':"assests/sons/lo-fi-synthwave.mp3",
            'musique_c': "assests/sons/The Red Sun in the Sky 100 - HQ.mp3",
            'chill':"assests/sons/chill.wav",
            }
        self.indice_musique=0
        self.liste_chansons=list(self.chansons.keys())#liste des noms de chansons dans l'ordre
        self.dernier_clique=0 #temps du dernier clic
        self.delai= 1 #delai entre chaque clique voulut en secondes

    #elle lance des bruitages pour le jeu comme un lancer de potion
    def jouer_bruitage(self,nom) :
        if nom in self.bruitage:
            self.bruitage[nom].stop()  # Arrêter le son s'il est déjà en cours de lecture
            self.bruitage[nom].play()

    #elle lance une musique
    def jouer_musique(self,nom):
        if nom in self.chansons:
            pygame.mixer.music.load(self.chansons[nom])
            pygame.mixer.music.play(-1)

    #change les musiques en avant lorsque qu'on appuie sur le bouton musique
    def ChangementdeMusique(self):
        self.indice_musique=(self.indice_musique + 1) % len(self.liste_chansons) # modulo de la bibliothèque pour avoir une boucle infini de chanson
        nom_chansons=self.liste_chansons[self.indice_musique] # récupère le nom de la chanson dans la liste
        self.jouer_musique(nom_chansons)

    # change les musiques en arrière lorsque qu'on appuie sur le bouton musique
    def Inverse_ChangementdeMusique(self):
        self.indice_musique = (self.indice_musique -1) % len(self.liste_chansons)  # modulo de la bibliothèque pour avoir une boucle infini de chanson
        nom_chansons = self.liste_chansons[self.indice_musique]  # récupère le nom de la chanson dans la liste
        self.jouer_musique(nom_chansons)

#initialisation de la classe musique dans la boucle
musique=Musique()


# détecte si on clique sur le logo d'une image
def Logoclique(image_rect):
    pos_souris = pygame.mouse.get_pos()
    clique_gauche = pygame.mouse.get_pressed()[0]
    if clique_gauche and image_rect.collidepoint(pos_souris):
        return True
    else:
        return False

# gère les évènements des boutons play et arrêt
def bascule_musique(switch_musique):
    # prend les variables globales
    global logo_play, logo_pause, x_white, y_white
    temps_actuel = time.time()
    # Détermine le logo actuel en fonction de la variable switch musique : jouer ou arrêt
    logo_actuel = logo_pause if switch_musique else logo_play
    # Afficher le logo actuel
    ecran.blit(logo_actuel, (x_white - 290, y_white - 50))
    # création de la zone cliquable du logo
    logo_rect = logo_actuel.get_rect(topleft=(x_white - 290, y_white - 50))
    # Vérifier si le logo a été cliqué avec un intervalle d'au moins 1 seconde
    if Logoclique(logo_rect) and (temps_actuel-musique.dernier_clique > musique.delai):
        musique.dernier_clique = temps_actuel
        if switch_musique:
            # Arrête la musique et afficher le logo play
            pygame.mixer.music.stop()
            switch_musique = False
        else:
            # Lance la musique et afficher le logo pause
            pygame.mixer.music.play()
            switch_musique = True
    return switch_musique

# Gère les différents évènements du menu paramètre
def Evenement_para():
    global switch_musique
    temps_actuel=time.time()
    #si on clique sur le logo next et que l'intervalle de temps est supérieur à 1 entre les cliques
    if Logoclique(image_rect) and (temps_actuel-musique.dernier_clique > musique.delai):
        switch_musique = True
        musique.dernier_clique=temps_actuel
        musique.ChangementdeMusique()
    if Logoclique(image_rect_2) and (temps_actuel-musique.dernier_clique > musique.delai):
        switch_musique = True
        musique.dernier_clique = temps_actuel
        musique.Inverse_ChangementdeMusique()

# vérifie quand on clique sur le logo paramètre la page se lancer
def verif_para():
    action_para = mon_bouton_parametre.action
    # si on appuie sur le logo paramètre, on peut lancer, changer la musique et mettre en pause le jeu
    if action_para == False:
        Bouton.Menu_parametre()
        ecran.blit(logo_ar, (0, 0))


#verifie les différents évènements pour chaque bouton
def verif_boutons():
    Bouton.Evenement(mon_bouton_jouer)
    Bouton.Evenement(mon_bouton_quitter)
    Bouton.Evenement(mon_bouton_parametre)
    Evenement_para()

#affiche les boutons et le logo du menu principal
def affichage_menu_bouton():
    # Créer et affiche les boutons jouer et quitter
    mon_bouton_jouer.CreationBouton(ecran)
    mon_bouton_quitter.CreationBouton(ecran)


def affichage_menu():
    lancerjeuV3()
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



#bouton jouer
mon_bouton_jouer = Bouton(texte, x, y, couleur,longueur_b,hauteur_b, police_b,action_bouton1)
#bouton quitter
mon_bouton_quitter=Bouton("quitter",x,y+120,couleur,longueur_b,hauteur_b,police_b,True)
#bouton paramètre
mon_bouton_parametre=Bouton("",x_p,y_p,'white',60,60,police_b,True)
#bouton retour en arrière
mon_bouton_ar=Bouton("",0,0,'white',50,50,police_b,True)
#bouton pour quitter le menu paramètre
mon_bouton_ar2=Bouton("",560,50,'white',50,50,police_b,True)

def boucle_menu():
    # Boucle principale
    running = True
    while running:
        affichage_menu()
        verif_para()
        pygame.display.flip()
        # boucle tant qu'on n'a pas appuyé sur le bouton quitter (running=False)
        if affichage_menu()==True:
            return True
        if affichage_menu() == False:
            running = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()