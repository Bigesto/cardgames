import pygame
from pygame.locals import *
from assets import Card, Deck, DeckType, Pile
from gameslogic import Solitaire
from graphics import SolitaireGraphics, StartingMenu

class App:
    def __init__(self):
        # Initialisation de Pygame
        pygame.init()
        
        # Configuration de base
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Jeux de Cartes")
        
        # Variables d'état
        self.running = True
        self.clock = pygame.time.Clock()
        self.in_game = False
        
    def handle_events(self):
        # Gestion des événements (clavier, souris, etc.)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            # Autres gestionnaires d'événements...
    
    def update(self):
        # Mise à jour de la logique du jeu
        pass
    
    def render(self):
        # Dessin sur l'écran
        self.screen.fill((0, 0, 0))  # Fond noir

        if not self.in_game:
            self.start_menu = StartingMenu(self.screen)
            self.start_menu.draw_menu()


        self.graphics = SolitaireGraphics(self.screen)
        self.graphics.draw_plateau()
        self.screen.blit(self.graphics.plateau, (0,0))

        
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


