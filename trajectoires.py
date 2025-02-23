import ctypes
import math
import pygame
from pygame.sprite import Group

# Permet de désactiver la mise à l'échelle de l'ordinateur
ctypes.windll.user32.SetProcessDPIAware()

pygame.init()  # Initialisation de pygame avant toute autre instruction


class Sol(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0, 800, 1920, 300)

    def affichage(self, surface):
        pygame.draw.rect(surface, (0, 200, 100), self.rect)  # Sol vert


class Joueur(pygame.sprite.Sprite):
    def __init__(self, x, y, taille):
        super().__init__()
        self.x = x
        self.y = y
        self.taille = taille
        self.rect = pygame.Rect(x, y, self.taille[0], self.taille[1])
        self.a_tirer = False
        self.tir_auto = 35838248
        self.direction = 1
        self.vitesse_y = 0
        self.vitesse_x = 0
        self.image_joueur = pygame.Surface(self.taille)
        self.image_joueur.fill((169, 169, 169))  # Le joueur est maintenant gris
        self.angle = 0

    def rotation_arme(self, pos_souris):
        # Position du "côté gauche" de l'arc (à gauche du joueur)
        x_gauche = self.rect.left - 20  # Décalage sur la gauche du joueur
        y_gauche = self.rect.centery  # Centre vertical du joueur

        dx = pos_souris[0] - x_gauche  # Utiliser la souris à gauche du joueur
        dy = pos_souris[1] - y_gauche
        self.angle = pygame.math.Vector2(dx, dy).angle_to((1, 0))

        # Image de l'arme
        self.image_joueur_rot = pygame.Surface((64, 128), pygame.SRCALPHA)
        pygame.draw.line(self.image_joueur_rot, (255, 255, 255), (0, 64), (64, 64), 5)  # Dessin de l'arc
        self.image_joueur_rot = pygame.transform.rotate(self.image_joueur_rot, self.angle)
        self.rect = self.image_joueur_rot.get_rect(center=self.rect.center)  # Utilise `rect` pour ajuster la position

    def affichage(self, surface, pos_souris):
        surface.blit(self.image_joueur, self.rect)  # Afficher le joueur (le rectangle gris)
        self.rotation_arme(pos_souris)
        surface.blit(self.image_joueur_rot, self.rect)  # Afficher l'arme


class Projectyles(pygame.sprite.Sprite):
    def __init__(self, x, y, taille, image, angle):
        super().__init__()
        self.x = x
        self.y = y
        self.taille = taille
        self.image = image
        self.image = pygame.transform.scale(self.image, (self.taille[0], self.taille[1]))  # Redimensionner l'image
        self.rect = pygame.Rect(self.x, self.y, self.taille[0], self.taille[1])
        self.angle = angle  # Angle du tir

        # Calcul du mouvement du projectile en fonction de l'angle
        self.vitesse = 5  # Vitesse du projectile (ajustable)
        self.vitesse_x = math.cos(math.radians(self.angle)) * self.vitesse  # Vitesse horizontale
        self.vitesse_y = -math.sin(math.radians(self.angle)) * self.vitesse  # Inverser la direction verticale

    def afficher(self, surface):
        surface.blit(self.image, self.rect)

    def mouvement(self):
        self.rect.x += self.vitesse_x
        self.rect.y += self.vitesse_y


class Jeu:
    def __init__(self):
        self.ecran = pygame.display.set_mode((1920, 1024), pygame.RESIZABLE)
        self.image = pygame.image.load("logo.png").convert()
        pygame.display.set_icon(self.image)

        # Chargement et redimensionnement de l'image de fond
        self.background = pygame.image.load("background3.png").convert()
        self.background = pygame.transform.scale(self.background,
        (self.ecran.get_width(), self.ecran.get_height()))  # Étire le fond

        # Sol
        self.sol = Sol()

        self.joueur_x, self.joueur_y = 200, 400
        self.taille = [64, 128]  # Taille initiale du joueur (avant redimensionnement)
        self.joueur = Joueur(self.joueur_x, self.joueur_y, self.taille)
        self.projectiles_groupe = Group()
        self.gravite = (0, 0.01)
        self.resistance = (0, 0)

    def gravite_jeu(self):
        self.joueur.vitesse_y += self.gravite[1]  # Augmente la vitesse vers le bas
        self.joueur.rect.y += self.joueur.vitesse_y  # Applique la vitesse au joueur

        # Empêche de tomber sous le sol
        if self.joueur.rect.bottom >= self.sol.rect.top:
            self.joueur.rect.bottom = self.sol.rect.top
            self.joueur.vitesse_y = 0

    def boucle_principale(self):
        continuer = True

        while continuer:
            self.ecran.blit(self.background, (0, 0))  # Affichage du fond redimensionné
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    continuer = False
                elif event.type == pygame.VIDEORESIZE:
                    self.ecran = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

                    # Mise à jour de l'image de fond lors du redimensionnement
                    self.background = pygame.image.load("background3.png").convert()
                    self.background = pygame.transform.scale(self.background, (event.w, event.h))

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:  # 1 = Bouton gauche de la souris
                        self.joueur.a_tirer = True  # Active le tir du joueur

            # Affichage de la trajectoire avant le tir
            pos_souris = pygame.mouse.get_pos()

            # Tirer un projectile
            if self.joueur.a_tirer:
                if len(self.projectiles_groupe) < self.joueur.tir_auto:
                    # L'arme est maintenant à gauche du joueur, et le projectile part de cette position
                    projectile = Projectyles(self.joueur.rect.left - 20, self.joueur.rect.centery, [20, 20],
                    self.joueur.image_joueur, self.joueur.angle)
                    self.projectiles_groupe.add(projectile)  # Ajout au groupe
                self.joueur.a_tirer = False  # Empêcher le tir continu

            # Mise à jour des projectiles
            for projectile in self.projectiles_groupe:
                projectile.mouvement()  # Appel de la méthode sans l'argument "2"
                if projectile.rect.right >= self.ecran.get_width() or projectile.rect.top <= 0 or projectile.rect.bottom >= self.ecran.get_height():
                    self.projectiles_groupe.remove(projectile)

            # Affichage des éléments
            self.sol.affichage(self.ecran)
            self.gravite_jeu()
            self.joueur.affichage(self.ecran, pos_souris)
            for projectile in self.projectiles_groupe:
                projectile.afficher(self.ecran)

            pygame.display.update()

        pygame.quit()


if __name__ == '__main__':
    Jeu().boucle_principale()
