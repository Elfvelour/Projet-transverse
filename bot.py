#####################################################
# Fichier de gestion du bot                         #
# Auteurs : Flavie BREMAND et Thomas AUBERT         #
#####################################################
import pygame
import random
import math

# Niveau de difficulté (FACILE, MOYEN, DIFFICILE)
difficulte = "FACILE"  # Valeur par défaut

class Bot(pygame.sprite.Sprite):
    def __init__(self, x, y, taille):
        super().__init__()
        self.rect = pygame.Rect(x, y, taille[0], taille[1])
        self.image = pygame.Surface(taille)
        self.image.fill((178, 30, 240))  # Couleur pour le BOT
        self.angle = 0

    def affichage(self, surface):
        surface.blit(self.image, self.rect)

    def obtenir_plage_position(self, joueur_x):
        """
        Détermine la plage de position horizontale du BOT en fonction de la difficulté.
        """
        if difficulte == "FACILE":
            return joueur_x - 250, joueur_x + 250
        elif difficulte == "MOYEN":
            return joueur_x - 150, joueur_x + 150
        elif difficulte == "DIFFICILE":
            return joueur_x - 50, joueur_x + 50
        else:
            return joueur_x - 250, joueur_x + 250  # Par défaut, facile

    def choisir_position(self, joueur_x):
        """
        Choisit une position aléatoire dans la plage de positions autour du joueur en fonction de la difficulté.
        """
        min_x, max_x = self.obtenir_plage_position(joueur_x)
        return random.randint(min_x, max_x)

    def calcul_angle(self, player_x, player_y):
        """Calcule l'angle entre la position du bot et celle du joueur."""
        dx = player_x - self.rect.centerx
        dy = player_y - self.rect.centery
        return pygame.math.Vector2(dx, dy).angle_to((1, 0))

    def calcul_puissance(self, target_x):
        """Calcule la puissance du tir en fonction de la distance."""
        distance = abs(target_x - self.rect.centerx)
        return min(distance / 200, 1)

    def tir(self, joueur_x, joueur_y):
        target_x = self.choisir_position(joueur_x)
        angle = self.calcul_angle(target_x, joueur_y)
        puissance = self.calcul_puissance(target_x)
        return angle, puissance

