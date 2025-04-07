# Projet-transverse
création du jeu bowmaster

-03/02/2024, Noémie : Organisation des fichiers du jeu 

-04/02/2025, Noémie : Création des statistiques des armes 

-09/02/2025, Noémie : Initialisation de la fonction run_game dans le fichier main + invention des descriptions

-10/02/2025, Noémie : Initialisation de la fonction monnaie.py

-10/02/2025, Tim: Initialistaion de la fonction main_menu.py

-23/02/2025, Flavie : Mise en place du lancement du projectile par clic gauche

-24/02/2025, Noémie : Le joueur gagne une pièce à chaque fois qu'il tire

-24/02/2025, Tim: création de la page et des bouton

-28/02/2025, Flavie : Mise en place de la trajectoire parabole (vitesse en fonction du temps du clic gauche)

-28/02/2025, Tim: bouton quitter fonctionelle + musique

-03/03/2025, Flavie : Ajustements dans la trajectoire (notamment sur la vitesse et l'angle)
                      Création du fichier bot et début de son code

-03/03/2025, Noémie : Recherche des assets pour les armes du jeu
                      Modification du .json pour correspondre au choix du joueur

-14/03/2025 Noémie : Ajout du bouton pour utiliser l'ultime coup du personnage 

-15/03/2025 Tim: revue en profondeur des assets pour le menu principal (nouvelles images et redimensions)+animation bouton et sons

-24/03/2025 Flavie: Améliorations des trajectoires et du bot (gravité et projectiles)
                    Ajustement du positionnement des images d'explosion (centrées par rapport au projectile)

-25/03/2025 Tim: mise au propre des assets et correction bug sons potion

-03/04/2025 Tim: mise au propre des commentaires ainsi que la création bu bouton "revenir en arrière".

-06/04/2025 Flavie: Refonte de la boucle principale
                    Positionnement correct des images d'explosion (SUR le sol)
                    [Améliorations des tirs du bot (corrections des plages de distance en fonction du joueur)]->pas réussi...T^T

-06/04/2025 Tim: 1ère fusion du main et main_menu réussi attente avec raphalél pour le faire avec le menu des joueurs puis début de la création du bouton paramètre pour changer et arrêter la musique à tout moment

     def gerer_evenements_jeu(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.tour_joueur:
            self.joueur.temps_debut = pygame.time.get_ticks()

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.tour_joueur:
            puissance = self.joueur.relacher_tir()
            x_proj, y_proj = self.joueur.position_depart_projectile()
            projectile = Projectile(x_proj, y_proj, [60, 60], self.image_projectile, self.joueur.angle,
                                    puissance, "joueur")
            self.projectiles_joueur.add(projectile)
            self.piece.monnaie_joueur += 1
            self.temps_attente = pygame.time.get_ticks()
            self.en_attente = True
            self.tour_joueur = False

    def mettre_a_jour_jeu(self, event):
        if self.en_attente:
            if pygame.time.get_ticks() - self.temps_attente >= 5000 and not self.explosion_active:
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

        for projectile in self.projectiles_joueur:
            projectile.mouvement(self.bot, self.piece, self)

        for projectile in self.projectiles_bot:
            projectile.mouvement(self.bot, self.piece, self)

    def afficher_jeu(self,pos_souris):
        self.ecran.blit(self.background,(0,0))
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

        if self.piece.monnaie_joueur >= 250:
            self.piece.afficher_gg(self.ecran)

    def boucle_principale(self=None):
        continuer = True
        etat_jeu = "menu"  # ou "jeu"
        while continuer:
            pos_souris = pygame.mouse.get_pos()

            # ----- 1. GESTION DES ÉVÉNEMENTS -----
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    continuer = False

                if etat_jeu == "jeu":
                    # 🎯 Appelle ta fonction pour gérer les clics du joueur
                    Jeu.gerer_evenements_jeu(self,event)

                elif etat_jeu == "menu":
                    pass  # Les événements menu sont dans affichage_menu()

            # ----- 2. MISE À JOUR LOGIQUE -----
            if etat_jeu == "jeu":
                Jeu.mettre_a_jour_jeu(self,event)

            # ----- 3. AFFICHAGE -----
            if etat_jeu == "menu":
                action = affichage_menu()
                if action == True:
                    etat_jeu = "jeu"
                elif action == False:
                    continuer = False

            elif etat_jeu == "jeu":
                Jeu.afficher_jeu(self,pos_souris)

            pygame.display.update()
            clock.tick(60)

        pygame.quit()

