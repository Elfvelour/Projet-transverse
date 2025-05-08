#############################################################
# Fichier de gestion des trajectoires (sol et projectiles)  #
# Auteurs : Flavie BREMAND et Thomas AUBERT                 #
#############################################################

import pygame
import math
from main_menu import Musique

musique = Musique()
clock = pygame.time.Clock()

class Sol(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0, 800, 1920, 300)
        #self.rect = pygame.image.load("assets/images/affichage/toit_immeuble.png").convert()
        self.rect = pygame.image.load("assets/images/affichage/toit_immeuble.png").convert()
        self.rect_position = (0, 800)

    def affichage(self, surface):
        surface.blit(self.rect, self.rect_position)

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, taille, image, angle, puissance, vitesse_initiale, tireur):
        super().__init__()
        self.image = pygame.transform.scale(image, (taille[0], taille[1]))
        self.rect = pygame.Rect(x, y, taille[0], taille[1])
        self.angle = angle
        self.vitesse = vitesse_initiale
        self.vitesse_x = math.cos(math.radians(self.angle)) * self.vitesse
        self.vitesse_y = -math.sin(math.radians(self.angle)) * self.vitesse
        self.gravite = 7
        self.sol_y = 800
        self.explosion = pygame.image.load("assets/images/affichage/explosion.png").convert_alpha()
        self.explosion_size = (100, 100)
        self.explosion = pygame.transform.scale(self.explosion, self.explosion_size)
        self.explosion_rect = None
        self.temps_explosion = None  # Temps de début de l'explosion
        self.a_touche_bot = False  # Pour éviter d'ajouter des pièces par erreur
        self.hors_ecran = False  # True si le projectile est sorti de l'écran
        self.tireur = tireur  # "joueur" ou "bot" pour éviter les mélanges

    def mouvement(self, bot, piece, jeu, sons):
        """Gère le mouvement du projectile et ses collisions"""
        if self.temps_explosion:
            if pygame.time.get_ticks() - self.temps_explosion > 500:
                if self.tireur == "joueur":
                    jeu.projectiles_joueur.remove(self)
                else:
                    jeu.projectiles_bot.remove(self)
                jeu.explosion_active = False
            return
        if self.tireur == "bot" and self.rect.colliderect(jeu.joueur.rect):
            self.creer_explosion(jeu.joueur.rect.centerx, jeu.joueur.rect.centery)
            self.temps_explosion = pygame.time.get_ticks()
            jeu.joueur.subir_degats(jeu.bot.degat)  # Inflige les dégâts du bot
            jeu.explosion_active = True
            print(f"Le projectile du bot a touché le joueur.")  # Debug
            return

        # Appliquer la gravité
        self.vitesse_y += self.gravite
        prev_x, prev_y = self.rect.x, self.rect.y  # Sauvegarde de la position précédente
        self.rect.x += int(self.vitesse_x)
        self.rect.y += int(self.vitesse_y)

        print(f"Position du projectile : ({self.rect.x}, {self.rect.y})")  # Debug

        if self.rect.right < 0 or self.rect.left > 1920 or self.rect.bottom < 0 or self.rect.top > 1024:
            # Le projectile continue sa chute jusqu'à toucher le sol, même hors écran
            self.hors_ecran = True
            print(f"Le projectile est hors écran.")  # Debug

        if self.tireur == "joueur" and self.rect.colliderect(bot.rect) and not self.a_touche_bot:
            self.creer_explosion(bot.rect.centerx, bot.rect.centery)
            self.temps_explosion = pygame.time.get_ticks()
            self.a_touche_bot = True
            piece.monnaie_joueur += 10
            bot.subir_degats(jeu.joueur.degat)  # Inflige les dégâts du joueur
            jeu.explosion_active = True
            print(f"Le projectile a touché le bot.")  # Debug
            musique.jouer_bruitage(sons)
            return

        if self.rect.bottom >= self.sol_y:
            self.creer_explosion(self.rect.centerx, self.sol_y)  # Utilise la position du sol pour l'impact
            self.temps_explosion = pygame.time.get_ticks()
            jeu.explosion_active = True
            print(f"Le projectile a touché le sol.")  # Debug
            if self.tireur == "joueur":
                musique.jouer_bruitage(sons)
            return

    def creer_explosion(self, x, y):
        explosion_size = (50, 50)
        self.explosion_rect = pygame.Rect(
            x - explosion_size[0] // 2,  # Centrer horizontalement l'explosion sur l'impact
            y - explosion_size[1],  # Placer le bas de l'explosion sur la surface du sol
            explosion_size[0],
            explosion_size[1]
        )

    def afficher(self, surface):
        if self.temps_explosion:
            surface.blit(self.explosion, self.explosion_rect)
        else:
            surface.blit(self.image, self.rect)


class Trajectoire:
    def __init__(self):
        self.temps_chargement = 0
        self.temps_debut = 0

    def start_charging(self):
        self.temps_debut = pygame.time.get_ticks()

    def stop_charging_and_compute_speed(self, masse):
        self.temps_chargement = (pygame.time.get_ticks() - self.temps_debut) / 1000  # en secondes
        if self.temps_chargement > 3:
            self.temps_chargement = 3
        facteur = 2000  #ajuster ce facteur pour équilibrer gameplay vs physique
        energie = facteur * self.temps_chargement
        return math.sqrt((3 * energie) / masse)
