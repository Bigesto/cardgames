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
            
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     if not self.in_game:
            #         for button in self.start_menu.games_buttons:
            #             if button.rect.collidepoint(event.pos):
                            

            if event.type == pygame.MOUSEMOTION:
                if not self.in_game:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    local_mouse_x = mouse_x - self.start_menu.menu_x
                    local_mouse_y = mouse_y - self.start_menu.menu_y
                    for button in self.start_menu.games_buttons:
                        if button.rect.collidepoint((local_mouse_x, local_mouse_y)):
                            button.is_hovered = True
                        else:
                            button.is_hovered = False
    
    def update(self):
        # Mise à jour de la logique du jeu
        pass
    
    def render(self):
        # Dessin sur l'écran
        self.screen.fill((0, 0, 0))  # Fond noir

        if not self.in_game:
            self.start_menu.draw_menu()


        # self.graphics = SolitaireGraphics(self.screen)
        # self.graphics.draw_plateau()
        # self.screen.blit(self.graphics.plateau, (0,0))

        
        pygame.display.flip()
    
    def run(self):
        # Boucle principale du jeu
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(30)  # 30 FPS
        
        # Nettoyage à la fin
        pygame.quit()


