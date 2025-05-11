#############################################################
# Fichier de gestion des trajectoires (sol et projectiles)  #
# Auteurs : Flavie BREMAND et Thomas AUBERT                 #
#############################################################

import pygame
import math
from main_menu import Musique  # Pour jouer les sons d'explosion

musique = Musique()  # Initialisation d'un objet Musique pour les bruitages
clock = pygame.time.Clock()

class Sol(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Chargement de l'image du sol (toit d'immeuble)
        self.rect = pygame.image.load("assets/images/affichage/toit_immeubleV2.png").convert()
        self.rect_position = (0, 800)  # Position de l'image sur l'écran

    def affichage(self, surface):
        surface.blit(self.rect, self.rect_position) # Affiche l'image du sol à sa position

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, taille, image, angle, puissance, vitesse_initiale, tireur):
        super().__init__()
        self.image = pygame.transform.scale(image, (taille[0], taille[1]))  # Mise à l’échelle de l’image du projectile
        self.rect = pygame.Rect(x, y, taille[0], taille[1])  # Rectangle de collision du projectile
        self.angle = angle  # Angle de tir en degrés
        self.vitesse = vitesse_initiale  # Vitesse initiale calculée à partir du temps de charge et de la masse

        # Décomposition de la vitesse en composantes x et y
        self.vitesse_x = math.cos(math.radians(self.angle)) * self.vitesse
        self.vitesse_y = -math.sin(math.radians(self.angle)) * self.vitesse
        self.gravite = 7  # Gravité appliquée à chaque frame
        self.sol_y = 800  # Hauteur du sol pour détecter l'impact

        # Chargement de l'image d'explosion
        self.explosion = pygame.image.load("assets/images/affichage/explosion.png").convert_alpha()
        self.explosion_size = (100, 100)
        self.explosion = pygame.transform.scale(self.explosion, self.explosion_size)
        self.explosion_rect = None  # Rectangle de l'explosion (sera défini à l'impact)
        self.temps_explosion = None  # Moment de l'explosion (pour affichage temporaire)

        self.a_touche_bot = False  # Évite que le bot subisse plusieurs fois le même projectile
        self.hors_ecran = False  # Marque le projectile comme sorti de l'écran
        self.tireur = tireur  # "joueur" ou "bot"

    def mouvement(self, bot, piece, jeu, sons):
        """Déplace le projectile et gère les collisions"""

        if self.temps_explosion:  # Si le projectile est en phase d'explosion
            if pygame.time.get_ticks() - self.temps_explosion > 500:
                if self.tireur == "joueur":  # Supprime le projectile de la liste après explosion
                    jeu.projectiles_joueur.remove(self)
                else:
                    jeu.projectiles_bot.remove(self)
                jeu.explosion_active = False
            return

        # Collision du projectile du bot avec le joueur
        if self.tireur == "bot" and self.rect.colliderect(jeu.joueur.rect):
            self.creer_explosion(jeu.joueur.rect.centerx, jeu.joueur.rect.centery)  # On crée un explosion au point d'impact
            self.temps_explosion = pygame.time.get_ticks()  # On laisse affiché l'explosion le temps défini
            jeu.joueur.subir_degats(jeu.bot.degat)  # Dégâts infligés au joueur
            jeu.explosion_active = True
            print(f"Le projectile du bot a touché le joueur.")  #Debug pour vérification
            return

        self.vitesse_y += self.gravite  # Appliquer la gravité

        # Mise à jour de la position du projectile
        self.rect.x += int(self.vitesse_x)
        self.rect.y += int(self.vitesse_y)

        print(f"Position du projectile : ({self.rect.x}, {self.rect.y})")  # Debug de verif

        # Détecter si le projectile sort de l'écran
        if self.rect.right < 0 or self.rect.left > 1920 or self.rect.bottom < 0 or self.rect.top > 1024:
            self.hors_ecran = True
            print(f"Le projectile est hors écran.") # Debug de verif

        # Collision du projectile du joueur avec le bot
        if self.tireur == "joueur" and self.rect.colliderect(bot.rect) and not self.a_touche_bot:
            self.creer_explosion(bot.rect.centerx, bot.rect.centery)  # On crée l'explosion à l'impact
            self.temps_explosion = pygame.time.get_ticks()
            self.a_touche_bot = True
            piece.monnaie_joueur += 10  # Récompense le joueur
            bot.subir_degats(jeu.joueur.degat)  # Dégâts infligés au bot
            jeu.explosion_active = True
            print(f"Le projectile a touché le bot.") # Debug de verif
            musique.jouer_bruitage(sons) # On joue la musique associée
            return

        # Collision avec le sol
        if self.rect.bottom >= self.sol_y:
            self.creer_explosion(self.rect.centerx, self.sol_y) # On crée l'explosion
            self.temps_explosion = pygame.time.get_ticks()
            jeu.explosion_active = True
            print(f"Le projectile a touché le sol.") # Debug de verif
            if self.tireur == "joueur":
                musique.jouer_bruitage(sons) # On joue la musique associée
            return

    def creer_explosion(self, x, y):
        """Crée un effet d'explosion centré sur les coordonnées (x, y)"""
        explosion_size = (50, 50)  # Taille de l'explosion (en pixels)
        self.explosion_rect = pygame.Rect(  # On associe l'explosion à un rectangle qu'on défini ici
            x - explosion_size[0] // 2,
            y - explosion_size[1],
            explosion_size[0],
            explosion_size[1]
        )

    def afficher(self, surface):
        """Affiche le projectile ou l’explosion à l'écran"""
        if self.temps_explosion:
            surface.blit(self.explosion, self.explosion_rect) # Affichage de l'explosion
        else:
            surface.blit(self.image, self.rect)

class Trajectoire:
    def __init__(self):
        self.temps_chargement = 0  # Durée du clic maintenu
        self.temps_debut = 0  # Heure à laquelle on a commencé à charger

    def start_charging(self):
        self.temps_debut = pygame.time.get_ticks()  #Débute la charge (à l'appui du clic)

    def stop_charging_and_compute_speed(self, masse):
        """Termine la charge et retourne une vitesse initiale réaliste basée sur l’énergie"""
        # Temps de chargement en secondes
        self.temps_chargement = (pygame.time.get_ticks() - self.temps_debut) / 1000
        if self.temps_chargement > 3:
            self.temps_chargement = 3  # Limite la charge à 3 secondes

        facteur = 2000  # facteur de proportion énergie/temps (modifiable pour équilibrage)
        energie = facteur * self.temps_chargement  # énergie accumulée en fonction du temps

        # Formule basée sur E = ½mv² → v = sqrt((2E)/m)
        return math.sqrt((3 * energie) / masse)  # 3 au lieu de 2 pour accentuer le gameplay
