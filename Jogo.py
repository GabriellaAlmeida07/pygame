import pygame
from pygame.locals import *

# Inicialização do Pygame
pygame.init()

# Largura e altura da tela 
WIDTH, HEIGHT = 1850, 960

# Configuração das imagens 
vaca_img = pygame.image.load("imgs/personagens/vaca.png")
vaca_img = pygame.transform.scale(vaca_img, (300, 200)) # Redimensiona a img 

gato_img = pygame.image.load("imgs/personagens/gato.png")
gato_img = pygame.transform.scale(gato_img, (300, 200)) # Redimensiona a img 

rato_img = pygame.image.load("imgs/personagens/rato.png")
rato_img = pygame.transform.scale(rato_img, (300, 200)) # Redimensiona a img 

botao_start = pygame.image.load("imgs/botoes/botao_start.png")
botao_start = pygame.transform.scale(botao_start, (400, 200)) # Redimensiona a img 

fundo_personagens = pygame.image.load("imgs/fundos/personagens.png")
fundo_personagens = pygame.transform.scale(fundo_personagens, (WIDTH, HEIGHT))  

botao_personag = pygame.image.load("imgs/botoes/personag_botao.png")
botao_personag = pygame.transform.scale(botao_personag, (400, 200)) # Redimensiona a img 

balao_aviso = pygame.image.load("imgs/botoes/balao.png")
balao_aviso = pygame.transform.scale(balao_aviso, (700, 500)) # Redimensiona a img 

# Configuração da janela inicial
janela = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo")
fundo_img = pygame.image.load("imgs/fundos/start.png")
fundo_img = pygame.transform.scale(fundo_img, (WIDTH, HEIGHT))  
clock = pygame.time.Clock()

# Definindo as posições dos botões (parâmetro rect da função desenhar_botao)
# Parâmetros pygame.Rect: posição em x e y, largura e altura 
start_button = pygame.Rect(750, 610, 400, 200) 
gato_button = pygame.Rect(150, 700, 300, 200)
vaca_button = pygame.Rect(730, 700, 300, 200)
rato_button = pygame.Rect(1270, 700, 300, 200)

# Fonte para texto
fonte = pygame.font.Font(None, 70)

# Função para desenhar botão
def desenhar_botao(rect, img, texto, x, y):
    janela.blit(img, (rect.x, rect.y)) # Desenha a imagem do botão
    
    texto_renderizado = fonte.render(texto, True, (255, 255, 255))  
    # Defina a posição desejada através dos parametros x e y
    texto_x = rect.x + x
    texto_y = rect.y + y
    janela.blit(texto_renderizado, (texto_x, texto_y)) # Desenha o texto 


# Função para o menu inicial
def tela_inicial():
    # Desenha o fundo e o botão start
    janela.blit(fundo_img, (0, 0))
    desenhar_botao(start_button, botao_start, "", 0, 0)  
    pygame.display.update()
    
    for event in pygame.event.get():            
        if event.type == QUIT:
            return "sair" 
        
        if event.type == MOUSEBUTTONDOWN and event.button == 1: 
            if start_button.collidepoint(event.pos):
                return "personagens"  
    
    return "menu"

# Tela de escolha do personagem
def tela_personagens():
    personag_escolhido = None
    janela = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Escolha seu Personagem")

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                return 

        janela.blit(fundo_personagens, (0, 0))
        desenhar_botao(vaca_button, botao_personag, "VACA", 120, 85)
        desenhar_botao(rato_button, botao_personag, "RATO", 120, 85)
        desenhar_botao(gato_button, botao_personag, "GATO", 120, 85)
        pygame.display.update()

        for event in pygame.event.get(): 
            if event.type == MOUSEBUTTONDOWN and event.button == 1: 
                if vaca_button.collidepoint(event.pos):
                    personag_escolhido = "vaca" 
                elif gato_button.collidepoint(event.pos):
                    personag_escolhido =  "gato" 
                elif rato_button.collidepoint(event.pos):
                    personag_escolhido =  "rato"
        
                
        if personag_escolhido is not None:
            texto = f"Você escolheu {personag_escolhido}!"
            janela.blit(balao_aviso, (500, 150))
            texto_renderizado = fonte.render(texto, True, (0, 0, 0))  
            janela.blit(texto_renderizado, (620, 360)) 
            pygame.display.update()
            pygame.time.wait(2000)
            return

# Tela viscosidade
def tela_viscosidade():
    None

# Tela gravidade
def tela_gravidade():
    None

# Função principal
def game_loop():
    running = True  # Loop infinito para o jogo
    personagem = None # Será string exemplo: "rato"
    viscosidade = None # Será string exemplo: "mel"
    gravidade = None # Será string exemplo: "lua"

    while running:
        clock.tick(60)

        evento = tela_inicial()  

        if evento == "sair":
            running = False   
        
        elif evento == "personagens":
            personagem = tela_personagens() 
        
        #viscosidade = tela_viscosidade()
        #gravidade = tela_gravidade()

    pygame.quit()

if __name__ == '__main__':
    game_loop()
