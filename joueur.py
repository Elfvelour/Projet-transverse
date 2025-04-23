#####################################################
# Fichier de gestion du joueur                      #
# Auteurs : Flavie BREMAND et Thomas AUBERT         #
#####################################################

import pygame
import math
import json
from menu_joueur import *

clock = pygame.time.Clock()


class Joueur(pygame.sprite.Sprite):
    def __init__(self, x, y, taille, perso, arme):
        super().__init__()
        self.donnees_json = self.charger_donnees_json("gestion_stats.json")  # chargement des données
        self.joueur = perso
        self.arme = arme
        self.image_perso = self.obtenir_image_perso(perso, arme)
        # Récupération des PV et dégâts depuis les données JSON
        for item in self.donnees_json:
            if item["code P"] == perso and item["code A"] == arme:
                self.pv_max = item["pv"]
                self.pv = item["pv"]
                self.degat = item["degat"]
                break

        self.rect = pygame.Rect(x, y, taille[0], taille[1])
        self.angle = 0
        self.charge_tir = 0
        self.max_charge = 60
        self.temps_debut = None  # Temps au début du clic
        self.longueur_ligne = 50  # Longueur de la ligne blanche

    def charger_tir(self):
        if self.temps_debut:
            temps_ecoule = pygame.time.get_ticks() - self.temps_debut
            self.charge_tir = min(temps_ecoule // 10, self.max_charge)

    def relacher_tir(self):
        puissance = self.charge_tir / self.max_charge
        self.charge_tir = 0
        self.temps_debut = None
        print(f"Puissance du tir : {puissance:.2f}")  # Debug
        return puissance

    def rotation_arme(self, pos_souris):
        dx = pos_souris[0] - self.rect.centerx
        dy = pos_souris[1] - self.rect.centery
        nouvel_angle = pygame.math.Vector2(dx, dy).angle_to((1, 0))

        # Vérifie si l'angle a changé (ajouter une tolérance pour éviter des changements minimes)
        if abs(nouvel_angle - self.angle) > 1:  # Si l'angle a changé d'au moins 1 degré
            self.angle = nouvel_angle
            print(f"Angle de l'arme : {self.angle}")  # Debug

    def affichage(self, surface, pos_souris):
        # Ajustement de l'image
        offset_x = -100
        offset_y = -50

        # Dessiner l'image du personnage avec les offsets
        surface.blit(self.image_perso, (self.rect.x + offset_x, self.rect.y + offset_y))

        # Rotation de l'arme et affichage de la ligne de visée
        self.rotation_arme(pos_souris)
        x_fin = self.rect.centerx + math.cos(math.radians(self.angle)) * self.longueur_ligne
        y_fin = self.rect.centery - math.sin(math.radians(self.angle)) * self.longueur_ligne
        pygame.draw.line(surface, (255, 255, 255), self.rect.center, (x_fin, y_fin), 3)

    def position_depart_projectile(self):
        x_depart = self.rect.centerx + math.cos(math.radians(self.angle)) * self.longueur_ligne
        y_depart = self.rect.centery - math.sin(math.radians(self.angle)) * self.longueur_ligne
        print(f"Position de départ du projectile : ({x_depart}, {y_depart})")  # Debug
        return x_depart, y_depart

    def charger_donnees_json(self, fichier):
        with open(fichier, "r", encoding="utf-8") as f:
            return json.load(f)

    def obtenir_image_perso(self, personnage, arme):
        for item in self.donnees_json:
            if item["code P"] == personnage and item["code A"] == arme:
                image = pygame.image.load(item["image_perso"]).convert_alpha()
                # Redimensionner l'image à la taille souhaitée
                return pygame.transform.scale(image, (150, 190))
        return pygame.image.load("assets/images/perso/jean_soma.png").convert_alpha()

    def obtenir_image_arme(self, personnage, arme):
        for item in self.donnees_json:
            if item["code P"] == personnage and item["code A"] == arme:
                return pygame.image.load(item["image_arme"]).convert_alpha()
        return pygame.image.load("assets/images/armes/default_projectile.png").convert_alpha()

    def subir_degats(self, montant):
        """Réduit les points de vie du joueur"""
        self.pv = max(0, self.pv - montant)
        print(f"Le joueur a été touché ! PV restants : {self.pv}")

    def afficher_barre_vie(self, surface):
        """Affiche une barre de vie verte au-dessus du joueur"""
        largeur_max = 100
        hauteur = 10
        x = self.rect.centerx - largeur_max // 2
        y = self.rect.top - 20

        largeur_actuelle = int((self.pv / self.pv_max) * largeur_max)
        pygame.draw.rect(surface, (255, 0, 0), (x, y, largeur_max, hauteur))  # fond rouge
        pygame.draw.rect(surface, (0, 255, 0), (x, y, largeur_actuelle, hauteur))  # barre verte
