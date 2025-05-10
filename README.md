# Projet-transverse Bow Master [](https://github.com/Elfvelour/Projet-transverse/blob/main/assets/images/menup/logo.png)

## Sujet
 Développement d'un jeu sur python à l'aide de la bibliothèque python

## Caractéristiques
- Jeu de tir en 2D
- 1 Vs 1 contre un bot 
- De multiples personnages et armes
- Un menu interactif de musique

### Caractéristiques techniques :

- 8 fichiers _.py_, 1 fichier _.json_, 2 fichiers _.txt_, 35 fichiers _.png_, 10 fichiers _.mp3_, 1 fichier _.wav_
- Le fichier json stocke toutes les caractéristiques liées au personnages et armes disponibles.
Il est chargé dans les fichiers **jeu.py** et **joueur.py** et gère donne les chemins d'accès de l'imagedu personnage
et de l'arme choisi, ainsi que celles du BOT. 

thomas pk enlever le plein écran
flavie comment déterminer les trajectoires
- utilisation de langage orienté objet avec l'utilisation des classes.

#### Bibliothèques python utilisées :

pygame, math, random, json, os, ctypes, time

## Contributeurs :

- Girault Timothée : [timothee.girault@efrei.net](mailto:timothee.girault@efrei.net)
- Aubert Thomas : [thomas.aubert@efrei.net](mailto:thomas.aubert@efrei.net)
- Brémand Flavie : [flavie.bremand@efrei.net](mailto:flavie.bremand@efrei.net)
- Marques Noémie : [noemie.marques@efrei.net](mailto:noemie.marques@efrei.net)
- De Jesus Coelho Rafaël : [rafael.de-jesus-coelho@efrei.net](mailto:rafael.de-jesus-coelho@efrei.net)

#### - Timothée Girault :

[![main_menu.py](https://img.shields.io/badge/main_menu-blue)](main_menu.py) : création du menu principal du jeu ainsi que les paramètres pour changer de musique et l'allumer ou l'éteindre

[![main.py](https://img.shields.io/badge/main-red)](main.py) : résolution des bugs

#### - Flavie Brémand :

[![jeu.py](https://img.shields.io/badge/jeu-green)](jeu.py) : gestion de l'alternance entre le joueur et le bot, affichage de l'explosion, boucle principale et gestion de l'historique

[![trajectoires.py](https://img.shields.io/badge/trajectoire.py-green)](trajectoires.py) : calcul de la trajectoire du tir du joueur et de la puissance du tir en fonction du clic gauche, gestion des images d'explosion

[![bot.py](https://img.shields.io/badge/jeu-green)](bot.py) : bases du bot (sa position et début des fonctions pour son lancer)

[![main.py](https://img.shields.io/badge/main-red)](main.py) : création de l'ancienne version

#### - Noémie Marques :

[![monnaie.py](https://img.shields.io/badge/monnaie-purple)](monnaie.py) : gestion du système de monnaie du jeu, octroyant au joueur une amélioration de ses dégâts (cela comprend l'affichage et la gestion du nombre de pièces et l'affichage et la gestion du bouton du coffre)  

[![main.py](https://img.shields.io/badge/main-red)](main.py) : création de la liaison entre les fonctions du menu_joueur.py et l'affichage du bon personnage 

#### - Thomas Aubert :

[![trajectoires.py](https://img.shields.io/badge/trajectoire.py-green)](trajectoires.py) : Création et amélioration de la trajectoire. Ajout de physique et d'un système de masse pour les projectiles. 

[![bot.py](https://img.shields.io/badge/bot-green)](bot.py) : Faire tirer le bot. Ajout d'un système de vie, dégâts, barre de vie. 

[![bot.py](https://img.shields.io/badge/joueur.py-green)](joueur.py) : Base du personnage joueur. Ajout du système de vie, dégâts et barre de vie.

[![bot.py](https://img.shields.io/badge/gestion_stats-blue)](gestion_stats.json) : Création des statistiques de vie, dégâts et masse pour les personnages


#### - Rafaël De Jesus Coelho :

[![menu_joueur.py](https://img.shields.io/badge/menu_joueur-blue)](menu_joueur.py) : permet de sélectionner le personnage et son arme avec ntégration des différents personnages et armes disponibles à partir du fichier gestion_stats.json.


Commun : ***assets***


## Carnet de bord :

### Février 2025 :

#### 03/02/2025 :

- **Noémie** : Organisation des fichiers du jeu sur le fichier **contenu.txt**

#### 04/02/2025 :

- **Noémie** : Création des statistiques des armes sur le fichier **gestion_stats.json**

#### 09/02/2025 :

- **Noémie** : Initialisation de la fonction run_game dans le fichier **main.py** + invention des descriptions

#### 10/02/2025 :

- **Noémie** : Initialisation de la fonction **monnaie.py**


- **Timothée** : Initialisation du fichier **main_menu.py** et suppression de l'ancien fichier menu.py pour repartir d'une base saine 
après de nombreux tests sur ce dernier


- **Thomas** : Début du fichier **trajectoires.py** avec quelques images pour commencer. J'ai commencé la classe Sol.

#### 23/02/2025 :

- **Flavie** : Mise en place du lancement du projectile par clic gauche et de la ligne blanche qui montre le début de la trajectoire

#### 24/02/2025 :

- **Noémie** : Continuation du fichier **monnaie.py**. Un compteur de pièce est affiché et le joueur gagne une pièce à chaque fois qu'il tire


- **Timothée** : Création de la fenêtre du jeu de taille 1920 par 1024 ainsi que des boutons "jouer" et "quitter" dans le fichier **main_menu.py**. 
Je teste les différentes couleurs comme le rouge, rouge bordeaux ou le noir pour les boutons ou le fond

#### 28/02/2025 :

- **Flavie** : Mise en place de la puissance de la trajectoire parabole (vitesse en fonction du temps du clic gauche)


- **Timothée** : J'ai créé une fonction pour détecter le clic de la souris sur une surface rectangulaire tel qu'on appuie sur le bouton quitter cela fait fermer la fenêtre. 
Puis j'ai initialisé la musique avec une boucle infinie avec la bibliothèque pygame dans le fichier **main_menu.py**.

### Mars 2025 :

#### 03/03/2025 :

- **Flavie** : Ajustements dans la trajectoire (notamment sur la vitesse et l'angle)
  Création du fichier bot et début de son code
  Séparation des fichiers **main.py** et **trajectoires.py** pour plus de clarté


- **Noémie** : Recherche des assets pour les armes du jeu
  Modification du .json pour correspondre au choix du joueur


- **Thomas** : Classe Sol finie. Possibilité de tirer donc amélioration de la trajectoire. J'ai aussi réussi à réaliser la collision avec le sol.

#### 14/03/2025 :

- **Noémie** : Ajout du bouton pour utiliser un boost. Les dégâts de l'arme choisi sont augmentés de 10 points. 

#### 15/03/2025 :

- **Timothée** : Création d'une fonction pour animer les boutons avec un changement de couleur au clic, par exemple en rouge et rouge bordeaux. Création 
d'une autre fonction pour changer de musique. Organisation des **assets** en deux types : images et sons, avec des sous-dossiers pour chaque fichier du jeu 
comme **menup** pour **main_menu.py**. Recherche et redimensionnement de nouvelles images pour le jeu avec GIMP.

#### 17/03/2025 :

- **Thomas** : J'ai réussi à faire jouer le bot et le joueur chacun leur tour et j'ai fait en sorte 
qu'une collision entre le joueur et le bot affiche une explosion à l'impact.

- **Rafael** : Création du fichier menu_joueur.py avec l’interface de base, intégration des personnages et armes depuis le JSON, et première version fonctionnelle des boutons de sélection.

#### 24/03/2025 :

- **Flavie** : Améliorations des trajectoires et du bot (gravité et projectiles)
  Ajustement du positionnement des images d'explosion (centrées par rapport au projectile)


- **Thomas** : Quelques petites modifications du bot et l'affichage de l'explosion fonctionne mieux. 
Quelques ajustements avec le code de Timothée pour que nos deux programmes fonctionnent ensemble.

- **Rafael** : Amélioration de l’affichage avec l’ajout des images des personnages et des descriptions dynamiques, ainsi qu’une fonction pour découper le texte selon la taille de l’écran. Dans l’après-midi et la soirée, finalisation du menu avec un affichage stylisé, un bouton de sélection d’arme et la gestion du retour à la sélection personnage/arme. Optimisation générale du code pour plus de clarté.

#### 25/03/2025 :

- **Timothée** : Après avoir mis au propre les **assets**, j'ai continué de faire le ménage en supprimant et remplaçant certaines par d'autres plus pertinentes et 
esthétiques. Lors de toutes les modifications d'images trouvées sur internet, j'ai utilisé GIMP qui fut d'une grande utilité pour moi. J'ai aussi corrigé le bug 
du son de la potion en s'activant une fois et non plus à chaque rafraîchissement de la fenêtre dans **trajectoires.py**.

### Avril 2025 :

#### 03/04/2025 :

- **Timothée** : J'ai commencé à commenter mon code pour que chaque personne du groupe puisse comprendre le mien et lors de problèmes sur le code, que 
j'arrive plus facilement à comprendre l'erreur. J'ai aussi créé le bouton "revenir en arrière" pour revenir en arrière lors du lancement du jeu prévu initialement. 
Il s'agit d'un bouton en deux parties la partie caché le bouton physique caché par le fond d'écran et la partie visible l'image du bouton.

#### 06/04/2025 :

- **Flavie** : Refonte de la boucle principale
  Positionnement correct des images d'explosion (SUR le sol)
  Essais d'instauration pour le bot de plages de valeurs où tirer


- **Timothée** : Après beaucoup d'efforts, j'ai réussi à relier chaque fichier pour que le jeu soit fonctionnel entre **main_menu.py** et **trajectoires.py** dans 
**main.py**. En attente de **menu_joueur.py** de Raphaël pour l'intégrer. Refonte complète de la musique avec une classe dédiée utilisant deux bibliothèques 
(son et musique). Refonte des fonctions pour la musique et création de deux fonctions pour changer et arrêter la musique. Création du bouton paramètre pour un menu 
translucide et changer de musique.

- **Rafael** : Finalisation de l’intégration quasi complète du menu_joueur dans le projet. Correction de quelques bugs liés à l’affichage et à la transition vers le jeu.

#### 07/04/2025 :

- **Flavie** : Améliorations dans **trajectoires.py** pour plus de clarté
  Séparation du fichier en plusieurs : **trajectoires.py** (sol et trajectoire du joueur), **joueur.py**, **bot.py**, **jeu.py**
  Rectifications qui en découlent dans le main

- **Noémie** : Modification du main pour que les valeurs renvoyées par le **menu_joueur.py** soit utilisées dans dans les fichiers **joueur.py** et **jeu.py** 

##### 10/04/2025 :

- **Timothée** : Refonte graphique du jeu en modifiant le fond d'écran avec openart.ai et redimensionnement des images avec GIMP. 
Changement des couleurs des boutons en jaune doré (`rgb(255, 215, 0)`) et jaune moutarde (`rgb(230, 170, 80)`). Création du menu paramètre translucide avec pygame. 
Simplification du code en regroupant les lignes de la boucle principale dans des fonctions.

#### 14/04/2025 :

- **Timothée** : Résolution des problèmes du *main* pour le rendre fonctionnel avec tous les fichiers du projet. Nettoyage des assets pour une charte graphique homogène.
Résolution du problème de rafraîchissement du menu des paramètres et mise en place d'un délai de 1s pour changer de musique avec le bouton "en avant".

#### 17/04/2025 :

- **Timothée** : Affichage de l'interface de la musique sur le menu des paramètres avec les boutons "jouer", "pause", "en avant" et "en arrière". 
Ajout des crédits dans **main_menu.py** avec la police souhaitée.

#### 19/04/2025 :

- **Timothée** : Résolution du problème d'affichage des boutons jouer et arrêter avec un booléen dans **main_menu.py**. Mise en place des fonctions pour arrêter et jouer de la musique. 
Ajout d'une condition pour rester sur le logo pause lors du changement de musique.

#### 20/04/2025 :

- **Timothée** : Intégration de la fonction *affichage_paramètre()* dans **jeu.py** et **menu_joueur.py** pour un menu des paramètres fonctionnel dans le jeu.

#### 22/04/2025 :

- **Timothée** : Résolution des problèmes de clic sur les personnages et de lancement du jeu avec le menu des paramètres ouvert. Ajout d'une condition de 
fermeture du menu dans **menu_joueur.py** et d'une limite d'angle de 95° dans **jeu.py** pour empêcher de tirer immédiatement après la sortie du menu.


#### 23/04/2025 :

- **Thomas** : Après une pause d'un mois sur le projet, j'ai (après beaucoup de galères) réussi à faire tirer le bot vers le joueur et fais en sorte 
que ce dernier puisse le toucher. J'ai également ajouté un système de PV et de dégâts au joueur et bot.

#### 25/04/2025 :

- **Timothée** : J'ai raccordé les différents bruitages aux personnages à l'aide de ma bibliothèque de bruitages dans **main_menu.py**. 
Maintenant quand un personnage lance son arme et touche le sol ou le bot, cela produit un son.

### Mai 2025 :

#### 02/05/2025 :

- **Timothée** : J'ai mis en place un bouton quitter à la fin du jeu lorsqu'on a éliminé le bot sur **bot.py**. Puis pour ne pas forcer le code, 
j'ai mis la variable "continuer" de la boucle principale dans **jeu.py** en globale pour quand on appuie sur le bouton, cela fait quitter proprement la fenêtre.

#### 03/05/2025 :

- **Timothée** : Création d'une condition en plus pour le joueur et le bot pour qu'on ne puisse plus tirer lorsque le bot ou le joueur a été battu.

#### 04/05/2025 :

- **Thomas** : J'ai ajouté la masse de chaque arme au fichier **gestion_stats.json** et la physique, mais il y a encore beaucoup de bugs.

#### 05/05/2025 :

- **Thomas** : Ajout d'un système de vitesse initiale ce qui a réglé tous mes problèmes de masses.

- **Noémie** : Modification graphique du sol sur lequel est le joueur

#### 08/05/2025 :

- **Thomas** : Finalisation du système de masse et corrections de tous les petits bugs qui ne gênaient pas le jeu, mais qui visuellement étaient dérangeants.


- **Flavie** : Création et finalisation de l'historique.

- **Timothée** : Création d'un menu pour afficher les règles entre le menu principal et le menu de sélection des personnages dans **main_menu.py**.

#### 10/05/2025 :

- **Timothée** : Finalisation de l'écriture des règles et création d'un résumé des statistiques du jouer à la fin de la partie dans **jeu.py**.



[***Lien notion***](https://www.notion.so/Projet-Transverse-Equipe-A8-18f30068216c806396a2f057d07e91ca?pvs=4)
