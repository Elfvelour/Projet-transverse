#####################################################
# Fichier de gestion du jeu                         #
# Auteurs : tous                                    #
#####################################################

import pygame
import json
from joueur import *
from trajectoires import Projectile
from trajectoires import Sol
from monnaie import Pieces
from bot import Bot
from main_menu import Musique, mon_bouton_ar
clock = pygame.time.Clock()


class Jeu:
    def __init__(self, screen, perso, arme):
        self.donnees_json = self.charger_donnees_json("gestion_stats.json")  # chargement des données
        self.ecran = screen
        self.perso = perso
        self.arme = arme
        self.image_projectile = self.obtenir_image_arme(self.perso, self.arme)
        self.background = pygame.image.load("assets/images/menup/logoiajeu.jpeg")
        self.sol = Sol()
        self.joueur = Joueur(100, 672, [32, 64], perso, arme)
        self.donnees_json = self.charger_donnees_json("gestion_stats.json")  # chargement des données

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

    def obtenir_image_arme(self, personnage, arme):
        for item in self.donnees_json:
            if item["code P"] == personnage and item["code A"] == arme:
                return pygame.image.load(item["image_arme"]).convert_alpha()
        return pygame.image.load("assets/images/armes/default_projectile.png").convert_alpha()

    def gerer_evenements_jeu(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.tour_joueur:
            self.joueur.temps_debut = pygame.time.get_ticks()
        # tant qu'on appuis pas sur les paramètres et que l'angle est de moins de 95 °
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.tour_joueur and mon_bouton_parametre.action and self.joueur.angle<=95:
            puissance = self.joueur.relacher_tir()
            x_proj, y_proj = self.joueur.position_depart_projectile()
            projectile = Projectile(x_proj, y_proj, [60, 60], self.image_projectile, self.joueur.angle,
                                    puissance, "joueur")
            self.projectiles_joueur.add(projectile)
            self.piece.monnaie_joueur += 1
            print(f"Le projectile a été tiré : puissance={puissance:.2f}")  # Debug
            self.temps_attente = pygame.time.get_ticks()
            self.en_attente = True
            self.tour_joueur = False

        self.piece.verifier_clic(event, self)

    def mettre_a_jour_jeu(self):
        if self.en_attente:
            if pygame.time.get_ticks() - self.temps_attente >= 3000 and not self.explosion_active:
                if not self.projectiles_joueur and not self.projectiles_bot:
                    self.en_attente = False
                    if not self.tour_joueur:
                        angle, puissance = self.bot.tir(self.joueur.rect.centerx, self.joueur.rect.centery)
                        projectile = Projectile(self.bot.rect.centerx, self.bot.rect.centery, [60, 60],
                                                self.image_projectile, angle, puissance, "bot")
                        self.projectiles_bot.add(projectile)
                        self.temps_attente = pygame.time.get_ticks()
                        self.en_attente = True
                        self.tour_joueur = True
                        print(f"Le bot a tiré.")  # Debug

        for projectile in self.projectiles_joueur:
            projectile.mouvement(self.bot, self.piece, self)

        for projectile in self.projectiles_bot:
            projectile.mouvement(self.bot, self.piece, self)

    def afficher_jeu(self, pos_souris):
        self.ecran.blit(self.background, (0, 0))
        self.sol.affichage(self.ecran)

        self.joueur.affichage(self.ecran, pos_souris)
        self.bot.affichage(self.ecran)

        self.joueur.afficher_barre_vie(self.ecran)
        self.bot.afficher_barre_vie(self.ecran)

        for projectile in self.projectiles_joueur:
            projectile.afficher(self.ecran)

        for projectile in self.projectiles_bot:
            projectile.afficher(self.ecran)

        self.piece.afficher_monnaie(self.ecran)
        self.piece.afficher_nombre_pieces(self.ecran)
        self.piece.afficher_bouton(self.ecran)

        if self.piece.monnaie_joueur >= 250:
            self.piece.afficher_gg(self.ecran)
        affichage_parametre()

    def boucle_principale(self):
        continuer = True
        while continuer:
            pos_souris = pygame.mouse.get_pos()

            # ----- 1. GESTION DES ÉVÉNEMENTS -----
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    continuer = False
                self.gerer_evenements_jeu(event)
            # ----- 2. MISE À JOUR LOGIQUE (appelée à chaque frame) -----
            self.mettre_a_jour_jeu()
            # ----- 3. AFFICHAGE -----
            self.afficher_jeu(pos_souris)

            pygame.display.update()
            clock.tick(60)

        pygame.quit()
