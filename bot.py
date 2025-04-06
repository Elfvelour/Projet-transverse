#####################################################
# Fichier de gestion du bot                         #
# Auteurs : Flavie BREMAND et Thomas AUBERT         #
#####################################################
'''
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
'''

import pygame
import random
import math

# Constantes de difficulté
DIFFICULTE_PLAGE = {
    "FACILE": 100,    # Plage grande pour le niveau facile
    "MOYEN": 70,      # Plage moyenne pour le niveau intermédiaire
    "DIFFICILE": 40   # Plage petite pour le niveau difficile
}

difficulte = "FACILE"  # Valeur par défaut

# Classe pour la plage de tir autour du joueur
class BotPlage:
    def __init__(self, difficulte):
        self.difficulte = difficulte

    def obtenir_plage_position(self, joueur_x):
        """Détermine la plage de position horizontale du BOT en fonction de la difficulté."""
        plage = DIFFICULTE_PLAGE.get(self.difficulte, 100)  # Valeur par défaut : FACILE
        # Plage autour du joueur
        return joueur_x - plage, joueur_x + plage

    def choisir_position(self, joueur_x):
        """Choisit une position aléatoire dans la plage de positions autour du joueur."""
        min_x, max_x = self.obtenir_plage_position(joueur_x)
        # On évite que le bot tire trop près de lui en choisissant un point un peu plus éloigné
        # Par exemple, on évite de tirer dans les 20 pixels proches du bot (en fonction de la difficulté)
        distance_min = 20  # Distance minimale avant le tir
        adjusted_min_x = min_x + distance_min
        adjusted_max_x = max_x - distance_min
        return random.randint(adjusted_min_x, adjusted_max_x)

# Classe pour gérer les tirs du bot (calcul de l'angle, de la puissance)
class BotTir:
    def __init__(self):
        pass

    def calcul_angle(self, player_x, player_y, bot_x, bot_y):
        """Calcule l'angle entre la position du bot et celle du joueur."""
        dx = player_x - bot_x
        dy = player_y - bot_y
        return math.degrees(math.atan2(-dy, dx))  # Conversion en degrés

    def calcul_puissance(self, target_x, bot_x):
        """Calcule la puissance du tir en fonction de la distance."""
        distance = abs(target_x - bot_x)
        # On peut utiliser une formule simple pour la puissance, qui sera proportionnelle à la distance
        return max(min(distance / 150, 1), 0.1)  # Distance plus proche = puissance plus forte

    def tirer(self, joueur_x, joueur_y, bot_x, bot_y, difficulte):
        """Fait tirer le bot directement sur la position du joueur avec ajustement selon la difficulté."""
        # On utilise la plage de tir en fonction de la difficulté pour rendre le tir plus ou moins précis
        plage_bot = BotPlage(difficulte)
        target_x = plage_bot.choisir_position(joueur_x)  # Cibler une position aléatoire dans la plage
        target_y = joueur_y  # Le bot tire toujours vers la position Y du joueur
        angle = self.calcul_angle(target_x, target_y, bot_x, bot_y)
        puissance = self.calcul_puissance(target_x, bot_x)
        return angle, puissance

# Classe principale pour le bot
class Bot(pygame.sprite.Sprite):
    def __init__(self, x, y, taille, difficulte):
        super().__init__()
        self.rect = pygame.Rect(x, y, *taille)
        self.image = pygame.Surface(taille)
        self.image.fill((178, 30, 240))  # Couleur pour le BOT
        self.angle = 0
        self.bot_tir = BotTir()  # Instance de BotTir
        self.difficulte = difficulte  # Niveau de difficulté du bot

    def affichage(self, surface):
        surface.blit(self.image, self.rect)

    def tir(self, joueur_x, joueur_y):
        """Le bot tire directement sur le joueur."""
        angle, puissance = self.bot_tir.tirer(joueur_x, joueur_y, self.rect.centerx, self.rect.centery, self.difficulte)
        return angle, puissance
