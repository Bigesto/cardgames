import pygame
pygame.init()
window = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Mon premier jeu Pygame")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    window.fill((0, 0, 0))  # Fond noir
    pygame.display.flip()  # Met à jour l'écran

pygame.quit()