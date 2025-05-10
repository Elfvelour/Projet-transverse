#####################################################
# Fichier de gestion du jeu                         #
# Auteurs : tous                                    #
#####################################################

from joueur import *
from trajectoires import Projectile, Sol, Trajectoire
from monnaie import Pieces
from bot import Bot
import json
import pygame
from datetime import datetime

# Ouvrir le fichier historique.txt en mode ajout
with open("historique.txt", "a", encoding="utf-8") as fichier_historique:
    pass  # Juste pour s'assurer que le fichier est ouvert

clock = pygame.time.Clock()
continuer = True

class Jeu:
    def __init__(self, screen, perso, arme, sons):
        self.donnees_json = self.charger_donnees_json("gestion_stats.json")  # chargement des données
        self.ecran = screen
        self.perso = perso
        self.arme = arme
        self.image_projectile_joueur = self.obtenir_image_arme(self.perso, self.arme)
        self.image_projectile_bot = self.obtenir_image_arme("PB", "A0")  # arme par défaut du bot
        self.background = pygame.image.load("assets/images/menup/logoiajeu.jpeg")
        self.sol = Sol()
        self.joueur = Joueur(100, 670, [32, 64], perso, arme)
        self.donnees_json = self.charger_donnees_json("gestion_stats.json")
        self.sons = sons
        self.projectiles_joueur = pygame.sprite.Group()
        self.projectiles_bot = pygame.sprite.Group()

        self.piece = Pieces((50, 50))
        self.bot = Bot((1920 - 200), 620, [32, 128])

        self.tour_joueur = True
        self.en_attente = False
        self.temps_attente = 0
        self.explosion_active = False

        self.trajectoire = Trajectoire()
        self.masse_projectile = self.get_masse_projectile()

        self.debut_partie = pygame.time.get_ticks()

        # Historique
        self.lancements_joueur = 0  # Compteur pour les lancements du joueur
        #self.collisions_joueur = 0  # Compteur pour les collisions du joueur
        self.lancements_bot = 0  # Compteur pour les lancements du bot
        #self.collisions_bot = 0  # Compteur pour les collisions du bot

    def charger_donnees_json(self, fichier):
        with open(fichier, "r", encoding="utf-8") as f:
            return json.load(f)

    def enregistrer_historique(self, perso, arme):
        # Trouver les détails du personnage et de l'arme
        details_perso = None
        details_arme = None

        for item in self.donnees_json:
            if item["code P"] == perso:
                details_perso = item
                if item["code A"] == arme:
                    details_arme = item

        if details_perso and details_arme:
            # Créer des entrées pour l'historique
            date_heure = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            date_h = f"{date_heure}\n"
            choix_perso_h = f"- Personnage choisi : {details_perso['personnage']}\n"
            choix_arme_h = f"- Arme choisie : {details_arme['nom']}\n"
            pieces_h = f"- Monnaie : {self.piece.monnaie_joueur} pièces à la fin de la partie\n"
            joueur_h = f"- Le bot a touché le joueur {self.joueur.collisions_joueur} fois sur {self.lancements_bot} coup(s)\n"
            bot_h = f"- Le joueur a touché le bot {self.bot.collisions_bot} fois sur {self.lancements_joueur} coup(s)\n"
            if self.bot.victoire_joueur :
                resultat_h = f"-> Victoire du joueur ! Félicitations !\n\n"
            else :
                resultat_h = f"-> Partie non finie ou perdue...\n\n"

            # Écrire dans le fichier historique.txt
            with open("historique.txt", "a", encoding="utf-8") as fichier:
                fichier.write(date_h)
                fichier.write(choix_perso_h)
                fichier.write(choix_arme_h)
                fichier.write(pieces_h)
                fichier.write(joueur_h)
                fichier.write(bot_h)
                fichier.write(resultat_h)

    def get_masse_projectile(self):
        for item in self.donnees_json:
            if item["code P"] == self.perso and item["code A"] == self.arme:
                return item.get("masse", 1)
        return 1

    def obtenir_image_arme(self, personnage, arme):
        for item in self.donnees_json:
            if item["code P"] == personnage and item["code A"] == arme:
                return pygame.image.load(item["image_arme"]).convert_alpha()
        return pygame.image.load("assets/images/armes/default_projectile.png").convert_alpha()

    def gerer_evenements_jeu(self, event):
        temps_ecoule_depuis_debut = pygame.time.get_ticks() - self.debut_partie
        if temps_ecoule_depuis_debut < 500:
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.tour_joueur:
            self.trajectoire.start_charging()

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.tour_joueur and mon_bouton_parametre.action and self.joueur.angle <= 95 and self.bot.pv > 0 and self.joueur.pv > 0:
            vitesse_initiale = self.trajectoire.stop_charging_and_compute_speed(self.masse_projectile)
            puissance = vitesse_initiale / 10
            x_proj, y_proj = self.joueur.position_depart_projectile()
            projectile = Projectile(x_proj, y_proj, [60, 60], self.image_projectile_joueur, self.joueur.angle,
                                    puissance, vitesse_initiale, "joueur")
            self.projectiles_joueur.add(projectile)
            self.piece.monnaie_joueur += 1
            self.lancements_joueur += 1  # Incrémenter le compteur de lancements du joueur (historique)
            print(f"Le projectile a été tiré : puissance={puissance:.2f}, vitesse_initiale={vitesse_initiale:.2f}")
            self.temps_attente = pygame.time.get_ticks()
            self.en_attente = True
            self.tour_joueur = False

        self.piece.verifier_clic(event, self)

    def mettre_a_jour_jeu(self):
        if self.en_attente:
            if pygame.time.get_ticks() - self.temps_attente >= 3000 and not self.explosion_active:
                if not self.projectiles_joueur and not self.projectiles_bot:
                    self.en_attente = False
                    if not self.tour_joueur and self.bot.pv > 0 and self.joueur.pv > 0:
                        angle, puissance = self.bot.tir(self.joueur.rect.centerx, self.joueur.rect.centery)
                        vitesse_initiale = 110 + (7 * puissance)
                        projectile = Projectile(self.bot.rect.centerx, self.bot.rect.centery, [60, 60],
                                                self.image_projectile_bot, angle, puissance, vitesse_initiale, "bot")
                        self.projectiles_bot.add(projectile)
                        self.lancements_bot += 1  # Incrémenter le compteur de lancements du bot (historique)
                        self.temps_attente = pygame.time.get_ticks()
                        self.en_attente = True
                        self.tour_joueur = True
                        print(f"Le bot a tiré.")

        for projectile in self.projectiles_joueur:
            projectile.mouvement(self.bot, self.piece, self, self.sons)

        for projectile in self.projectiles_bot:
            projectile.mouvement(self.bot, self.piece, self, self.sons)

    def afficher_jeu(self, pos_souris):
        global continuer
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

        if self.bot.pv <= 0:
            self.bot.afficher_gg(self.ecran)
            if self.bot.afficher_gg(self.ecran):
                continuer = False
        affichage_parametre()

    def boucle_principale(self):
        global continuer
        while continuer:
            pos_souris = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    continuer = False
                self.gerer_evenements_jeu(event)

            self.mettre_a_jour_jeu()
            self.afficher_jeu(pos_souris)
            pygame.display.update()
            clock.tick(40)

        self.enregistrer_historique(self.perso, self.arme)

        pygame.quit()
