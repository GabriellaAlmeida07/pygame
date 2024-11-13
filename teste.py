import pygame
from pygame.locals import *

# Inicializa o Pygame
pygame.init()

# Definindo a largura e altura da tela
WIDTH, HEIGHT = 1080, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo com Fundo de Imagem")
fundo_img = pygame.image.load("espaco.jpg")
fundo_img = pygame.transform.scale(fundo_img, (WIDTH, HEIGHT))  # Redimensiona para caber na tela

clock = pygame.time.Clock()

def game_loop():
    running = True 
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        
        # Desenha a imagem de fundo
        screen.blit(fundo_img, (0, 0))
        
        # Atualiza a tela
        pygame.display.update()
    
    pygame.quit()

if __name__ == '__main__':
    game_loop()
