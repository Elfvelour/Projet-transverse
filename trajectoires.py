#########################################################
# Fichier gérant la trajectoire et l'interface du jeu   #
# Auteur : Flavie BREMAND et Thomas AUBERT              #
#########################################################

import ctypes
import math
import pygame
from monnaie import Pieces
from pygame.sprite import Group

# Permet de désactiver la mise à l'échelle de l'ordinateur
ctypes.windll.user32.SetProcessDPIAware()

pygame.init()

class Sol(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0, 800, 1920, 300)

    def affichage(self, surface):
        pygame.draw.rect(surface, (0, 200, 100), self.rect)

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

    def mouvement(self):
        self.vitesse_y += self.gravite
        self.rect.x += int(self.vitesse_x)
        self.rect.y += int(self.vitesse_y)

    def afficher(self, surface):
        surface.blit(self.image, self.rect)

class Jeu:
    def __init__(self):
        self.ecran = pygame.display.set_mode((1920, 1024), pygame.RESIZABLE)
        self.image_projectile = pygame.image.load("assests/arme_os.png").convert_alpha()
        self.background = pygame.image.load("assests/background3.png").convert()
        self.background = pygame.transform.scale(self.background, (1920, 1024))
        self.sol = Sol()
        self.joueur = Joueur(200, 672, [64, 128])
        self.projectiles_groupe = Group()
        self.piece = Pieces((50, 50))  # Initialisation du système de pièces

    clock = pygame.time.Clock()
    def boucle_principale(self):
        continuer = True

        while continuer:
            self.ecran.blit(self.background, (0, 0))
            pos_souris = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    continuer = False

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.joueur.temps_debut = pygame.time.get_ticks()

                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    puissance = self.joueur.relacher_tir()
                    x_proj, y_proj = self.joueur.position_depart_projectile()
                    projectile = Projectile(x_proj, y_proj, [60, 60], self.image_projectile, self.joueur.angle, puissance)
                    self.projectiles_groupe.add(projectile)
                    self.piece.monnaie_joueur += 1  # Ajout d'une pièce à chaque tir

            if pygame.mouse.get_pressed()[0]:
                self.joueur.charger_tir()

            for projectile in self.projectiles_groupe:
                projectile.mouvement()

            self.sol.affichage(self.ecran)
            self.joueur.affichage(self.ecran, pos_souris)
            for projectile in self.projectiles_groupe:
                projectile.afficher(self.ecran)

            self.piece.afficher_monnaie(self.ecran)
            self.piece.afficher_nombre_pieces(self.ecran)

            pygame.display.update()

            self.clock.tick(110)

        pygame.quit()

if __name__ == '__main__':
    Jeu().boucle_principale()
