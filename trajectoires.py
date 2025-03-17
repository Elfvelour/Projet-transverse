import ctypes
import math
import pygame
from monnaie import Pieces
from pygame.sprite import Group
from bot import Bot

# Permet de désactiver la mise à l'échelle de l'ordinateur
ctypes.windll.user32.SetProcessDPIAware()

pygame.init()

class Joueur(pygame.sprite.Sprite):
    def __init__(self, x, y, taille):
        super().__init__()
        self.rect = pygame.Rect(x, y, taille[0], taille[1])
        self.image = pygame.Surface(taille)
        self.image.fill((169, 169, 169))  # Gris
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
        return puissance

    def rotation_arme(self, pos_souris):
        dx = pos_souris[0] - self.rect.centerx
        dy = pos_souris[1] - self.rect.centery
        self.angle = pygame.math.Vector2(dx, dy).angle_to((1, 0))

    def affichage(self, surface, pos_souris):
        surface.blit(self.image, self.rect)
        self.rotation_arme(pos_souris)

        # Ligne blanche de visée
        x_fin = self.rect.centerx + math.cos(math.radians(self.angle)) * self.longueur_ligne
        y_fin = self.rect.centery - math.sin(math.radians(self.angle)) * self.longueur_ligne
        pygame.draw.line(surface, (255, 255, 255), self.rect.center, (x_fin, y_fin), 3)

    def position_depart_projectile(self):
        x_depart = self.rect.centerx + math.cos(math.radians(self.angle)) * self.longueur_ligne
        y_depart = self.rect.centery - math.sin(math.radians(self.angle)) * self.longueur_ligne
        return x_depart, y_depart

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, taille, image, angle, puissance):
        super().__init__()
        self.image = pygame.transform.scale(image, (taille[0], taille[1]))
        self.rect = pygame.Rect(x, y, taille[0], taille[1])
        self.angle = angle
        self.vitesse = 5 + (16 * puissance)
        self.vitesse_x = math.cos(math.radians(self.angle)) * self.vitesse
        self.vitesse_y = -math.sin(math.radians(self.angle)) * self.vitesse
        self.gravite = 0.2
        self.sol_y = 800
        self.explosion = pygame.image.load("assests/explosion.png").convert_alpha()
        self.explosion_rect = None
        self.temps_explosion = None  # Temps de début de l'explosion
        self.a_touche_bot = False  # Pour éviter de donner des pièces par erreur

    def mouvement(self, bot, piece, jeu):
        """ Gère le mouvement du projectile et ses collisions """
        if self.temps_explosion:
            # Vérifier si l'explosion doit être retirée après 500ms
            if pygame.time.get_ticks() - self.temps_explosion > 500:
                jeu.projectiles_groupe.remove(self)  # Supprime le projectile après explosion
                jeu.explosion_active = False  # Marquer que l'explosion est terminée
            return

        # Appliquer la gravité
        self.vitesse_y += self.gravite
        self.rect.x += int(self.vitesse_x)
        self.rect.y += int(self.vitesse_y)

        # Vérifier la collision avec le bot
        if self.rect.colliderect(bot.rect) and not self.a_touche_bot:
            self.explosion_rect = self.rect.copy()  # L'explosion apparaît à l'impact
            self.temps_explosion = pygame.time.get_ticks()  # Démarre le timer d'explosion
            self.a_touche_bot = True  # Marque que le bot a été touché
            piece.monnaie_joueur += 10  # Ajoute 10 pièces
            jeu.explosion_active = True  # Marquer qu'une explosion est en cours
            return

        # Vérifier la collision avec le sol
        if self.rect.bottom >= self.sol_y:
            self.explosion_rect = self.rect.copy()  # Explosion à l'impact
            self.temps_explosion = pygame.time.get_ticks()
            jeu.explosion_active = True  # Marquer qu'une explosion est en cours
            return

        # Si le projectile sort de l’écran, on le supprime **sans donner de pièces**
        if self.rect.top > 1024 or self.rect.right < 0 or self.rect.left > 1920:
            jeu.projectiles_groupe.remove(self)  # Supprime sans explosion
            return

    def afficher(self, surface):
        """ Affiche le projectile ou l'explosion """
        if self.temps_explosion:
            surface.blit(self.explosion, self.explosion_rect)  # Affiche l'explosion
        else:
            surface.blit(self.image, self.rect)
