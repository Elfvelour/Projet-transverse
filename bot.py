#####################################################
# Fichier de gestion du bot                         #
# Auteurs : Flavie BREMAND et Thomas AUBERT         #
#####################################################

import pygame
import random
import math

# Constantes de difficulté
DIFFICULTE_PLAGE = {
    "FACILE": 250,
    "MOYEN": 150,
    "DIFFICILE": 50
}
difficulte = "FACILE"  # Valeur par défaut

class Bot(pygame.sprite.Sprite):
    def __init__(self, x, y, taille):
        super().__init__()
        self.rect = pygame.Rect(x, y, *taille)
        self.image = pygame.Surface(taille)
        self.image.fill((178, 30, 240))  # Couleur pour le BOT
        self.angle = 0

    def affichage(self, surface):
        surface.blit(self.image, self.rect)

    def obtenir_plage_position(self, joueur_x):
        """Détermine la plage de position horizontale du BOT en fonction de la difficulté."""
        plage = DIFFICULTE_PLAGE.get(difficulte, 250)  # Par défaut, facile
        return joueur_x - plage, joueur_x + plage

    def choisir_position(self, joueur_x):
        """Choisit une position aléatoire dans la plage de positions autour du joueur en fonction de la difficulté."""
        min_x, max_x = self.obtenir_plage_position(joueur_x)
        return random.randint(min_x, max_x)

    def calcul_angle(self, player_x, player_y):
        """Calcule l'angle entre la position du bot et celle du joueur."""
        dx = player_x - self.rect.centerx
        dy = player_y - self.rect.centery
        return math.degrees(math.atan2(-dy, dx))  # Conversion en degrés

    def calcul_puissance(self, target_x):
        """Calcule la puissance du tir en fonction de la distance."""
        distance = abs(target_x - self.rect.centerx)
        return max(min(distance / 200, 1), 0.1)  # Valeur minimale pour éviter un tir nul

    def tir(self, joueur_x, joueur_y):
        """Définit l'angle et la puissance du tir."""
        target_x = self.choisir_position(joueur_x)
        angle = self.calcul_angle(target_x, joueur_y)
        puissance = self.calcul_puissance(target_x)
        return angle, puissance
