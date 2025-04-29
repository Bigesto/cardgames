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
        self.screen_width = 1024
        self.screen_height = 768
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
                        mouse_pos = pygame.mouse.get_pos()
                        pygame.draw.circle(self.screen, (255, 0, 255), mouse_pos, 5)  # Purple dot
                        pygame.display.update()  # Force an update to see it

                        if self.graphics.draw_rect.collidepoint(mouse_pos):
                            if len(self.game.stock.cards) > 0:
                                self.game.solitaire_draw_card()
                            else:
                                self.game.stock.make_pile(self.game.waste)
                        
                        elif len(self.game.waste.cards) > 0:
                            accessible_card_in_waste = self.game.waste.cards[-1]
                            waste_card = (accessible_card_in_waste.suit, accessible_card_in_waste.value)
                            rect_pos = self.graphics.card_visuals[waste_card].rect.topleft
                            rect_size = self.graphics.card_visuals[waste_card].rect.size
                            print(f"Mouse position: {mouse_pos}")
                            print(f"Rectangle position: {rect_pos}, size: {rect_size}")
                            print(f"Is the mouse in rectangle? {self.graphics.card_visuals[waste_card].rect.collidepoint(mouse_pos)}")
                            print(f"Mouse check: {rect_pos[0] <= mouse_pos[0] <= rect_pos[0] + rect_size[0]} and {rect_pos[1] <= mouse_pos[1] <= rect_pos[1] + rect_size[1]}")
                            print(f"Last card in draw is {self.game.stock.cards[-1].suit}, {self.game.stock.cards[-1].value}")
                            print(f"Last card in waste is {accessible_card_in_waste.suit, accessible_card_in_waste.value}")
                            # if self.graphics.card_visuals[waste_card].rect.collidepoint(mouse_pos):
                            #     self.game.clic_card(accessible_card_in_waste)
                        
                        
                        # À faire : un switch-case (match-case en l'occurence))
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