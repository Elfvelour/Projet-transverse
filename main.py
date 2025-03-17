#####################################################
# Fichier de lancement du jeu                       #
# Auteurs: Flavie BREMAND et Thomas AUBERT          #
#####################################################
from trajectoires import *
from monnaie import *
from bot import *
import json

class Sol(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0, 800, 1920, 300)

    def affichage(self, surface):
        pygame.draw.rect(surface, (0, 200, 100), self.rect)


class Jeu:
    def __init__(self):
        self.ecran = pygame.display.set_mode((1920, 1024), pygame.RESIZABLE)
        self.donnees_json = self.charger_donnees_json("gestion_stats.json")
        self.personnage_actuel = "Einstein"
        self.image_projectile = self.obtenir_image_projectile(self.personnage_actuel)
        self.background = pygame.image.load("assests/background3.png").convert()
        self.background = pygame.transform.scale(self.background, (1920, 1024))
        self.sol = Sol()
        self.joueur = Joueur(200, 672, [64, 128])
        self.projectiles_groupe = Group()
        self.piece = Pieces((50, 50))
        self.bot = Bot(1920 - 100, 672, [64, 128])

        self.tour_joueur = True  # Le joueur commence
        self.en_attente = False  # Attente entre les tours
        self.temps_attente = 0  # Temps de début d'attente
        self.explosion_active = False  # True si une explosion est affichée

    def charger_donnees_json(self, fichier):
        with open(fichier, "r", encoding="utf-8") as f:
            return json.load(f)

    def obtenir_image_projectile(self, personnage):
        for item in self.donnees_json:
            if item["personnage"] == personnage:
                return pygame.image.load(item["image"]).convert_alpha()
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
                                            puissance)
                    self.projectiles_groupe.add(projectile)
                    self.piece.monnaie_joueur += 1

                    # Début de l'attente avant le tour du bot
                    self.temps_attente = pygame.time.get_ticks()
                    self.en_attente = True
                    self.tour_joueur = False

            if pygame.mouse.get_pressed()[0] and self.tour_joueur:
                self.joueur.charger_tir()

            # Gestion de l'attente entre les tours
            if self.en_attente:
                if pygame.time.get_ticks() - self.temps_attente >= 1000 and not self.explosion_active:
                    self.en_attente = False

                    if not self.tour_joueur:  # C'est au bot de jouer
                        angle, puissance = self.bot.tir(self.joueur.rect.centerx, self.joueur.rect.centery)
                        projectile = Projectile(self.bot.rect.centerx, self.bot.rect.centery, [60, 60],
                                                self.image_projectile, angle, puissance)
                        self.projectiles_groupe.add(projectile)

                        # Début de l'attente avant de redonner le tour au joueur
                        self.temps_attente = pygame.time.get_ticks()
                        self.en_attente = True
                        self.tour_joueur = True

            for projectile in self.projectiles_groupe:
                projectile.mouvement(self.bot, self.piece, self)

            # Vérifier si une explosion est en cours
            if not self.projectiles_groupe and not self.explosion_active:
                self.en_attente = False  # Plus d’attente
                self.tour_joueur = True  # Le joueur peut rejouer

            self.sol.affichage(self.ecran)
            self.joueur.affichage(self.ecran, pos_souris)
            self.bot.affichage(self.ecran)
            for projectile in self.projectiles_groupe:
                projectile.afficher(self.ecran)

            self.piece.afficher_monnaie(self.ecran)
            self.piece.afficher_nombre_pieces(self.ecran)
            self.piece.afficher_bouton(self.ecran)

            pygame.display.update()
            clock.tick(110)

        pygame.quit()

if __name__ == '__main__':
    Jeu().boucle_principale()
