import ctypes
from email.mime import image
import time
import pygame
from pygame.sprite import Group


# Permet de désactiver la mise à l'échelle de l'ordinateur
ctypes.windll.user32.SetProcessDPIAware()

pygame.init()  # Initialisation de pygame avant toute autre instruction


class Sol(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0, 800, 1792, 300)

    def affichage(self, image):
        pygame.draw.rect(image, (0, 200, 100), self.rect)


class Joueur(pygame.sprite.Sprite):
    def __init__(self,x,y,taille):
        super().__init__()
        self.x = x
        self.y = y
        self.taille = taille
        self.rect = pygame.Rect(x, y, self.taille[0], self.taille[1])
        self.a_tirer = False
        self.tir_auto = 34567890
        self.direction = 1
        self.vitesse_y = 0
        self.vitesse_x = 0


    def affichage(self, surface):
        pygame.draw.rect(surface, (0, 200, 200), self.rect)


class Projectyles(pygame.sprite.Sprite):
    def __init__(self,x,y,taille,direction,image):
        super().__init__()
        self.x = x
        self.y = y
        self.taille = taille
        self.direction = direction
        self.image = image
        self.image = pygame.transform.scale(image, (self.taille[0], self.taille[1]))  # Redimensionner l'image
        self.rect = pygame.Rect(self.x, self.y, self.taille[0], self.taille[1])

    def afficher(self, surface):
        surface.blit(self.image, self.rect)

    def mouvement(self,vitesse):
        self.rect.x += vitesse * self.direction

class Jeu:
    def __init__(self):
        self.ecran = pygame.display.set_mode((1920, 1024), pygame.RESIZABLE)
        self.image = pygame.image.load("logo.png").convert()
        pygame.display.set_icon(self.image)
        self.background = pygame.image.load("background3.png").convert()
        self.sol = Sol()
        self.joueur_x , self.joueur_y = 200, 400
        self.taille = [64,128]
        self.joueur = Joueur(self.joueur_x,self.joueur_y,self.taille)
        self.projectiles_groupe = Group()
        self.image_joueur = pygame.image.load("arme_os.png")
        self.image_joueur_rect = pygame.Rect(124, 453 , 8, 8)
        self.image_tir = self.image_joueur.subsurface(self.image_joueur_rect)
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
            self.ecran.blit(self.background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    continuer = False
                elif event.type == pygame.VIDEORESIZE:
                    self.ecran = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:  # 1 = Bouton gauche de la souris
                        self.joueur.a_tirer = True


            # Tirer un projectile
            if self.joueur.a_tirer:
                if len(self.projectiles_groupe) < self.joueur.tir_auto:
                    projectile = Projectyles(self.joueur.rect.x + 20 , self.joueur.rect.y - 5, [20 ,20], self.joueur.direction, self.image_tir)
                    self.projectiles_groupe.add(projectile)  # Ajout au groupe
                self.joueur.a_tirer = False  # Empêcher le tir continu

            # Mise à jour des projectiles
            for projectile in self.projectiles_groupe:
                projectile.mouvement(2)  # Ajustement de la vitesse
                if projectile.rect.right >= self.ecran.get_width():
                    self.projectiles_groupe.remove(projectile)

            self.sol.affichage(self.ecran)
            self.gravite_jeu()
            self.joueur.affichage(self.ecran)
            for projectile in self.projectiles_groupe:
                projectile.afficher(self.ecran)  # Correction de l'appel

            pygame.display.update()

        pygame.quit()



if __name__ == '__main__':
    Jeu().boucle_principale()
