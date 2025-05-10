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

clock = pygame.time.Clock() # Horloge pour contrôler le nombre d’images par seconde
continuer = True

class Jeu:
    def __init__(self, screen, perso, arme, sons):
        # Initialisation des données depuis le fichier JSON
        self.donnees_json = self.charger_donnees_json("gestion_stats.json")

        # Références aux éléments principaux
        self.ecran = screen
        self.perso = perso
        self.arme = arme
        self.sons = sons

        # Chargement des images de projectiles selon le personnage et l'arme choisis
        self.image_projectile_joueur = self.obtenir_image_arme(self.perso, self.arme)
        self.image_projectile_bot = self.obtenir_image_arme("PB", "A0")

        # Chargement de l’arrière-plan
        self.background = pygame.image.load("assets/images/menup/logoiajeu.jpeg")

        # Création des objets de jeu
        self.sol = Sol()
        self.joueur = Joueur(100, 670, [32, 64], perso, arme)
        self.bot = Bot((1920 - 200), 620, [32, 128])
        self.projectiles_joueur = pygame.sprite.Group()
        self.projectiles_bot = pygame.sprite.Group()
        self.piece = Pieces((50, 50))

        # État du jeu
        self.tour_joueur = True
        self.en_attente = False
        self.temps_attente = 0
        self.explosion_active = False

        # Système de trajectoires
        self.trajectoire = Trajectoire()
        self.masse_projectile = self.get_masse_projectile()

        self.debut_partie = pygame.time.get_ticks() # Heure du début de partie

        # Compteurs pour l'historique
        self.lancements_joueur = 0  # Compteur pour les lancements du joueur
        self.lancements_bot = 0  # Compteur pour les lancements du bot

    def charger_donnees_json(self, fichier):
        # Charge les données JSON des personnages et armes
        with open(fichier, "r", encoding="utf-8") as f:
            return json.load(f)

    def enregistrer_historique(self, perso, arme): # Sauvegarde les infos de la partie dans un fichier texte
        # Recherche des infos du personnage et de l’arme
        details_perso = None
        details_arme = None

        for item in self.donnees_json:
            if item["code P"] == perso:
                details_perso = item
                if item["code A"] == arme:
                    details_arme = item

        # Si les infos sont trouvées, on les enregistre dans le fichier
        if details_perso and details_arme:
            # Construction de l'historique
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

            # Écriture dans le fichier
            with open("historique.txt", "a", encoding="utf-8") as fichier:
                fichier.write(date_h)
                fichier.write(choix_perso_h)
                fichier.write(choix_arme_h)
                fichier.write(pieces_h)
                fichier.write(joueur_h)
                fichier.write(bot_h)
                fichier.write(resultat_h)

    def affichage_score(self):
        # Affiche un résumé du score du joueur en bas de l’écran
        police = pygame.font.Font("assets/images/affichage/04B_30__.TTF", 40)
        texte=police.render(f"Coup(s): {self.bot.collisions_bot}, ratio: {self.bot.collisions_bot}/{self.lancements_joueur}, Monnaie restantes: {self.piece.monnaie_joueur}", True, "white")
        ecran.blit(texte, (250, 650))

    def get_masse_projectile(self):
        # Récupère la masse du projectile à partir des données du joueur et de l’arme
        for item in self.donnees_json:
            if item["code P"] == self.perso and item["code A"] == self.arme:
                return item.get("masse", 1)
        return 1 # Valeur par défaut

    def obtenir_image_arme(self, personnage, arme):
        # Charge l’image du projectile associé au personnage et à l’arme
        for item in self.donnees_json:
            if item["code P"] == personnage and item["code A"] == arme:
                return pygame.image.load(item["image_arme"]).convert_alpha()
        return pygame.image.load("assets/images/armes/default_projectile.png").convert_alpha()

    def gerer_evenements_jeu(self, event): # Gestion des événements de la souris (tir du joueur)
        # Calcul du temps écoulé depuis le début de la partie
        temps_ecoule_depuis_debut = pygame.time.get_ticks() - self.debut_partie

        # Empêche toute interaction dans les 500 premières millisecondes du jeu (empêche le tir immédiat au lancement du jeu)
        if temps_ecoule_depuis_debut < 500:
            return

        # Détection d'un clic gauche de souris (bouton 1) pendant le tour du joueur
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.tour_joueur:
            # Le joueur commence à charger son tir (le clic est maintenu)
            self.trajectoire.start_charging()

        # Détection du relâchement du clic gauche de la souris pour déclencher le tir
        if (
                event.type == pygame.MOUSEBUTTONUP and
                event.button == 1 and
                self.tour_joueur and
                mon_bouton_parametre.action and  # Le bouton paramètre est actif (conditions de tir respectées)
                self.joueur.angle <= 95 and      # L'angle du tir est autorisé
                self.bot.pv > 0 and              # Le bot est encore en vie
                self.joueur.pv > 0               # Le joueur est encore en vie
        ):
            # Calcul de la vitesse initiale du projectile en fonction de la durée de chargement
            vitesse_initiale = self.trajectoire.stop_charging_and_compute_speed(self.masse_projectile)

            # Conversion de la vitesse en puissance (échelle divisée par 10)
            puissance = vitesse_initiale / 10

            # Coordonnées de départ du projectile (en fonction de l'angle et de la position du joueur)
            x_proj, y_proj = self.joueur.position_depart_projectile()

            # Création d’un nouveau projectile
            projectile = Projectile(x_proj, y_proj, [60, 60], self.image_projectile_joueur, self.joueur.angle,
                                    puissance, vitesse_initiale, "joueur")

            self.projectiles_joueur.add(projectile) # Ajout du projectile dans le groupe des projectiles du joueur

            # Récompense et historique
            self.piece.monnaie_joueur += 1
            self.lancements_joueur += 1  # Incrémenter le compteur de lancements du joueur (historique)
            print(f"Le projectile a été tiré : puissance={puissance:.2f}, vitesse_initiale={vitesse_initiale:.2f}")

            # Démarre le temps d’attente avant que le bot puisse tirer
            self.temps_attente = pygame.time.get_ticks()
            self.en_attente = True

            self.tour_joueur = False # Le joueur a terminé son tour

        # Gestion des clics sur les pièces (interaction avec le système de monnaie)
        self.piece.verifier_clic(event, self)

    def mettre_a_jour_jeu(self): # Gère la logique de passage de tour et mouvements des projectiles
        # Si le jeu est en attente (après un tir), on vérifie si le délai d'attente est écoulé
        if self.en_attente:
            # Si 3 secondes se sont écoulées depuis le dernier tir et qu'aucune explosion n'est en cours
            if pygame.time.get_ticks() - self.temps_attente >= 3000 and not self.explosion_active:
                # Si aucun projectile n'est actif sur l'écran
                if not self.projectiles_joueur and not self.projectiles_bot:
                    self.en_attente = False # Le jeu peut continuer


                    # Si c'est au tour du bot de jouer, et que les deux personnages sont encore en vie
                    if not self.tour_joueur and self.bot.pv > 0 and self.joueur.pv > 0:
                        # Le bot calcule l'angle et la puissance de son tir en fonction de la position du joueur
                        angle, puissance = self.bot.tir(self.joueur.rect.centerx, self.joueur.rect.centery)
                        # La vitesse initiale du tir dépend de la puissance, avec un minimum de 110
                        vitesse_initiale = 110 + (7 * puissance)

                        # Création du projectile tiré par le bot
                        projectile = Projectile(self.bot.rect.centerx, self.bot.rect.centery, [60, 60],
                                                self.image_projectile_bot, angle, puissance, vitesse_initiale, "bot")

                        self.projectiles_bot.add(projectile) # Ajout du projectile à la liste des projectiles du bot

                        self.lancements_bot += 1  # Incrémenter le compteur de lancements du bot (historique)

                        # Mise à jour de l'heure du dernier tir
                        self.temps_attente = pygame.time.get_ticks()
                        self.en_attente = True # On entre à nouveau en attente (temps de réaction du joueur)
                        self.tour_joueur = True # C'est maintenant au tour du joueur de jouer
                        print(f"Le bot a tiré.")

        # Mise à jour de la position et des collisions des projectiles du joueur
        for projectile in self.projectiles_joueur:
            projectile.mouvement(self.bot, self.piece, self, self.sons)

        # Mise à jour de la position et des collisions des projectiles du bot
        for projectile in self.projectiles_bot:
            projectile.mouvement(self.bot, self.piece, self, self.sons)

    def afficher_jeu(self, pos_souris): # Affiche tous les éléments à l’écran
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

        # Affichage du message de victoire
        if self.bot.pv <= 0:
            self.bot.afficher_gg(self.ecran)
            Jeu.affichage_score(self)
            if self.bot.afficher_gg(self.ecran):
                continuer = False

        affichage_parametre() # Affiche les paramètres (volume, etc.)

    def boucle_principale(self): # Boucle principale du jeu
        global continuer
        while continuer:
            pos_souris = pygame.mouse.get_pos() # Récupère la position actuelle de la souris

            # Parcours de tous les événements Pygame (clics, touches, fermeture, etc.)
            for event in pygame.event.get():
                # Si l'utilisateur clique sur la croix de la fenêtre, on quitte le jeu
                if event.type == pygame.QUIT:
                    continuer = False
                # Gestion des autres événements du jeu (clics de tir, interactions avec les pièces...)
                self.gerer_evenements_jeu(event)

            # Met à jour les états du jeu : projectiles, tirs du bot, collisions, attente, etc.
            self.mettre_a_jour_jeu()

            # Rafraîchit l’affichage du jeu (dessine le fond, les personnages, les projectiles, la monnaie, etc.)
            self.afficher_jeu(pos_souris)

            # Met à jour l’écran avec tout ce qui a été dessiné
            pygame.display.update()

            # Limite la vitesse de la boucle à 40 images par seconde (FPS)
            clock.tick(40)

        # Une fois la boucle terminée (victoire, défaite ou fermeture), on enregistre les données de fin de partie dans l'historique
        self.enregistrer_historique(self.perso, self.arme)

        pygame.quit()
