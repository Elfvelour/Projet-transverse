
##############################################
###### Programme Python menu principal  ######
###### Auteur: Timothée Girault         ######
###### Version: 1.6                     ######
##############################################

##############################################
# Importation des fonctions externes

import pygame
#initialisation de pygame
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
##############################################
#Constantes
hauteur,largeur=790,1530
action_bouton1=True
#defini la taille de l'écran
ecran=pygame.display.set_mode((largeur,hauteur))
#donne le nom a la page
pygame.display.set_caption("BOW MASTER")
##############################################
#initialisation musique
#pygame.mixer.music.load("assests/sons/The Red Sun in the Sky 100 - HQ.mp3")
#pygame.mixer.music.play(-1)

#chargements des textures
logo_para=pygame.image.load("assests/images/menup/logo_paraV2.png")
fond_ecran=pygame.image.load("assests/images/menup/backgroundV2.png")
logo_jeux=pygame.image.load("assests/logojeux.png")

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
        #le jeux a commencé ou non
        self.en_train_de_jouer=False

    @staticmethod
    def lancerjeu():
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
        self.police_caractere =pygame.font.Font("assests/images/affichage/04B_30__.TTF", police)

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

    def Evenement(self):
        if mon_bouton_jouer.BoutonClique() and self.action == True:
            self.action = False
            musique.jouer_musique('chill')
        if mon_bouton_quitter.BoutonClique():
            return False
        if mon_bouton_parametre.BoutonClique():
            musique.jouer_bruitage('clique')

class Musique:
    #bibliothèque des sons
    def __init__(self):
        self.bruitage={
            'clique':pygame.mixer.Sound("assests/sons/bruitage_bouton2.mp3"),
            'potion':pygame.mixer.Sound("assests/sons/potion_bruit.mp3"),

        }
        self.chansons={
            'chill':"assests/sons/chill.wav",
            'musique_c':"assests/sons/The Red Sun in the Sky 100 - HQ.mp3",
        }
    def jouer_bruitage(self,nom) :
        if nom in self.bruitage:
            self.bruitage[nom].stop()  # Arrêter le son s'il est déjà en cours de lecture
            self.bruitage[nom].play()

    def jouer_musique(self,nom):
        pygame.mixer.music.load(self.chansons[nom])
        pygame.mixer.music.play(-1)



musique=Musique()

# Définir les paramètres du bouton
texte = "jouer"
x = (largeur-300)/2
y = (hauteur-70)/2
couleur = 'red'  # Rouge
police_b = 40
hauteur_b = 300
longueur_b = 70
x_p=largeur-60
y_p=hauteur-60

#bouton jouer
mon_bouton_jouer = Bouton(texte, x, y, couleur,hauteur_b,longueur_b, police_b,action_bouton1)
#bouton quitter
mon_bouton_quitter=Bouton("quitter",x,y+120,'red',300,70,police_b,True)
#bouton parametre
mon_bouton_parametre=Bouton("",x_p,y_p,'white',50,50,police_b,True)
# Boucle principale
running = True
while running:
    Menu.lancerjeu()
    Bouton.Evenement(mon_bouton_jouer)
    Bouton.Evenement(mon_bouton_quitter)
    Bouton.Evenement(mon_bouton_parametre)
    if Bouton.Evenement(mon_bouton_quitter)==False:
        running = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
