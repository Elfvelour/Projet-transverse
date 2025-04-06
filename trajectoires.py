import ctypes
import math
import pygame
from monnaie import Pieces
from pygame.sprite import Group
from bot import Bot
import json

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

import pygame
import math

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, taille, image, angle, puissance, tireur):
        super().__init__()
        self.image = pygame.transform.scale(image, (taille[0], taille[1]))
        self.rect = pygame.Rect(x, y, taille[0], taille[1])
        self.angle = angle
        self.vitesse = 5 + (16 * puissance)
        self.vitesse_x = math.cos(math.radians(self.angle)) * self.vitesse
        self.vitesse_y = -math.sin(math.radians(self.angle)) * self.vitesse
        self.gravite = 0.2
        self.sol_y = 800
        self.explosion = pygame.image.load("assests/images/affichage/explosion.png").convert_alpha()
        self.explosion_size = (100, 100)
        self.explosion = pygame.transform.scale(self.explosion, self.explosion_size)
        self.explosion_rect = None
        self.temps_explosion = None  # Temps de début de l'explosion
        self.a_touche_bot = False  # Pour éviter d'ajouter des pièces par erreur
        self.hors_ecran = False  # True si le projectile est sorti de l'écran
        self.tireur = tireur  # "joueur" ou "bot" pour éviter les mélanges

        print(f"🎯 Projectile ({self.tireur}) créé à ({x}, {y}) avec angle {self.angle}° et vitesse ({self.vitesse_x}, {self.vitesse_y})")

    def mouvement(self, bot, piece, jeu):
        """Gère le mouvement du projectile et ses collisions"""
        if self.temps_explosion:
            if pygame.time.get_ticks() - self.temps_explosion > 500:
                print(f"⏳ Explosion terminée, suppression du projectile ({self.tireur})")
                if self.tireur == "joueur":
                    jeu.projectiles_joueur.remove(self)
                else:
                    jeu.projectiles_bot.remove(self)
                jeu.explosion_active = False
            return

        # Appliquer la gravité
        self.vitesse_y += self.gravite
        prev_x, prev_y = self.rect.x, self.rect.y  # Sauvegarde de la position précédente
        self.rect.x += int(self.vitesse_x)
        self.rect.y += int(self.vitesse_y)

        print(f"🚀 Projectile ({self.tireur}) position: ({self.rect.x}, {self.rect.y}) - Vitesse: ({self.vitesse_x}, {self.vitesse_y})")

        if self.rect.right < 0 or self.rect.left > 1920 or self.rect.bottom < 0 or self.rect.top > 1024:
            # Le projectile continue sa chute jusqu'à toucher le sol, même hors écran
            self.hors_ecran = True

        # Vérifier la collision avec le bot (uniquement si c'est le joueur qui tire)
        if self.tireur == "joueur" and self.rect.colliderect(bot.rect) and not self.a_touche_bot:
            print(f"💥 Collision avec le bot ! Impact en ({self.rect.centerx}, {self.rect.centery})")
            self.creer_explosion(bot.rect.centerx, bot.rect.centery)
            self.temps_explosion = pygame.time.get_ticks()
            self.a_touche_bot = True
            piece.monnaie_joueur += 10
            jeu.explosion_active = True
            return

        # Vérifier la collision avec le sol
        if self.rect.bottom >= self.sol_y:
            print(f"💥 Collision avec le sol en ({self.rect.centerx}, {self.sol_y})")
            self.creer_explosion(self.rect.centerx, self.sol_y)
            self.temps_explosion = pygame.time.get_ticks()
            jeu.explosion_active = True
            return

    def creer_explosion(self, x, y):
        """Crée une explosion à une position précise"""
        print(f"💥 Explosion créée à ({x}, {y}), rect: {self.explosion_rect}")
        explosion_size = (50, 50)
        self.explosion_rect = pygame.Rect(
            x - explosion_size[0] // 2,
            y - explosion_size[1] // 2,
            explosion_size[0],
            explosion_size[1]
        )

    def afficher(self, surface):
        """ Affiche le projectile ou l'explosion """
        if self.temps_explosion:
            surface.blit(self.explosion, self.explosion_rect)  # Affiche l'explosion
        else:
            surface.blit(self.image, self.rect)


class Sol(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0, 800, 1920, 300)

    def affichage(self, surface):
        pygame.draw.rect(surface, (0, 200, 100), self.rect)


class Jeu:
    def __init__(self):
        self.ecran = pygame.display.set_mode((1920,1010), pygame.RESIZABLE)
        self.donnees_json = self.charger_donnees_json("gestion_stats.json")
        self.personnage_actuel = "P1"
        self.arme_actuel = "A1"
        self.image_projectile = self.obtenir_image_projectile(self.personnage_actuel, self.arme_actuel)
        self.background = pygame.image.load("assests/images/menup/backgroundV2.png").convert()
        self.background = pygame.transform.scale(self.background, (1920, 1024))
        self.sol = Sol()
        self.joueur = Joueur(200, 672, [64, 128])

        self.projectiles_joueur = pygame.sprite.Group()
        self.projectiles_bot = pygame.sprite.Group()

        self.piece = Pieces((50, 50))
        self.bot = Bot(1920 - 100, 672, [64, 128])

        self.tour_joueur = True  # Le joueur commence
        self.en_attente = False  # Attente entre les tours
        self.temps_attente = 0  # Temps de début d'attente
        self.explosion_active = False  # True si une explosion est affichée

    def charger_donnees_json(self, fichier):
        with open(fichier, "r", encoding="utf-8") as f:
            return json.load(f)

    def obtenir_image_projectile(self, personnage, arme):
        for item in self.donnees_json:
            if item["code P"] == personnage and item["code A"] == arme :
                return pygame.image.load(item["image_arme"]).convert_alpha()
        return pygame.image.load("assests/default_projectile.png").convert_alpha()

    def boucle_principale(self):
        clock = pygame.time.Clock()
        continuer = True

        while continuer:
            self.ecran.blit(self.background, (0, 0))
            pos_souris = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    continuer = False
                self.piece.verifier_clic(event, self)

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.tour_joueur:
                    self.joueur.temps_debut = pygame.time.get_ticks()

                if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.tour_joueur:
                    puissance = self.joueur.relacher_tir()
                    x_proj, y_proj = self.joueur.position_depart_projectile()
                    projectile = Projectile(x_proj, y_proj, [60, 60], self.image_projectile, self.joueur.angle,
                                            puissance, "joueur")
                    self.projectiles_joueur.add(projectile)
                    self.piece.monnaie_joueur += 1

                    # Début de l'attente avant le tour du bot
                    self.temps_attente = pygame.time.get_ticks()
                    self.en_attente = True
                    self.tour_joueur = False

            if pygame.mouse.get_pressed()[0] and self.tour_joueur:
                self.joueur.charger_tir()

            # Gestion de l'attente entre les tours
            if self.en_attente:
                if pygame.time.get_ticks() - self.temps_attente >= 5000 and not self.explosion_active:
                    # Fin de l'attente, on vérifie si tous les projectiles sont terminés
                    if not self.projectiles_joueur and not self.projectiles_bot:
                        self.en_attente = False

                        if not self.tour_joueur:
                            # 🔹 Le bot joue maintenant
                            angle, puissance = self.bot.tir(self.joueur.rect.centerx, self.joueur.rect.centery)
                            projectile = Projectile(self.bot.rect.centerx, self.bot.rect.centery, [60, 60],
                                                    self.image_projectile, angle, puissance, "bot")
                            self.projectiles_bot.add(projectile)

                            print("🤖 Le bot a tiré !")

                            # 🔸 Préparer le tour du joueur après le tir du bot
                            self.temps_attente = pygame.time.get_ticks()
                            self.en_attente = True
                            self.tour_joueur = True

            for projectile in self.projectiles_joueur:
                projectile.mouvement(self.bot, self.piece, self)

            for projectile in self.projectiles_bot:
                projectile.mouvement(self.bot, self.piece, self)

            self.sol.affichage(self.ecran)
            self.joueur.affichage(self.ecran, pos_souris)
            self.bot.affichage(self.ecran)
            for projectile in self.projectiles_joueur:
                projectile.afficher(self.ecran)

            for projectile in self.projectiles_bot:
                projectile.afficher(self.ecran)

            self.piece.afficher_monnaie(self.ecran)
            self.piece.afficher_nombre_pieces(self.ecran)
            self.piece.afficher_bouton(self.ecran)

            if self.piece.monnaie_joueur >= 250 :
                self.piece.afficher_gg(self.ecran)

            pygame.display.update()
            clock.tick(110)

        pygame.quit()
