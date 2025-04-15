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


class SolitaireGraphics:
    def __init__(self, screen, solitaire_game):
        self.screen = screen
        self.game = solitaire_game
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

    def get_card_dim(self):
        column_number = NUM_COL_SOLITAIRE
        bordures_ratio = BORDURES_RATIO_SOLITAIRE
        gap_ratio = GAP_RATIO_SOLITAIRE
        total_spaces = (2 * bordures_ratio) + ((column_number -1) * gap_ratio)

        card_width = self.screen_width / (column_number + total_spaces)
        card_height = card_width / FRENCH_SUIT_CARD_RATIO

        return card_width, card_height
    
    def init_card_stands_positions(self):
        self.left_stands_positions = []
        self.right_stands_positions = []
        card_width, card_height = self.get_card_dim()
        bordures_size = card_width * BORDURES_RATIO_SOLITAIRE
        
        y_offset = 2 * bordures_size + card_height  # Ajout de card_height pour l'offset vertical
        for _ in range(2):
            position = (bordures_size, y_offset)
            self.left_stands_positions.append(position)
            y_offset += card_height + bordures_size
        
        y_offset = 2 * bordures_size + card_height
        for _ in range(4):
            position = (self.screen_width - card_width - bordures_size, y_offset)
            self.right_stands_positions.append(position)
            y_offset += card_height + bordures_size
    
    def draw_plateau(self):
        if not hasattr(self, 'left_stands_positions'):
            self.card_width, self.card_height = self.get_card_dim()
            self.bordures_size = self.card_width * BORDURES_RATIO_SOLITAIRE
            self.init_card_stands_positions()

        self.plateau = pygame.Surface((self.screen_width, self.screen_height))
        self.plateau.fill((50, 250, 50))

        left_side = pygame.Surface((self.card_width + (2 * self.bordures_size), (self.screen_height - self.card_height)))
        right_side = pygame.Surface((self.card_width + (2 * self.bordures_size), (self.screen_height - self.card_height)))
        upper_side = pygame.Surface((self.screen_width, self.card_height))
        card_stand = pygame.Surface((self.card_width, self.card_height))
        
        # Remplir les surfaces
        stand_rect = card_stand.get_rect()
        card_stand.fill((50, 190, 50))
        left_side.fill((50, 190, 50))
        right_side.fill((50, 190, 50))
        upper_side.fill((128, 128, 128))
        pygame.draw.rect(card_stand, (0, 0, 0), stand_rect, 2)
        
            # Dessiner les card stands sur les côtés en utilisant les positions précalculées
        for pos in self.left_stands_positions:
            # Ajuster la position relative à left_side (soustraire l'offset vertical)
            relative_pos = (pos[0], pos[1] - self.card_height)
            left_side.blit(card_stand, relative_pos)
        
        for pos in self.right_stands_positions:
            # Ajuster la position relative à right_side (soustraire l'offset vertical et horizontal)
            relative_pos = (self.bordures_size, pos[1] - self.card_height)
            right_side.blit(card_stand, relative_pos)
        
        # Ajouter les surfaces au plateau principal
        self.plateau.blit(left_side, (0, self.card_height))
        self.plateau.blit(right_side, (self.screen_width - right_side.get_width(), self.card_height))
        self.plateau.blit(upper_side, (0, 0))