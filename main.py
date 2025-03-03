#####################################################
# Fichier de lancement du jeu                       #
# Auteurs: Flavie BREMAND et Thomas AUBERT          #
#####################################################

import pygame
from trajectoires import *
from monnaie import *
from bot import *

class Sol(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0, 800, 1920, 300)

    def affichage(self, surface):
        pygame.draw.rect(surface, (0, 200, 100), self.rect)


class Jeu:
    def __init__(self):
        self.ecran = pygame.display.set_mode((1920, 1024), pygame.RESIZABLE)
        self.image_projectile = pygame.image.load("arme_os.png").convert_alpha()
        self.background = pygame.image.load("background3.png").convert()
        self.background = pygame.transform.scale(self.background, (1920, 1024))
        self.sol = Sol()
        self.joueur = Joueur(200, 672, [64, 128])
        self.projectiles_groupe = Group()
        self.piece = Pieces((50, 50))
        self.bot = Bot(1920 - 100, 672, [64, 128])

    def boucle_principale(self):
        clock = pygame.time.Clock()  # Limiter les FPS
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
                    self.piece.monnaie_joueur += 1

            if pygame.mouse.get_pressed()[0]:
                self.joueur.charger_tir()

            # Mouvements et affichage des projectiles
            for projectile in self.projectiles_groupe:
                projectile.mouvement()

            # Mise à jour des éléments à l'écran
            self.sol.affichage(self.ecran)
            self.joueur.affichage(self.ecran, pos_souris)
            self.bot.affichage(self.ecran)
            for projectile in self.projectiles_groupe:
                projectile.afficher(self.ecran)

            self.piece.afficher_monnaie(self.ecran)
            self.piece.afficher_nombre_pieces(self.ecran)

            pygame.display.update()
            clock.tick(110)  # Limiter les FPS à 30

        pygame.quit()

if __name__ == '__main__':
    Jeu().boucle_principale()
