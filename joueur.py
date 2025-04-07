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
    def __init__(self, x, y, taille):
        super().__init__()
        self.donnees_json = self.charger_donnees_json("gestion_stats.json")  # chargement des données
        self.menu_joueur = run_character_menu()
        self.rect = pygame.Rect(x, y, taille[0], taille[1])
        self.image_perso = self.obtenir_image_perso(self.menu_joueur[0], self.menu_joueur[1])
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
        surface.blit(self.image_perso, self.rect)
        self.rotation_arme(pos_souris)

        # Ligne blanche de visée
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
                return pygame.image.load(item["image_perso"]).convert_alpha()
        return pygame.image.load("assests/images/perso/jean_soma.png").convert_alpha()

    def obtenir_image_arme(self, personnage, arme):
        for item in self.donnees_json:
            if item["code P"] == personnage and item["code A"] == arme:
                return pygame.image.load(item["image_arme"]).convert_alpha()
        return pygame.image.load("assests/images/armes/default_projectile.png").convert_alpha()






