
##############################################
###### Programme Python menu principal  ######
###### Auteur : Timothée Girault        ######
###### Version: 2.4                     ######
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
#donne le nom à la fenêtre
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
pygame.mixer.music.load("assets/sons/super-ambiance.mp3")
pygame.mixer.music.play(-1)

#chargements des textures
logo_ecran=pygame.image.load("assets/images/menup/logo.png")
logo_para=pygame.image.load("assets/images/menup/logo_paraV2.png")
fond_ecran=pygame.image.load("assets/images/menup/logoia3.jpg")
logo_ar=pygame.image.load("assets/images/menup/back_bouton.png")
fond_jeu=pygame.image.load("assets/images/menup/fond_jeu_partie.png")
logo_next=pygame.image.load("assets/images/menup/Forward_button_white2.png")
logo_next_inverse=pygame.image.load("assets/images/menup/Forward_buttonwhite_inverse.png")
logo_pause=pygame.image.load("assets/images/menup/pause4.png")
logo_play=pygame.image.load("assets/images/menup/play3.png")

#met le logo du jeu en haut à gauche à la place du logo pygame
pygame.display.set_icon(logo_ecran)

#creation des images cliquables
# logo play/pause
image_rect = logo_next.get_rect() # création de la zone cliquable
image_rect.topleft = (x_white, y_white) # Position de l'image sur l'écran
# logo en arrière
image_rect_2 = logo_next_inverse.get_rect()
image_rect_2.topleft = (x_white-500, y_white)

#creation de la variable globale pour arrêter et jouer de la musique
switch_musique=True
##############################################

# lance le menu principal sans les boutons de la fonction affichage_menu_bouton
def lancerjeuv3():
    # Remplir l'écran avec une couleur de fond
    ecran.fill('white')  # blanc
    #creation des boutons paramètre et retour en arrière
    mon_bouton_parametre.creation_bouton(ecran)
    mon_bouton_ar.creation_bouton(ecran)
    ecran.blit(fond_ecran, (0, 0))

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
        self.police_caractere =pygame.font.Font("assets/images/affichage/04B_30__.TTF", police)

    def creation_bouton(self, ecran):

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
            if self.bouton_clique():
                pygame.draw.rect(ecran,(255, 215, 0), bouton_creer,border_radius=10) #jaune doré
                pygame.draw.rect(ecran, "black", (self.axe_x, self.axe_y, self.longueur, self.hauteur), 2, border_radius=10)
            else:
                pygame.draw.rect(ecran, self.couleur, bouton_creer,border_radius=10)
                pygame.draw.rect(ecran, "black", (self.axe_x, self.axe_y, self.longueur, self.hauteur), 2, border_radius=10)
        #affiche le bouton
        ecran.blit(texte_surface, texte_rectangle)

    @staticmethod
    # créer le menu paramètre
    def menu_parametre():
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
        police=pygame.font.Font("assets/images/affichage/04B_30__.TTF", 45)

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

    @staticmethod
    # créer le menu des règles
    def menu_regle():
        couleur_param = (0, 0, 0, 192)  # noir transparent
        taille_param = (50, 50, 1800, 800)  # paramètre du rectangle paramètre
        surface_param = pygame.Surface(pygame.Rect(taille_param).size,pygame.SRCALPHA)  # création de la surface translucide
        pygame.draw.rect(surface_param, couleur_param, surface_param.get_rect())  # création du rectangle

        # Création de la zone de texte pour les règles
        police = pygame.font.Font("assets/images/affichage/04B_30__.TTF", 50)
        texte_1 = police.render("REGLES", True, "white")  # affichage du texte
        position_texte = (taille_param[0] + 775, taille_param[1]+ 50 )  # Position du texte dans le rectangle

        police = pygame.font.Font("assets/images/affichage/04B_30__.TTF", 35)
        texte_2 = police.render("Le but est simple! Eliminer l'adversaire et vous gagnez! Pour le", True, "white")
        position_texte_2 = (taille_param[0]+10 , taille_param[1] + 200)

        texte_3=police.render("toucher, il suffit de maintenir le clic gauche appuye",True,"white")
        position_texte_3=(taille_param[0]+150,taille_param[1]+300)

        texte_4=police.render("pour augmenter la puissance de votre tir. Avant de relacher",True,"white")
        position_texte_4=(taille_param[0]+50,taille_param[1]+400)

        texte_5=police.render("votre clic, viser pour obtenir une belle trajectoire. Et",True,"white")
        position_texte_5=(taille_param[0]+100,taille_param[1]+500)

        texte_6=police.render("normalement, la victoire sera a vous! :)",True,"white")
        position_texte_6=(taille_param[0]+300,taille_param[1]+600)

        # Quand on clique sur le bouton jouer, le menu règle est affiché.
        if  mon_bouton_jouer.action == False:
            mon_bouton_ok.creation_bouton(ecran)
            ecran.blit(surface_param, taille_param)  # mise à jour de l'écran
            ecran.blit(texte_1, position_texte)
            ecran.blit(texte_2, position_texte_2)
            ecran.blit(texte_3, position_texte_3)
            ecran.blit(texte_4, position_texte_4)
            ecran.blit(texte_5, position_texte_5)
            ecran.blit(texte_6, position_texte_6)

        #si on clique sur le bouton ok, cela lance la sélection des personnages
        if mon_bouton_ok.bouton_clique():
            return True

        return None

    #verifie si le clic gauche de la souris clique sur le bouton
    def bouton_clique(self):
        pos_souris=pygame.mouse.get_pos()
        clique_gauche=pygame.mouse.get_pressed()[0]
        bouton_creer=pygame.Rect(self.axe_x, self.axe_y, 300, 70)
        if clique_gauche and bouton_creer.collidepoint(pos_souris):
            return True
        else:
            return False

    # gère les évènements du menu principal
    def evenement(self):
        #si on clique le bouton "jouer", on lance le menu des personnages
        if mon_bouton_jouer.bouton_clique() and mon_bouton_jouer.action == True:
            mon_bouton_jouer.action = False
        #si on clique sur le bouton quitter cela fait quitter le jeu
        if mon_bouton_quitter.bouton_clique():
            return False
        # si on clique le bouton paramètre, on lance le bruitage de bouton (on ne peut pas le lancer pendant les règles)
        if mon_bouton_parametre.bouton_clique() and mon_bouton_parametre.action==True and mon_bouton_jouer.action == True:
            mon_bouton_parametre.action=False
            musique.jouer_bruitage('clique')
        #si on clique sur le bouton revenir en arrière, on peut revenir au menu principal
        if mon_bouton_ar.bouton_clique() and self.action == False:
            self.action=True

class Musique:
    #bibliothèque des sons
    def __init__(self):
        self.bruitage={
            'clique':pygame.mixer.Sound("assets/sons/bruitage_bouton2.mp3"),
            'potion':pygame.mixer.Sound("assets/sons/potion_bruit.mp3"),
            'canard':pygame.mixer.Sound("assets/sons/canard.mp3"),
            'os':pygame.mixer.Sound("assets/sons/os.mp3"),
            'noel':pygame.mixer.Sound("assets/sons/mere_noel.mp3"),
        }
        #bibliothèque des chansons
        self.chansons={
            'super_ambiance': "assets/sons/super-ambiance.mp3",
            'Lo-Fi':"assets/sons/lo-fi-synthwave.mp3",
            'musique_c': "assets/sons/The Red Sun in the Sky 100 - HQ.mp3",
            'chill':"assets/sons/chill.wav",
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
            pygame.mixer.music.stop()
            pygame.mixer.music.load(self.chansons[nom])
            pygame.mixer.music.play(-1)

    #change les musiques en avant lorsque qu'on appuie sur le bouton musique
    def changement_de_musique(self):
        self.indice_musique=(self.indice_musique + 1) % len(self.liste_chansons) # modulo de la bibliothèque pour avoir une boucle infini de chanson
        nom_chansons=self.liste_chansons[self.indice_musique] # récupère le nom de la chanson dans la liste
        self.jouer_musique(nom_chansons)

    # change les musiques en arrière lorsque qu'on appuie sur le bouton musique
    def inverse_changement_de_musique(self):
        self.indice_musique = (self.indice_musique -1) % len(self.liste_chansons)  # modulo de la bibliothèque pour avoir une boucle infini de chanson
        nom_chansons = self.liste_chansons[self.indice_musique]  # récupère le nom de la chanson dans la liste
        self.jouer_musique(nom_chansons)

#initialisation de la classe musique dans la boucle
musique=Musique()


# détecte si on clique sur le logo d'une image
def logo_clique(image_rect):
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
    # Si le logo a été cliqué avec un intervalle d'au moins 0.5 seconde
    if logo_clique(logo_rect) and (temps_actuel-musique.dernier_clique > musique.delai/2):
        musique.dernier_clique = temps_actuel
        if switch_musique:
            # Arrête la musique et affiche le logo play
            pygame.mixer.music.pause()
            switch_musique = False
        else:
            # Lance la musique et affiche le logo pause
            pygame.mixer.music.unpause()
            switch_musique = True
    return switch_musique

# Gère les différents évènements du menu paramètre
def evenement_para():
    global switch_musique
    temps_actuel=time.time()
    #si on clique sur le logo next et que l'intervalle de temps est supérieur à 1s entre les cliques
    if logo_clique(image_rect) and (temps_actuel-musique.dernier_clique > musique.delai):
        #on change de musique +1 dans la liste de musique
        switch_musique = True
        musique.dernier_clique=temps_actuel
        musique.changement_de_musique()
    # si on clique sur le logo next inverse et que l'intervalle de temps est supérieur à 1s entre les cliques
    if logo_clique(image_rect_2) and (temps_actuel-musique.dernier_clique > musique.delai):
        # on change de musique -1 dans la liste de musique
        switch_musique = True
        musique.dernier_clique = temps_actuel
        musique.inverse_changement_de_musique()

# vérifie quand on clique sur le logo paramètre la page se lancer
def verif_para():
    action_para = mon_bouton_parametre.action
    # si on appuie sur le logo paramètre, on peut lancer, changer la musique et mettre en pause le jeu
    if action_para == False :
        Bouton.menu_parametre()
        evenement_para()
        ecran.blit(logo_ar, (0, 0))


#verifie les différents évènements pour chaque bouton
def verif_boutons():
    Bouton.evenement(mon_bouton_jouer)
    Bouton.evenement(mon_bouton_quitter)

#affiche les boutons et le logo du menu principal
def affichage_menu_bouton():
    # Créer et affiche les boutons jouer et quitter
    mon_bouton_jouer.creation_bouton(ecran)
    mon_bouton_quitter.creation_bouton(ecran)

# affiche et gère le menu paramètre ainsi que son logo
def affichage_parametre():
    ecran.blit(logo_para, (x_p, y_p))
    Bouton.evenement(mon_bouton_parametre)
    verif_para()

def affichage_menu():
    lancerjeuv3()
    action_para=mon_bouton_parametre.action
    #on affiche les boutons tant qu'on n'appuie pas sur le bouton jouer pour lancer le jeu (on a action=True pour chaque bouton par défaut).
    if mon_bouton_jouer.action == True:
        affichage_menu_bouton()
    verif_boutons()

    # si on appuie sur jouer cela fait lancer le menu règle
    if mon_bouton_jouer.action == False and action_para == True:
        return True
    #si on appuie sur quitter cela fait quitter le jeu
    if Bouton.evenement(mon_bouton_quitter) == False and action_para == True:
        return False

    return None



#bouton jouer
mon_bouton_jouer = Bouton(texte, x, y, couleur,longueur_b,hauteur_b, police_b,action_bouton1)
#bouton quitter
mon_bouton_quitter=Bouton("quitter",x,y+120,couleur,longueur_b,hauteur_b,police_b,True)
#bouton paramètre
mon_bouton_parametre=Bouton("",x_p,y_p,'white',60,60,police_b,True)
#bouton retour en arrière pour quitter le menu paramètre
mon_bouton_ar=Bouton("",0,0,'white',50,50,police_b,True)
#bouton ok
mon_bouton_ok=Bouton("OK",x,y+200,couleur,longueur_b,hauteur_b,police_b,True)

def boucle_menu():
    # Boucle principale
    running = True
    while running:
        affichage_menu()
        affichage_parametre()
        Bouton.menu_regle()
        pygame.display.flip()
        # boucle tant qu'on n'a pas appuyé sur le bouton quitter (running=False)
        #si on a appuyé sur jouer et ok
        if affichage_menu() and Bouton.menu_regle():
            # réactivation du menu musique après les règles
            mon_bouton_jouer.action = True
            return True
        if affichage_menu() == False:
            running = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()