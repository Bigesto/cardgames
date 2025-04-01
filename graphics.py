import pygame
from pygame.locals import *
from assets import Card, Pile
from gameslogic import Solitaire
from constants import *

class Overlay:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.games = ["Solitaire"]
        menu_witdh = self.screen_width * MAIN_MENU_RATIO
        menu_height = self.screen_height * MAIN_MENU_RATIO

        self.menu = pygame.Surface((menu_witdh, menu_height))

    def draw_start_menu(self):
        games_buttons = []
        button_ratio = 1 / (len(self.games))

        for game in self.games:




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