import pygame
from pygame.locals import *
from assets import Card, Deck, DeckType, Pile
from gameslogic import Solitaire
from graphics import SolitaireGraphics, StartMenu

class App:
    def __init__(self):
        # Initialisation de Pygame
        pygame.init()
        
        # Configuration de base
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Jeux de Cartes")
        
        self.start_menu = StartMenu(self.screen)

        # Variables d'état
        self.running = True
        self.clock = pygame.time.Clock()
        self.in_game = False
        
    def handle_events(self):
        # Gestion des événements (clavier, souris, etc.)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if not self.in_game:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                local_mouse_x = mouse_x - self.start_menu.menu_x
                local_mouse_y = mouse_y - self.start_menu.menu_y

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.start_menu.games_buttons:
                        if button.rect.collidepoint((local_mouse_x, local_mouse_y)):
                            self.active_game = button.text
                            self.load_game()
                            self.in_game = True
                            break
                    
                    if self.start_menu.close_button.rect.collidepoint((local_mouse_x, local_mouse_y)):
                        self.running = False
                            
                if event.type == pygame.MOUSEMOTION:
                    for button in self.start_menu.games_buttons:
                        if button.rect.collidepoint((local_mouse_x, local_mouse_y)):
                            button.is_hovered = True
                        else:
                            button.is_hovered = False

            if self.in_game == True:
                if self.active_game == "Solitaire":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = (pygame.mouse.get_pos())
                        # Supprimé. À faire : un switch-case (match-case en l'occurence))
                        # Un case par localisation de clic, je suppose ? Au moins, je pourrais mettre des breaks clairs entre les cases.
                                


    
    def load_game(self):
        if self.active_game == "Solitaire":
            self.game = Solitaire("easy")
            self.graphics = SolitaireGraphics(self.screen, self.game)
            self.graphics.get_cards_graphics()
            self.game.initialize_game()
            self.graphics.init_card_stands_positions()
            self.graphics.resize_cards()
        
        else:
            self.running = False


    def update(self):
        # Mise à jour de la logique du jeu
        pass
    
    def render(self):
        # Dessin sur l'écran
        self.screen.fill((0, 0, 0))  # Fond noir

        if not self.in_game:
            self.start_menu.draw_menu()
        
        else:
            if self.active_game == "Solitaire":
                self.graphics.draw_plateau()
                self.screen.blit(self.graphics.plateau, (0,0))

        
        pygame.display.flip()
    
    def run(self):
        # Boucle principale du jeu
        while self.running:
            self.render()
            self.handle_events()
            self.update()
            self.clock.tick(30)  # 30 FPS
        
        # Nettoyage à la fin
        pygame.quit()