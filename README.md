# Projet-transverse Bow Master [](https://github.com/Elfvelour/Projet-transverse/blob/main/assets/images/menup/logo.png)

## Contributeurs:

#### - Timothée Girault :

[![main_menu.py](https://img.shields.io/badge/main_menu-blue)](main_menu.py) : création du menu principal du jeu ainsi que les paramètres pour changer de musique et l'allumer ou l'éteindre

[![main.py](https://img.shields.io/badge/main-red)](main.py) : résolution des bugs

#### - Flavie Brémand :

[![jeu.py](https://img.shields.io/badge/jeu-green)](jeu.py) : gestion de l'alternance entre le joueur et le bot, affichage de l'explosion et boucle principale

[![trajectoires.py](https://img.shields.io/badge/trajectoire.py-green)](trajectoires.py) : calcul de la trajectoire du tir du joueur et de la puissance du tir en fonction du clic gauche, gestion des images d'explosion

[![bot.py](https://img.shields.io/badge/jeu-green)](bot.py) : bases du bot (sa position et début des fonctions pour son lancer)

[![main.py](https://img.shields.io/badge/main-red)](main.py) : création de l'ancienne version

#### - Noémie Marques :

[![monnaie.py](https://img.shields.io/badge/monnaie-purple)](monnaie.py) :

[![main.py](https://img.shields.io/badge/main-red)](main.py) :

#### - Thomas Aubert :

[![trajectoires.py](https://img.shields.io/badge/trajectoire.py-green)](trajectoires.py) :

[![bot.py](https://img.shields.io/badge/bot-green)](bot.py) :


#### - Rafaël De Jesus Coelho :

[![menu_joueur.py](https://img.shields.io/badge/menu_joueur-blue)](menu_joueur.py) :

## Carnet de bord:

Nom du jeu : BOW MASTER

Type de jeu : jeu de tir

Nombre de joueur(s) : un contre le bot de difficulté croissante

But : tuer le bot en lui infligeant des dégâts grâce aux projectiles lancés

#### Février 2025 :

##### -03/02/2024:
- __Noémie__: Organisation des fichiers du jeu sur le fichier ***contenu.txt***

##### -04/02/2025:
- __Noémie__: Création des statistiques des armes sur le fichier ***gestion_stats.json***

##### -09/02/2025:
- __Noémie__: Initialisation de la fonction run_game dans le fichier ***main.py*** + invention des descriptions

##### -10/02/2025:
- __Noémie__: Initialisation de la fonction ***monnaie.py***


- __Timothée__: Initialisation du fichier ***main_menu.py*** et suppression de l'ancien fichier menu.py pour repartir 
d'une base saine après de nombreux tests sur ce dernier

##### -23/02/2025:
- __Flavie__: Mise en place du lancement du projectile par clic gauche et de la ligne blanche qui montre le début de la trajectoire

##### -24/02/2025:
- __Noémie__: Le joueur gagne une pièce à chaque fois qu'il tire


- __Timothée__: Création de la fenêtre du jeu de taille 1920 par 1024 ainsi que des boutons "jouer" et "quitter"
dans le fichier ***main_menu.py***. Je teste les différentes couleurs comme le rouge, rouge bordeaux ou le noir pour les boutons 
ou le fond

##### -28/02/2025:
- __Flavie__: Mise en place de la puissance de la trajectoire parabole (vitesse en fonction du temps du clic gauche)


- __Timothée__: J'ai créé une fonction pour détecter le clic de la souris sur une surface rectangulaire tel qu'on appuie sur 
le bouton quitter cela fait fermer la fenêtre. Puis j'ai initialisé la musique avec une boucle infinie avec la bibliothèque pygame 
dans le fichier ***main_menu.py***.

#### Mars 2025 :

##### -03/03/2025:
- __Flavie__: Ajustements dans la trajectoire (notamment sur la vitesse et l'angle)
                      Création du fichier bot et début de son code
                      Séparation des fichiers ***main.py*** et ***trajectoires.py*** pour plus de clarté


- __Noémie__: Recherche des assets pour les armes du jeu
                      Modification du .json pour correspondre au choix du joueur

##### -14/03/2025:
- __Noémie__: Ajout du bouton pour utiliser l'ultime coup du personnage 

##### -15/03/2025:
- __Timothée__: Création d'une fonction pour animer les boutons tels qu'on appuie dessus cela lui donne une couleur plus sombre.
Par exemple, j'utilise le rouge et le rouge bordeaux pour l'animation. Et une autre pour qu'on puisse changer de musique. J'ai mis
au propre les ***assets*** en les classant en 2 types les images et les sons puis dans les images dans différents dossiers pour chacune
fichiers du jeu comme ***menup*** pour ***main_menu.py***etc. J'ai recherché de nouvelles images pour le jeu ainsi que 
le redimensionnement du fond d'écran sur gimp.

##### -24/03/2025:
- __Flavie__: Améliorations des trajectoires et du bot (gravité et projectiles)
                    Ajustement du positionnement des images d'explosion (centrées par rapport au projectile)

##### -25/03/2025:
- __Timothée__: Après avoir mis au propre les ***assets***, j'ai continué de faire le ménage en supprimant et remplacent 
certaines par d'autres plus pertinentes et esthétiques. Lors de toutes les modifications d'images trouvées sur internet, j'ai utilisé
GIMP qui fut d'une grande utilité pour moi. J'ai aussi corrigé le bug du son de la potion en s'activant une fois
et non plus à chaque rafraichissement de la fenêtre dans ***trajectoires.py***.

#### Avril 2025 :

#### -03/04/2025:
- __Timothée__: J'ai commencé à commenter mon code pour que chaque personne du groupe puisse comprendre le mien
et lors de problèmes sur le code, que j'arrive plus facilement à comprendre l'erreur. J'ai aussi créé le bouton "revenir en arrière" pour
revenir en arrière lors du lancement du jeu prévu initialement. Il s'agit d'un bouton en 2 parties la partie caché le bouton physique
caché par le fond d'écran et la partie visible l'image du bouton.

##### -06/04/2025:
 
- __Flavie__: Refonte de la boucle principale
                    Positionnement correct des images d'explosion (SUR le sol)
                    Essais d'instauration pour le bot de plages de valeurs où tirer


- __Timothée__: Après beaucoup d'efforts, de problèmes et d'énervements, j'ai réussi pour la première fois à relier chaque fichier pour
que le jeu soit enfin fonctionnel soit entre ***main_menu.py*** et ***trajectoires.py*** dans le fichier ***main.py***. J'attends que 
Raphaël finisse son fichier ***menu_joueur.py*** pour le joindre au***main.py***. J'ai fait une refonte complète pour la musique en créant
une classe dédiée pour ce dernier avec 2 bibliothèques, une de son et une de musique. J'ai refait toutes les fonctions précédemment créer pour la musique
et créer deux fonctions pour changer et arrêter la musique. Enfin la création du bouton paramètre pour faire un menu translucide et changer de musique.


##### -07/04/2025:
 
- __Flavie__: Améliorations dans ***trajectoires.py*** pour plus de clarté
                    Séparation du fichier en plusieurs : ***trajectoires.py*** (sol et trajectoire du joueur), ***joueur.py***, ***bot.py***,***jeu.py***
                    Rectifications qui en découlent dans le main


##### -10/04/2025:

- __Timothée__: Refonte graphique du jeu en modifiant le fond d'écran. J'ai utilisé openart.ai pour améliorer le fond d'écran. Puis j'ai
utilisé GIMP pour redimensionner les images. J'ai changé les couleurs des boutons : `rgb(255, 215, 0)` le jaune doré et `rgb(230, 170, 80)` le jaune moutarde.
Création du menu paramètre translucide avec la bibliothèque pygame. Simplification du code : pour avoir un code plus lisible et plus simple, j'ai regroupé
les lignes de codes de ma boucle principales dans des fonctions. Puis j'ai simplifié leurs expressions jusqu'à avoir 2 lignes de codes dans ma
boucle principale sans compter les lignes de bases pour lancer le jeu.

##### -14/04/2025:

- __Timothée__:  Après avoir eu de nouveau un *main* qui ne marchait pas, je me suis remis au travail pour trouver une solution. Et après
quelques tentatives, j'ai réussi à avoir un *main* fonctionnel avec tous les fichiers du projet. J'ai aussi refait un ménage des assets
pour en remplacer et supprimer certains pour avoir une charte graphique à peu près homogène. Enfin, j'ai résolu le problème de 
rafraichissement du menu des paramètres en changeant les conditions pour qu'il apparaisse. J'ai mis en place pour le bouton "en avant" pour
la musique un délai de temps avec la bibliothèque time avec un intervalle de 1s pour changer de musique.


##### -17/04/2025:
- __Timothée__: J'ai affiché l'interface de la musique sur le menu des paramètres avec les boutons "jouer" et "pause" et "en avant" et "en arrière".
Puis j'ai ajouté dans ***main_menu.py*** dans la fonction *Menu_parametre()* des lignes de codes pour afficher les crédits.
Je l'ai mis dans la police souhaitée avec nos noms respectifs.

##### -19/04/2025:
- __Timothée__:  Après quelques heures, j'ai résolu le problème d'affichage du bouton jouer et arrêter avec un booléen sur le fichier ***main_menu.py***. Puis j'ai mis
les bonnes fonctions pour arrêter et jouer de la musique. Et on a rajouté une condition en plus lorsqu'on change de musique cela reste
sur le logo pause. On a donc un menu qui permet de faire pause et jouer de la musique en changeant en avant ou arrière la chanson parmi la liste.

##### -20/04/2025:
- __Timothée__: J'ai réussi après quelque temps à pouvoir utiliser les paramètres tout le temps sur le jeu en mettant la fonction
*affichage_paramètre()* dans les fichiers ***jeu.py*** et ***menu_joueur.py***. On a donc un menu des paramètres fonctionnel dans le jeu.

#### -22/04/2025:
- __Timothée__: En faisant quelques tests sur le jeu pour vérifier que mon code n'avait pas d'erreurs, je m'aperçois qu'on peut cliquer 
sur les personnages et lancer le jeu tandis que le menu des paramètres est lancé. Le même problème est apparu sur le lancer des projectiles avec le menu ouvert.
Je résous le problème en rajoutant la condition de fermeture du menu pour qu'on puisse choisir son personnage sur le fichier ***menu_joueur.py***.
Et sur le fichier ***jeu.py***, je rajoute la même condition en rajoutant une limite d'angle de 95° du tireur pour qu'on ne puisse pas tirer immédiatement
lorsque qu'on sort du menu.

#### -25/04/2025:
- __Timothée__: J'ai raccordé les différents bruitages aux personnages à l'aide de ma bibliothèque de bruitages dans ***main_menu.py***.
Maintenant quand un personnage lance son arme et touche le sol ou le bot, cela produit un son.

[***lien notion***](https://www.notion.so/Projet-Transverse-Equipe-A8-18f30068216c806396a2f057d07e91ca?pvs=4)
