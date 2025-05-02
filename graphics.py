import pygame
from pygame.locals import *
from assets import Card, Pile
from gameslogic import Solitaire
from constants import *

class Menus:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

    def draw(self):
        pass

class StartMenu(Menus):
    def __init__(self, screen):
        super().__init__(screen)
        self.games_list = GAMES_AVAILABLES
        self.width = self.screen_width * MAIN_MENU_RATIO
        self.height = self.screen_height * MAIN_MENU_RATIO
        self.menu = pygame.Surface((self.width, self.height))

        self.menu_x = self.screen_width/2 - self.width/2
        self.menu_y = self.screen_height/2 - self.height/2
        
        self.background = pygame.Rect(0, 0, self.width, self.height)
        self.title_1 = Texts("Choose your")
        self.title_2 = Texts("GAME", text_size=72)
        self.credits = Texts("Made by me")
        self.title_1_dimensions = self.title_1.width, self.title_1.height
        self.title_2_dimensions = self.title_2.width, self.title_2.height
        self.credits_dimensions = self.credits.width, self.credits.height

        close_dims = self.width/10
        close_x = self.width - close_dims
        self.close_button = Buttons(close_x, 0, close_dims, close_dims, (0,100,0), "X", (50,100,50))
        
        self._get_games_buttons()

    def _get_games_buttons(self):
        self.games_buttons = []
        button_height = self.height/10
        
        # Cas de un à trois jeux, fera une colonne centrée. Toutes valeurs relatives à la taille de l'écran.
        if NB_GAMES_AVAILABLES <= 3:
            button_width = self.width/2
            x = (self.width/2) - button_width / 2
            y = self.height/2
            off_set = button_height * 1.5

            for game in self.games_list:
                button = Buttons(x, y, button_width, button_height, (0,100,0), game)
                self.games_buttons.append(button)
                y += off_set
        
        # Cas de 4 à 6 jeux, fera deux colonnes réparties équitablement autour du centre (toujours relatif).
        elif NB_GAMES_AVAILABLES > 3 and NB_GAMES_AVAILABLES <= 6:
            button_width = self.width/4
            off_set = button_height * 1.5
            y = self.height / 2
            
            i = 0
            while i < NB_GAMES_AVAILABLES:
                x = (self.width/3) - (2 * (button_width / 3))
                button = Buttons(x, y, button_width, button_height, (0,100,0), self.games_list[i])
                self.games_buttons.append(button)
                y += off_set
                i += 1
            
            y = self.height / 2
            while i < NB_GAMES_AVAILABLES:
               
                x = (self.width / 2) + (button_width / 3)
                button = Buttons(x, y, button_width, button_height, (0,100,0), self.games_list[i])
                self.games_buttons.append(button)
                i += 1
                y += off_set
        
        # Cas de plus de 6 jeux. SI JAMAIS plus de 9 jeux, changer la méthode de display (de toute façon, ça sera moche).
        else :
            button_width = self.width / 6
            off_set = button_height * 1.5
            y = self.height / 2

            i = 0
            while i < 3:
                x = 3 * button_width/4
                button = Buttons(x, y, button_width, button_height, (0,100,0), self.games_list[i])
                self.games_buttons.append(button)
                y += off_set
                i += 1
            
            y = self.height / 2
            while i >= 3 and i < 6:
                x = (self.width/2) - (button_width/2)
                button = Buttons(x, y, button_width, button_height, (0,100,0), self.games_list[i])
                self.games_buttons.append(button)
                y += off_set
                i += 1
            
            y = self.height / 2

            while i < NB_GAMES_AVAILABLES:
                x = (self.width/2) + (button_width * 1.25)
                button = Buttons(x, y, button_width, button_height, (0,100,0), self.games_list[i])
                self.games_buttons.append(button)
                y += off_set
                i += 1

        for button in self.games_buttons:
            button.hover_color = (0,0,0)

        return self.games_buttons

    def draw_menu(self):
        pygame.draw.rect(self.menu, (50,250,50), self.background)
        for button in self.games_buttons:
            button.draw_button(self.menu)
        
        self.close_button.draw_button(self.menu)
        
        self.title_1.draw_text(self.menu, self.width/2 - self.title_1_dimensions[0]/2, self.height/4)
        self.title_2.draw_text(self.menu, self.width/2 - self.title_2_dimensions[0]/2, self.height/4 + self.title_1_dimensions[1])
        self.credits.draw_text(self.menu, self.width - self.credits_dimensions[0], self.height - self.credits_dimensions[1])

        self.screen.blit(self.menu, (self.menu_x, self.menu_y))

class InGameMenus(Menus):
    def __init__(self, screen):
        super().__init__(screen)
        self.width = self.screen_width * GAME_MENU_RATIO
        self.height = self.screen_height * GAME_MENU_RATIO
        self.new_game = Buttons(0, 0, 10, 10, (0,0,0), "New Game", (250, 0, 0))
        self.quit_game = Buttons(0, 0, 10, 10, (0,0,0), "Quit Game", (250, 0, 0))
        self.score = Texts("Score is:", text_size=24)
        self.time = Texts("Time:", 24)


class Buttons:
    def __init__(self, x, y, width, height, color=(0,0,0), text=None, hover_color=None):
        self.rect = pygame.Rect(int(x), int(y), int(width), int(height))
        self.color = color
        self.text = text
        self.hover_color = hover_color if hover_color else color
        self.is_hovered = False
        self.font = pygame.font.Font(None, 25)

    def draw_button(self, surface):
        current_color = self.hover_color if self.is_hovered else self.color

        pygame.draw.rect(surface, current_color, self.rect)
        pygame.draw.rect(surface, (0,0,0), self.rect, 2)

        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

class Texts:
    def __init__(self, text, text_size=36, text_color=(0,0,0), font=None):
        self.text_color = text_color
        self.font = pygame.font.Font(font, text_size)
        self.update_text(text)

    def update_text(self, text):
        self.surface = self.font.render(text, True, self.text_color)
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()        

    def draw_text(self, surface, x, y):
        surface.blit(self.surface, (x , y))

class CardsGraphics:
    def __init__(self, card, card_surface, position=(0,0)):
        self.card = card
        self.surface = card_surface
        self.position = position
        self.rect = self.surface.get_rect(topleft=position)
        self.visible_rect = None # Sera attribué plus tard, en faisant appel à resize_cards()

    def draw_card_graphics(self, screen):
        self.rect.topleft = self.position
        self.visible_rect.topleft = self.position
        screen.blit(self.surface, self.position)
        pygame.draw.rect(screen, (0,0,0), self.rect, 2)
        pygame.draw.rect(screen, (255,0,0), self.visible_rect, 2)
        

class SolitaireGraphics:
    def __init__(self, screen, solitaire_game):
        self.screen = screen
        self.game = solitaire_game
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.plateau = pygame.Surface((self.screen_width, self.screen_height))
        self.plateau.fill((50, 250, 50))
        self.solitaire_menu = InGameMenus(self.screen)

    def get_card_dim(self):
        column_number = NUM_COL_SOLITAIRE
        bordures_ratio = BORDURES_RATIO_SOLITAIRE
        gap_ratio = GAP_RATIO_SOLITAIRE
        total_spaces = (2 * bordures_ratio) + ((column_number -1) * gap_ratio)

        self.card_width = self.screen_width / (column_number + total_spaces)
        self.card_height = self.card_width / FRENCH_SUIT_CARD_RATIO

        return self.card_width, self.card_height
    
    def init_card_stands_positions(self):
        self.left_stands_positions = [] # Positions de la pioche[0] et de la défausse[1].
        self.right_stands_positions = [] # Positions des foundations [0] à [4].
        self.tableaus_positions = [] # Positions des tableaus [0] à [6].
        self.card_width, self.card_height = self.get_card_dim()
        self.bordures_size = self.card_width * BORDURES_RATIO_SOLITAIRE
        self.left_side = pygame.Surface((self.card_width + (2 * self.bordures_size), (self.screen_height - self.card_height)))
        self.right_side = pygame.Surface((self.card_width + (2 * self.bordures_size), (self.screen_height - self.card_height)))
        self.lower_side = pygame.Surface((self.screen_width, self.card_height))
        
        y_offset = 2 * self.bordures_size  # Ajout de card_height pour l'offset vertical
        for _ in range(2):
            position = [self.bordures_size, y_offset]
            self.left_stands_positions.append(position)
            y_offset += self.card_height + self.bordures_size
        
        self.draw_rect = pygame.Rect(self.left_stands_positions[0][0], self.left_stands_positions[0][1], self.card_width, self.card_height)

        y_offset = 2 * self.bordures_size
        for _ in range(4):
            position = [self.screen_width - self.card_width - self.bordures_size, y_offset]
            self.right_stands_positions.append(position)
            y_offset += self.card_height + self.bordures_size
        
        available_width = self.screen_width - ((9 * self.card_width) + (4 * self.bordures_size))
        space_between_tableaus = available_width / 8
        y = 2 * self.bordures_size
        x_offset = self.card_width + (2 * self.bordures_size) + space_between_tableaus
        for _ in range(7):
            position = [x_offset, y]
            self.tableaus_positions.append(position)
            x_offset += self.card_width + space_between_tableaus
    
    def resize_cards(self):
        for key, cardgraph in self.card_visuals.items():
            scaled_surface = pygame.transform.scale(cardgraph.surface, (self.card_width, self.card_height))
            visible_scaled_surface = pygame.transform.scale(cardgraph.surface, (self.card_width, self.card_height * TABLEAUS_PACING))
            cardgraph.surface = scaled_surface
            cardgraph.rect = scaled_surface.get_rect(topleft=cardgraph.position)
            cardgraph.visible_rect = visible_scaled_surface.get_rect(topleft=cardgraph.position)
        
        self.back_card_visual = pygame.transform.scale(self.back_card_visual, (self.card_width, self.card_height))

    def draw_plateau(self):
        if not hasattr(self, 'left_stands_positions'):
            self.init_card_stands_positions()
            self.resize_cards()

        card_stand = pygame.Surface((self.card_width, self.card_height))
        
        # Remplir les surfaces
        stand_rect = card_stand.get_rect()
        card_stand.fill((50, 190, 50))
        self.left_side.fill((50, 190, 50))
        self.right_side.fill((50, 190, 50))
        self.lower_side.fill((128, 128, 128))
        pygame.draw.rect(card_stand, (0, 0, 0), stand_rect, 2)
        
        # Dessiner les card stands sur les côtés en utilisant les positions précalculées
        stock_position = self.left_stands_positions[0][0], self.left_stands_positions[0][1]
        waste_position = self.left_stands_positions[1][0], self.left_stands_positions[1][1]

        if len(self.game.stock.cards) < 1:
            self.left_side.blit(card_stand, stock_position)
        elif len(self.game.stock.cards) >= 1:
            self.left_side.blit(self.back_card_visual, stock_position)
        
        if len(self.game.waste.cards) < 1:
            self.left_side.blit(card_stand, waste_position)
        elif len(self.game.waste.cards) >= 1:
            to_show = (self.game.waste.cards[-1].suit, self.game.waste.cards[-1].value)
            self.card_visuals[to_show].position = waste_position
            self.card_visuals[to_show].draw_card_graphics(self.left_side)
        # i = 0
        # for pos in self.left_stands_positions:
        #     # Ajuster la position relative à left_side (soustraire l'offset vertical)
        #     relative_pos = (pos[0], pos[1] - self.card_height)
        #     if i == 0 and len(self.game.stock.cards) < 1:
        #         self.left_side.blit(card_stand, relative_pos)
        #     elif i == 0 and len(self.game.stock.cards) >= 1:
        #         self.left_side.blit(self.back_card_visual, relative_pos)

        #     if i == 1 and len(self.game.waste.cards) < 1:
        #         self.left_side.blit(card_stand, relative_pos)
        #     elif i == 1 and len(self.game.waste.cards) >= 1:
        #         to_show = (self.game.waste.cards[-1].suit, self.game.waste.cards[-1].value)
        #         self.card_visuals[to_show].position = relative_pos
        #         self.card_visuals[to_show].draw_card_graphics(self.left_side)
        #     i += 1
        
        i = 0
        for pos in self.right_stands_positions:
            # Ajuster la position relative à right_side (soustraire l'offset vertical et horizontal)
            relative_pos = (self.bordures_size, pos[1])
            if len(self.game.foundations[i].cards) < 1:
                self.right_side.blit(card_stand, relative_pos)
            elif len(self.game.foundations[i].cards) <= 1:
                to_show = (self.game.foundations[i].cards[-1].suit, self.game.foundations[i].cards[-1].value)
                self.card_visuals[to_show].position = pos
                self.card_visuals[to_show].draw_card_graphics(self.right_side)
            i += 1
        
        i = 0
        for pos in self.tableaus_positions:
            if len(self.game.tableaus[i].cards) < 1:
                self.plateau.blit(card_stand,(pos[0], pos[1]))
            elif len(self.game.tableaus[i].cards) >= 1:
                current_pos = pos.copy()
                for card in self.game.tableaus[i].cards:
                    if not card.revealed:
                        self.plateau.blit(self.back_card_visual, current_pos)
                    else:
                        to_show = (card.suit, card.value)
                        self.card_visuals[to_show].position = current_pos
                        self.card_visuals[to_show].draw_card_graphics(self.plateau)
                    current_pos[1] += self.card_height * TABLEAUS_PACING
            i += 1

        # Ajouter les surfaces au plateau principal
        self.plateau.blit(self.left_side, (0, 0))
        self.plateau.blit(self.right_side, (self.screen_width - self.right_side.get_width(), 0))
        self.plateau.blit(self.lower_side, (0, self.screen_height - self.card_height))

    def get_cards_graphics(self): # Attention, méthode a appeler AVANT de distribuer les cartes (méthode initialize_game() de gameslogic).
        # Crée le dictionnaire qui contiendra les surfaces au format {(card.suit, card.value): surface}.
        self.card_visuals = {}
        self.full_deck = pygame.image.load("graphics/Cardsuits.jpg")

        # Le dictionnaire card_line est en dur parce que l'image est organisée comme ça.
        card_line = {"Atout": 4, "Pique": 3, "Trefle": 1, "Coeur": 2, "Carreau": 0}
        for card in self.game.deck.cards:
            if card.suit not in card_line or not (1 <= card.value <= 13):
                raise ValueError(f"Invalid card suit or value: {card.suit}, {card.value}")
            y = card_line[card.suit] * FRENCH_SUIT_CARD_HEIGHT
            x = (card.value - 1) * FRENCH_SUIT_CARD_WIDTH

            card_surface = self.full_deck.subsurface(x, y, FRENCH_SUIT_CARD_WIDTH, FRENCH_SUIT_CARD_HEIGHT)
            self.card_visuals[(card.suit, card.value)] = CardsGraphics(card, card_surface)
        
        self.back_card_visual = self.full_deck.subsurface((2 * FRENCH_SUIT_CARD_WIDTH), (4 * FRENCH_SUIT_CARD_HEIGHT), FRENCH_SUIT_CARD_WIDTH, FRENCH_SUIT_CARD_HEIGHT)