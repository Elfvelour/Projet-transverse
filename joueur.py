#####################################################
# Fichier de gestion du joueur                      #
# Auteurs : Flavie BREMAND et Thomas AUBERT         #
#####################################################

import pygame
import math
import json
from menu_joueur import *

clock = pygame.time.Clock()


class Joueur(pygame.sprite.Sprite):  # Hérite de Sprite pour permettre les collisions, affichages, etc.
    def __init__(self, x, y, taille, perso, arme):
        super().__init__()

        self.donnees_json = self.charger_donnees_json("gestion_stats.json")  # Charge les données (stats, images...) depuis le fichier JSON
        self.joueur = perso  # Code du personnage (ex: "P1")
        self.arme = arme     # Code de l’arme (ex: "A1")
        self.image_perso = self.obtenir_image_perso(perso, arme)  # Charge l'image du personnage en fonction du code perso+arme

        for item in self.donnees_json:  # Recherche les PV et dégâts correspondant au personnage et à l'arme choisis
            if item["code P"] == perso and item["code A"] == arme:
                self.pv_max = item["pv"]            # PV max du joueur
                self.pv = item["pv"]                # PV actuels
                self.degat = item["degat"]          # Dégâts infligés par son arme
                self.joueur_touche = 0              # Compteur de touches reçues (pour debug/stat)
                break


        self.rect = pygame.Rect(x, y, taille[0], taille[1])  # Position et taille du joueur sur l'écran

        self.angle = 0             # Angle de tir
        self.charge_tir = 0        # Niveau de puissance du tir
        self.max_charge = 60       # Puissance maximale que peut atteindre un tir
        self.temps_debut = None    # Temps au moment du clic pour commencer la charge
        self.longueur_ligne = 50   # Longueur de la ligne blanche de visée

        self.collisions_joueur = 0  # Compteur général pour les collisions subies

    def affichage(self, surface, pos_souris):  # Affichage du joueur à l'écran
        offset_x = -100  # Décalage horizontal (pour centrer l’image du joueur)
        offset_y = -50   # Décalage vertical (même but)

        # Affiche l’image du joueur à sa position ajustée
        surface.blit(self.image_perso, (self.rect.x + offset_x, self.rect.y + offset_y))

        # Affiche la ligne blanche de visée (indique la direction du tir)
        self.rotation_arme(pos_souris)
        x_fin = self.rect.centerx + math.cos(math.radians(self.angle)) * self.longueur_ligne
        y_fin = self.rect.centery - math.sin(math.radians(self.angle)) * self.longueur_ligne
        pygame.draw.line(surface, (255, 255, 255), self.rect.center, (x_fin, y_fin), 3)

    def rotation_arme(self, pos_souris):  # Rotation du bras/tir en fonction de la souris
        dx = pos_souris[0] - self.rect.centerx
        dy = pos_souris[1] - self.rect.centery

        # Calcule l'angle entre le centre du joueur et la souris
        nouvel_angle = pygame.math.Vector2(dx, dy).angle_to((1, 0))

        # N’enregistre le nouvel angle que si le changement est significatif
        if abs(nouvel_angle - self.angle) > 1:
            self.angle = nouvel_angle
            print(f"Angle de l'arme : {self.angle}")  # Debug

    def position_depart_projectile(self):  # Détermine la position de départ du projectile
        x_depart = self.rect.centerx + math.cos(math.radians(self.angle)) * self.longueur_ligne
        y_depart = self.rect.centery - math.sin(math.radians(self.angle)) * self.longueur_ligne
        print(f"Position de départ du projectile : ({x_depart}, {y_depart})")  # Debug
        return x_depart, y_depart


    def charger_donnees_json(self, fichier):  # Charge les données JSON du fichier
        with open(fichier, "r", encoding="utf-8") as f:
            return json.load(f)


    def obtenir_image_perso(self, personnage, arme):  # Récupère l’image du personnage selon les codes P et A
        for item in self.donnees_json:
            if item["code P"] == personnage and item["code A"] == arme:
                image = pygame.image.load(item["image_perso"]).convert_alpha()
                return pygame.transform.scale(image, (150, 190))  # Redimensionnement
        # Image par défaut si aucun match trouvé
        return pygame.image.load("assets/images/perso/jean_soma.png").convert_alpha()


    def obtenir_image_arme(self, personnage, arme): # Récupère l’image de l’arme projetée
        for item in self.donnees_json:
            if item["code P"] == personnage and item["code A"] == arme:
                return pygame.image.load(item["image_arme"]).convert_alpha()
        # Projectile par défaut si aucun match trouvé
        return pygame.image.load("assets/images/armes/default_projectile.png").convert_alpha()


    def subir_degats(self, montant):
        self.pv = max(0, self.pv - montant)  # Ne descend jamais en dessous de 0
        self.collisions_joueur += 1  # Incrément statistique pour le fichier historique
        print(f"Le joueur a été touché ! PV restants : {self.pv}") # Debug de vérif


    def afficher_barre_vie(self, surface):
        largeur_max = 100  # Taille fixe de la barre
        hauteur = 10       # Hauteur de la barre
        x = self.rect.centerx - largeur_max // 2  # Position centrée horizontalement
        y = self.rect.top - 60  # Position verticale au-dessus du joueur

        largeur_actuelle = int((self.pv / self.pv_max) * largeur_max)  # Proportion restante
        pygame.draw.rect(surface, (255, 0, 0), (x, y, largeur_max, hauteur))  # Fond rouge (barre de vie vide)
        pygame.draw.rect(surface, (0, 255, 0), (x, y, largeur_actuelle, hauteur))  # Barre verte (vie restante)
