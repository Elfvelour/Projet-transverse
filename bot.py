#############################################################
# Fichier de gestion du bot                                 #
# Auteurs : Flavie BREMAND et Thomas AUBERT                 #
# Aides sur le fichier: Noémie Marques et Timothée Girault  #
#############################################################

import pygame
import random
from main_menu import *
from jeu import *


class Bot(pygame.sprite.Sprite):
    def __init__(self, x, y, taille):
        super().__init__()

        # Chargement des données depuis un fichier JSON
        self.donnees_json = self.charger_donnees_json("gestion_stats.json")  # Chargement des données
        self.image_bot = self.obtenir_image_perso("PB", "A0") # Code associé à l'image de "Jean-Soma" et à celui de l'arme par défaut

        # Récupération des PV et dégâts depuis les données du fichier JSON
        for item in self.donnees_json:
            if item["code P"] == "PB" and item["code A"] == "A0":
                self.pv_max = item["pv"]       # Points de vie maximum
                self.pv = item["pv"]           # Points de vie actuels
                self.degat = item["degat"]     # Dégâts infligés
                break

        self.rect = pygame.Rect(x, y, 150, 190) # Position et taille du bot
        self.angle = 0 # Initialisation de l'angle de tir

        # Paramètres d'affichage de l'écran de victoire du joueur
        self.font = pygame.font.Font("assets/images/affichage/04B_30__.TTF", 50)
        self.x_gg = 750
        self.y_gg = 400
        self.taille_gg = (200, 200)
        self.image_gg = pygame.image.load('assets/images/affichage/trophe.png')
        self.image_gg = pygame.transform.scale(self.image_gg, self.taille_gg)
        self.rect_gg = self.image_gg.get_rect(topright=(self.x_gg, self.y_gg - 100))

        self.collisions_bot = 0  # Compteur des collisions du bot (historique)
        self.victoire_joueur = False # État de victoire du joueur

    def affichage(self, surface):
        """Affiche le bot sur la surface donnée"""
        surface.blit(self.image_bot, self.rect)

    def choisir_position(self, joueur_x):
        """Choisit une position aléatoire autour du joueur pour viser"""
        min_x = joueur_x - 250
        max_x = joueur_x + 250
        return random.randint(min_x, max_x)

    def calcul_angle_parabole(self, dx, dy, vitesse):
        """Calcule l’angle de tir nécessaire pour tirer en cloche à une certaine distance"""
        g = 7  # Gravité utilisée pour le tir
        v2 = vitesse ** 2
        racine = v2 ** 2 - g * (g * dx ** 2 + 2 * dy * v2) # Formule issue des équations du tir balistique

        if racine < 0:
            return 45  # Si pas de solution réelle, angle par défaut

        racine = math.sqrt(racine)
        angle_rad1 = math.atan((v2 + racine) / (g * dx))
        angle_rad2 = math.atan((v2 - racine) / (g * dx))

        # On choisit l’angle le plus élevé pour un tir plus en cloche
        angle = math.degrees(max(angle_rad1, angle_rad2))
        return angle

    def tir(self, joueur_x, joueur_y):
        """Définit l'angle et la puissance du tir avec une trajectoire balistique réaliste
        Vise une position aléatoire autour du joueur"""
        target_x = self.choisir_position(joueur_x)
        target_y = joueur_y + random.randint(-10, 10)  # Ajout d'une erreur verticale aléatoire

        dx = target_x - self.rect.centerx
        dy = self.rect.centery - target_y

        tir_vers_gauche = dx < 0 # On doit tirer à gauche
        dx = abs(dx) # Distance horizontale absolue

        # Calcul de la puissance de tir basée sur la distance
        distance = dx
        puissance = max(min(distance / 210, 1), 0.1) # Valeur minimale pour éviter un tir nul, puissance entre 0.1 et 1
        vitesse = 110 + (7 * puissance) # La vitesse augmente avec la puissance

        angle = self.calcul_angle_parabole(dx, -dy, vitesse) # Calcul de l'angle balistique

        if tir_vers_gauche:
            angle = 180 - angle  # Inverser l’angle pour tirer vers la gauche

        return angle, puissance # Retourne l’angle (degrés) et la puissance (0.1 à 1)

    def charger_donnees_json(self, fichier):
        """Charge un fichier JSON contenant les données du bot"""
        with open(fichier, "r", encoding="utf-8") as f:
            return json.load(f)

    def obtenir_image_perso(self, personnage, arme):
        """Retourne l’image du personnage avec une arme donnée"""
        for item in self.donnees_json:
            if item["code P"] == personnage and item["code A"] == arme:
                image = pygame.image.load(item["image_perso"]).convert_alpha()
                # Redimensionner l'image à la taille souhaitée
                return pygame.transform.scale(image, (150, 190))
        # Image par défaut si rien trouvé
        return pygame.image.load("assets/images/perso/jean_soma_bot.png").convert_alpha()

    def subir_degats(self, montant):
        """Réduit les points de vie du bot"""
        self.pv = max(0, self.pv - montant)
        self.collisions_bot += 1  # Incrémenter le compteur des collisions (historique)
        print(f"Le bot a été touché ! PV restants : {self.pv}")

    def afficher_barre_vie(self, surface):
        """Affiche une barre de vie verte au-dessus du bot"""
        largeur_max = 100
        hauteur = 10
        x = self.rect.centerx - largeur_max // 2
        y = self.rect.top - 20

        largeur_actuelle = int((self.pv / self.pv_max) * largeur_max)
        pygame.draw.rect(surface, (255, 0, 0), (x, y, largeur_max, hauteur))  # Barre rouge (fond)
        pygame.draw.rect(surface, (0, 255, 0), (x, y, largeur_actuelle, hauteur))  # Barre verte (vie)

    def gestion_quitter(self, x, y, couleur, longueur_b, hauteur_b, police_b):
        """Affiche un bouton Quitter et retourne True s'il est cliqué"""
        mon_bouton_quitter_2 = Bouton("quitter", x, y + 120, couleur, longueur_b, hauteur_b, police_b, True)
        mon_bouton_quitter_2.creation_bouton(ecran)
        if mon_bouton_quitter_2.bouton_clique():
            return True

    def afficher_gg(self, surface):
        """Affichage de la phrase de fin (victoire)"""
        self.victoire_joueur = True # Victoire du joueur (historique)
        surface.blit(self.image_gg, self.rect_gg)
        texte_3 = self.font.render("Ennemi battu !", True, (255, 255, 255)) # Texte de victoire affiché

        # Vérifie si on veut quitter
        if Bot.gestion_quitter(self, x, y, couleur, longueur_b, hauteur_b, police_b):
            return True

        surface.blit(texte_3, (self.x_gg, self.y_gg))
