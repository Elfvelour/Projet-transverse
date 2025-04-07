##############################################
###### Programme Python choix du joueur ######
###### Auteur: Raphael                  ######
###### Version: 1.8                     ######
##############################################

##############################################
import pygame
import os

pygame.init()

WIDTH, HEIGHT = 1920, 1010
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu des Joueurs")

#Couleurs
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
BUTTON_COLOR = (105, 105, 105)
BUTTON_HOVER_COLOR = (169, 169, 169)
BUTTON_BORDER_COLOR = (0, 0, 0)
BUTTON_TEXT_COLOR = (255, 255, 255)

font = pygame.font.SysFont("Roboto", 40)

class Button:
    def __init__(self, x, y, text, width=130, height=50, enabled=True, weapon=False):
        self.x = x
        self.y = y
        self.text = text
        self.width = width
        self.height = height
        self.enabled = enabled
        self.weapon = weapon

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = pygame.Rect((self.x, self.y), (self.width, self.height)).collidepoint(mouse_pos)
        color = BUTTON_COLOR
        color = BUTTON_HOVER_COLOR if is_hovered else color

        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height), border_radius=5)
        pygame.draw.rect(screen, BUTTON_BORDER_COLOR, (self.x, self.y, self.width, self.height), 2, 5)

        text_surface = font.render(self.text, True, BUTTON_TEXT_COLOR)

        text_x = self.x + (self.width - text_surface.get_width()) // 2
        text_y = self.y + (self.height - text_surface.get_height()) // 2
        screen.blit(text_surface, (text_x, text_y))

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        button_rect = pygame.Rect((self.x, self.y), (self.width, self.height))
        return left_click and button_rect.collidepoint(mouse_pos) and self.enabled


#Chargement des images
def load_image(path, x, y):
    if os.path.exists(path):
        return pygame.transform.scale(pygame.image.load(path), (x, y))
    else:
        print(f"Image non trouvée: {path}")
        return pygame.Surface((130, 170))

#Fonction pour découper le texte si trop long pour rentrer
def wrap_text(text, font, max_width):
    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + " " + word if current_line else word
        test_width, _ = font.size(test_line)

        if test_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    lines.append(current_line)  # Ajouter la dernière ligne
    return lines
def run_character_menu() :
    #Image de fond menu joueur
    background_image = load_image("assests/images/menup/backgroundV2.png", WIDTH, HEIGHT)

    #Image des personnages
    p1_img = load_image("assests/images/perso/canard.png", 175, 187.5)
    p2_img = load_image("assests/images/perso/mere_noel.png", 162.5   , 187.5)
    p3_img = load_image("assests/images/perso/einstein.png", 134.6, 206)
    p4_img = load_image("assests/images/perso/jean_soma.png", 150, 220)
    p5_img = load_image("assests/images/perso/squelette.png", 118, 200)


    #Liste d'armes pour chaque personnage
    weapons = {
        "P1": [("Oeuf", "assests/images/armes/oeuf.png","A1"), ("Canard laqué", "assests/images/armes/plat_canard.png","A2")],
        "P2": [("Cadeau", "assests/images/armes/cadeau.png","A1"), ("Biscuit", "assests/images/armes/cookie.png","A2")],
        "P3": [("Fiole rouge", "assests/images/armes/fiole_rouge.png","A1"), ("Fiole bleu", "assests/images/armes/fiole_bleu.png","A2")],
        "P4": [("Discours", "assests/images/armes/discours.png","A1"), ("SWS", "assests/images/armes/logo_sowesign.png","A2")],
        "P5": [("Os", "assests/images/armes/arme_os.png","A1"), ("Tombe", "assests/images/armes/tombe.png","A2")],
    }
    #Position des perso
    padding = 60
    top_spacing = (WIDTH - 5 * 130) // 6
    char_y_top = 60

    characters = [
        (p1_img, (padding, char_y_top), "Canard"),
        (p2_img, (top_spacing + 130 + padding, char_y_top), "Mère Noël"),
        (p3_img, (2 * (top_spacing + 130) + padding, char_y_top), "Einstein"),
        (p4_img, (3 * (top_spacing + 130) + padding, char_y_top), "J-S"),
        (p5_img, (4 * (top_spacing + 130) + padding, char_y_top), "Squelette")
    ]

    character_description = {
        "P1" : ["Ce légendaire combattant anatidés utilise ces compagnons pour attaquer son adversaire.","Quoi de mieux que sa progéniture pour arme ?","Toute sa famille est passée à la casserole."],
        "P2" : ["Elle n'a pas besoin de son mari pour livrer des cadeaux explosifs.","Visiblement, tu as été un vilain petit garnement...","Ses biscuits ont eu le temps de bien durcir depuis le temps."],
        "P3" : ["Ce scientifique fou revient encore une fois pout tout faire sauter.","On dit que cette fiole renferme du polonium.","On dit que cette fiole renferme du radium."],
        "P4" : ["Le plus grand professeur des matières littéraires.","Qui a dit que des actions valaient mieux que mille mots ?","Et hop là, une absence non-excusée."],
        "P5" : ["Elle est revenu d'entre les morts pour se venger de son ex.","Elle a tellement la haine qu'elle utilise son propre corps.","Un gros KAYOUX est utile pour se protéger."]
    }

    #Position bouton
    button_width = 200
    button_height = 50
    spacing = (WIDTH - 5 * button_width) // 6

    #Boutons des perso
    character_buttons = [
        Button(padding + i * (spacing + button_width), char_y_top + 180, name, width=button_width)
        for i, (char_img, (x, y), name) in enumerate(characters)
    ]

    #Booléen pour savoir si arme/personnage sélectionné
    selected_character = None
    selected_weapon = None

    running = True
    while running:
        screen.blit(background_image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Affichage des personnages
        for i, (char_img, (x, y), name) in enumerate(characters):
            #Permet de centrer image/bouton
            image_x = padding + i * (spacing + button_width) + (button_width - char_img.get_width()) // 2
            screen.blit(char_img, (image_x, char_y_top))

        #Affichage des boutons
        for i, button in enumerate(character_buttons):
            button.draw(screen)
            if button.check_click():
                selected_character = f"P{i + 1}"  # Ex: P1, P2, ...
                print(f"{selected_character} sélectionné !")

        #Affichage des info/arme
        if selected_character:
            #Affichage du rectangle
            rect_x = 50
            rect_y = 400
            rect_width = WIDTH - 100
            rect_height = 300
            pygame.draw.rect(screen, (135, 206, 250), (rect_x, rect_y, rect_width, rect_height), border_radius= 10)
            pygame.draw.rect(screen, (128, 0, 32), (rect_x, rect_y, rect_width, rect_height), 10, border_radius=10)



            #Affichage de l'image du perso+nom
            if selected_character == "P1":
                character_img = p1_img
                name_text = "Canard"
            elif selected_character == "P2":
                character_img = p2_img
                name_text = "Mère Noël"
            elif selected_character == "P3":
                character_img = p3_img
                name_text = "Einstein"
            elif selected_character == "P4":
                character_img = p4_img
                name_text = "Jean-Soma"
            elif selected_character == "P5":
                character_img = p5_img
                name_text = "Squelette"
            screen.blit(character_img, (rect_x + 20, rect_y + 50))
            text_surface = font.render(name_text, True, BLACK)
            screen.blit(text_surface, (rect_x + 20, rect_y + 10))

            # Affichage des armes du perso sélectionné
            y_offset = 120

            # Texte en rapport avec le perso + arme
            text_character = font.render(character_description[selected_character][0], True, WHITE)
            screen.blit(text_character, (rect_x + 200, rect_y + 20))

            text_weapon1 = font.render(character_description[selected_character][1], True, WHITE)
            screen.blit(text_weapon1, (rect_x + 170, rect_y + y_offset + 20))

            text_weapon2 = font.render(character_description[selected_character][2], True, WHITE)
            screen.blit(text_weapon2, (rect_x + 170, rect_y + 2 * y_offset - 20))

            for i, (weapon_name, weapon_img_path, weapon_code) in enumerate(weapons[selected_character]):

                # Nom de l'arme
                weapon_text = f"{weapon_name}"

                #Centré le texte+bouton
                text_surface = font.render(weapon_text, True, BLACK)
                text_width = text_surface.get_width()
                text_x = 1000 + (190 // 2) - (text_width // 2)
                screen.blit(text_surface, (text_x + 40 + 80, rect_y + y_offset + 40))

                #Image de l'arme
                weapon_img = load_image(weapon_img_path, 60, 60)
                screen.blit(weapon_img, (rect_x + 850 + 100, rect_y + y_offset))

                #Bouton d'arme
                x_button = Button(rect_x + 1000 + 80, rect_y + y_offset, "Sélectionner", width=180, height=40)
                x_button.draw(screen)


                #Code du perso + arme choisi avec affichage de sécurité
                if x_button.check_click():
                    weapon = f"{weapon_code}"
                    character = f"{selected_character}"
                    print(f"{selected_character} a sélectionné l'arme: {selected_weapon}")
                    running = False

                y_offset += 80

        pygame.display.flip()

    return (character, weapon)
