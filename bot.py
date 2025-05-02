#####################################################
# Fichier de gestion du bot                         #
# Auteurs : Flavie BREMAND et Thomas AUBERT         #
#####################################################

import pygame
import random
from main_menu import *
from jeu import *
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
        self.donnees_json = self.charger_donnees_json("gestion_stats.json")  # chargement des données
        self.image_bot = self.obtenir_image_perso("PB", "A0") #code associé à l'image de "Jean-Soma" et à celui de l'arme par défaut
        # Récupération des PV et dégâts depuis les données JSON
        for item in self.donnees_json:
            if item["code P"] == "PB" and item["code A"] == "A0":
                self.pv_max = item["pv"]
                self.pv = item["pv"]
                self.degat = item["degat"]
                break
        self.rect = pygame.Rect(x, y, 150, 190)
        self.angle = 0

        # animation de réussite après la mort du bot
        self.font = pygame.font.Font(None, 40)
        self.font = pygame.font.Font("assets/images/affichage/04B_30__.TTF", 40)
        self.x_gg = 900
        self.y_gg = 505
        self.taille_gg = (200, 200)
        self.image_gg = pygame.image.load('assets/images/affichage/trophe.png')
        self.image_gg = pygame.transform.scale(self.image_gg, self.taille_gg)
        self.rect_gg = self.image_gg.get_rect(topright=(self.x_gg, self.y_gg - 100))

    def affichage(self, surface):
        surface.blit(self.image_bot, self.rect)

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

    def calcul_angle_parabole(self, dx, dy, vitesse):
        """Calcule l'angle de tir en degrés pour atteindre une cible à dx, dy avec vitesse donnée"""
        g = 7  # gravité
        v2 = vitesse ** 2
        racine = v2 ** 2 - g * (g * dx ** 2 + 2 * dy * v2)

        if racine < 0:
            return 45  # Si pas de solution, angle par défaut

        racine = math.sqrt(racine)
        angle_rad1 = math.atan((v2 + racine) / (g * dx))
        angle_rad2 = math.atan((v2 - racine) / (g * dx))

        # Choix de l'angle le plus grand (tir plus en cloche)
        angle = math.degrees(max(angle_rad1, angle_rad2))
        return angle

    def tir(self, joueur_x, joueur_y):
        """Définit l'angle et la puissance du tir avec une trajectoire balistique réaliste."""
        target_x = self.choisir_position(joueur_x)
        target_y = joueur_y + random.randint(-10, 10)  # Ajouter un peu d'erreur verticale

        dx = target_x - self.rect.centerx
        dy = self.rect.centery - target_y

        tir_vers_gauche = dx < 0
        dx = abs(dx)

        distance = dx
        puissance = max(min(distance / 210, 1), 0.1)
        vitesse = 110 + (7 * puissance)

        angle = self.calcul_angle_parabole(dx, -dy, vitesse)

        if tir_vers_gauche:
            angle = 180 - angle  # Inverser l’angle pour tirer vers la gauche

        return angle, puissance

    def charger_donnees_json(self, fichier):
        with open(fichier, "r", encoding="utf-8") as f:
            return json.load(f)

    def obtenir_image_perso(self, personnage, arme):
        for item in self.donnees_json:
            if item["code P"] == personnage and item["code A"] == arme:
                image = pygame.image.load(item["image_perso"]).convert_alpha()
                # Redimensionner l'image à la taille souhaitée
                return pygame.transform.scale(image, (150, 190))
        return pygame.image.load("assets/images/perso/jean_soma_bot.png").convert_alpha()

    def subir_degats(self, montant):
        """Réduit les points de vie du bot"""
        self.pv = max(0, self.pv - montant)
        print(f"Le bot a été touché ! PV restants : {self.pv}")

    def afficher_barre_vie(self, surface):
        """Affiche une barre de vie verte au-dessus du bot"""
        largeur_max = 100
        hauteur = 10
        x = self.rect.centerx - largeur_max // 2
        y = self.rect.top - 20

        largeur_actuelle = int((self.pv / self.pv_max) * largeur_max)
        pygame.draw.rect(surface, (255, 0, 0), (x, y, largeur_max, hauteur))  # fond rouge
        pygame.draw.rect(surface, (0, 255, 0), (x, y, largeur_actuelle, hauteur))  # barre verte

    #affiche un bouton quitter pour quitter le jeu lorsqu'on a fini le jeu
    def gestion_quitter(self, x, y, couleur, longueur_b, hauteur_b, police_b):
        # bouton quitter
        mon_bouton_quitter_2 = Bouton("quitter", x, y + 120, couleur, longueur_b, hauteur_b, police_b, True)
        mon_bouton_quitter_2.creation_bouton(ecran)
        if mon_bouton_quitter_2.bouton_clique():
            return True
    def afficher_gg(self, surface):  # affichage de la phrase de fin
        surface.blit(self.image_gg, self.rect_gg)
        texte_3 = self.font.render("Ennemi battu !", True, (255, 255, 255))
        Bot.gestion_quitter(self, x, y, couleur, longueur_b, hauteur_b, police_b)
        if Bot.gestion_quitter(self, x, y, couleur, longueur_b, hauteur_b, police_b):
            return True
        surface.blit(texte_3, (self.x_gg, self.y_gg))
