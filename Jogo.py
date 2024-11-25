import pygame
from pygame.locals import *
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from matplotlib.animation import FuncAnimation

# Função de animação dos gráficos de tempo e velocidade

def plotar_grafico(g, b, m, H):

    def tempo_queda(g, b, m, H):
        if b == 0:
            def r(t):
                return H - (g * t**2 / 2)
            tempo = fsolve(r, 0)
            return np.linspace(0, tempo[0] * (-1), 100)
        else:
            def r(t):
                T = m/b
                return H - g*t*T + (g*(T**2)*(1 - (1/np.exp(t/T))))
            tempo = fsolve(r, 0)
            
            return np.linspace(0, tempo[0], 100)
    
    def posicao(g, b, m, H, t):

        if b == 0:
            y = H - (g * t**2 / 2)
        else:
            T = m/b
            y = H - g*t*T + (g*(T**2)*(1 - (1/np.exp(t/T))))

        return y

    def velocidade(g, b, m, H, t):

        if b == 0:
            y = -g * t
        else:
            T = m/b
            y = g * T * (1 - (1/np.exp(t / T)))

        return y


    # Define os eixos do gráfico
    t = tempo_queda(g, b, m, H)
    r = posicao(g, b, m, H, t)
    v = velocidade(g, b, m, H, t)

    # Cria a figura em um único eixo, com uma linha vazia a ser atualizada na animação
    fig, (eixo1, eixo2) = plt.subplots(1, 2, figsize=(10, 5))
    line1, = eixo1.plot([], [], label='Posição', color='blue')
    line2, = eixo2.plot([], [], label='Velocidade', color='red')

    # Define os limites do plot
    eixo1.set_xlim(0, max(t))
    eixo1.set_ylim(min(r)*1.1, max(r) * 1.1)
    eixo1.set_title("Posição")
    eixo1.set_xlabel("t (s)")
    eixo1.set_ylabel("r (m)")
    eixo1.legend()

    eixo2.set_xlim(0, max(t))
    eixo2.set_ylim(min(v) * 1.1, max(v) * 1.1)
    eixo2.set_title("Velocidade")
    eixo2.set_xlabel("t (s)")
    eixo2.set_ylabel("v (m/s)")
    eixo2.legend()

    # Inicializa as linhas
    line1.set_data([], [])
    line2.set_data([], [])

    # Função de atualização para a animação
    def update(frame):
        line1.set_data(t[:frame], r[:frame])
        line2.set_data(t[:frame], v[:frame])
        return line1, line2

    # Criando a animação
    ani = FuncAnimation(fig, update, frames=range(1, len(t)), blit=True, interval=15)
    plt.grid()
    plt.show()

# Inicialização do Pygame
pygame.init()

# Largura e altura da tela 
WIDTH, HEIGHT = 1850, 960

# Configuração das imagens dos personagens
vaca_img = pygame.image.load("imgs/personagens/vaca.png")
vaca_img = pygame.transform.scale(vaca_img, (300, 200)) # Redimensiona a img 

gato_img = pygame.image.load("imgs/personagens/gato.png")
gato_img = pygame.transform.scale(gato_img, (300, 200)) # Redimensiona a img 

rato_img = pygame.image.load("imgs/personagens/rato.png")
rato_img = pygame.transform.scale(rato_img, (300, 200)) # Redimensiona a img 

# Configuração das imagens de fundo e dos ambientes de jogo
fundo_img = pygame.image.load("imgs/fundos/start.png")
fundo_img = pygame.transform.scale(fundo_img, (WIDTH, HEIGHT))  

fundo_personagens = pygame.image.load("imgs/fundos/personagens.png")
fundo_personagens = pygame.transform.scale(fundo_personagens, (WIDTH, HEIGHT))  

fundo_gravidade = pygame.image.load("imgs/fundos/gravidade.png")
fundo_gravidade = pygame.transform.scale(fundo_gravidade, (WIDTH, HEIGHT))  

fundo_viscosidade = pygame.image.load("imgs/fundos/viscosidade.png")
fundo_viscosidade = pygame.transform.scale(fundo_viscosidade, (WIDTH, HEIGHT)) 

ambiente_lua = pygame.image.load("imgs/ambientes/lua.jpeg")
ambiente_lua = pygame.transform.scale(ambiente_lua, (WIDTH, HEIGHT))

ambiente_terra = pygame.image.load("imgs/ambientes/terra.png")
ambiente_terra = pygame.transform.scale(ambiente_terra, (WIDTH, HEIGHT))

ambiente_marte = pygame.image.load("imgs/ambientes/marte.jpeg")
ambiente_marte = pygame.transform.scale(ambiente_marte, (WIDTH, HEIGHT))

# Configuração dos botões e adicionais
botao_start = pygame.image.load("imgs/botoes/botao_start.png")
botao_start = pygame.transform.scale(botao_start, (400, 200)) # Redimensiona a img 

botao_padrao = pygame.image.load("imgs/botoes/personag_botao.png")
botao_padrao = pygame.transform.scale(botao_padrao, (400, 200)) # Redimensiona a img 

balao_aviso = pygame.image.load("imgs/botoes/balao.png")
balao_aviso = pygame.transform.scale(balao_aviso, (700, 500)) # Redimensiona a img 

# Configuração da janela inicial
janela = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo")
clock = pygame.time.Clock()

# Rect dos botões. Parâmetros pygame.Rect: posição em x e y (em relação à tela), largura e altura 
start_button = pygame.Rect(750, 610, 400, 200) 
gato_button = pygame.Rect(150, 700, 300, 200)
vaca_button = pygame.Rect(730, 700, 300, 200)
rato_button = pygame.Rect(1270, 700, 300, 200)
agua_button = pygame.Rect(150, 750, 300, 200)
mel_button = pygame.Rect(730, 750, 300, 200)
ar_button = pygame.Rect(1270, 750, 300, 200)
lua_button = pygame.Rect(170, 750, 300, 200)
terra_button = pygame.Rect(740, 750, 300, 200)
marte_button = pygame.Rect(1280, 750, 300, 200)

# Fonte para texto
fonte = pygame.font.Font(None, 70)

# Função para desenhar botão (rect do botão, imagem, texto, x e y do texto)
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
    janela = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Escolha seu Personagem")
    janela.blit(fundo_personagens, (0, 0))
<<<<<<< HEAD
    desenhar_botao(vaca_button, botao_padrao, "VACA", 130, 85)
    desenhar_botao(rato_button, botao_padrao, "RATO", 130, 85)
    desenhar_botao(gato_button, botao_padrao, "GATO", 130, 85)
    pygame.display.update()

    while True:
        personagem_escolhido = None
=======
    desenhar_botao(vaca_button, botao_personag, "VACA", 120, 85)
    desenhar_botao(rato_button, botao_personag, "RATO", 120, 85)
    desenhar_botao(gato_button, botao_personag, "GATO", 120, 85)
    pygame.display.update()

    while True:
        # clock.tick(60)
        # for event in pygame.event.get():
        #     if event.type == QUIT:
        #         return

>>>>>>> b0499209c955a6a05c12adae84c29792ba8997af
        for event in pygame.event.get(): 
            if event.type == MOUSEBUTTONDOWN and event.button == 1: 
                if vaca_button.collidepoint(event.pos):
                    personagem_escolhido = "vaca" 
                elif gato_button.collidepoint(event.pos):
                    personagem_escolhido =  "gato" 
                elif rato_button.collidepoint(event.pos):
<<<<<<< HEAD
                    personagem_escolhido =  "rato"
=======
                    personag_escolhido =  "rato"
            if event.type == QUIT:
                return
>>>>>>> b0499209c955a6a05c12adae84c29792ba8997af
                
        if personagem_escolhido is not None:
            texto = f"Você escolheu {personagem_escolhido}!"
            janela.blit(balao_aviso, (500, 150))
            texto_renderizado = fonte.render(texto, True, (0, 0, 0))  
            janela.blit(texto_renderizado, (620, 360)) 
            pygame.display.update()
            pygame.time.wait(2000)
            viscosidade = tela_viscosidade()
            gravidade = tela_gravidade()
            return personagem_escolhido, viscosidade, gravidade

# Tela viscosidade
def tela_viscosidade():
    janela = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Escolha a viscosidade")
    janela.blit(fundo_viscosidade, (0, 0)) # Troca img de fundo da janela
    desenhar_botao(agua_button, botao_padrao, "ÀGUA", 120, 85)
    desenhar_botao(mel_button, botao_padrao, "MEL", 150, 85)
    desenhar_botao(ar_button, botao_padrao, "AR", 160, 85)
    pygame.display.update()

    while True:
        viscosidade_escolhida = None

        for event in pygame.event.get(): 
            if event.type == MOUSEBUTTONDOWN and event.button == 1: 
                if agua_button.collidepoint(event.pos):
                    viscosidade_escolhida = "àgua" 
                elif mel_button.collidepoint(event.pos):
                    viscosidade_escolhida =  "mel" 
                elif ar_button.collidepoint(event.pos):
                    viscosidade_escolhida =  "ar"
            if event.type == QUIT:
                return
                
        if viscosidade_escolhida is not None:
            texto = f"Você escolheu {viscosidade_escolhida}!"
            janela.blit(balao_aviso, (500, 150))
            texto_renderizado = fonte.render(texto, True, (0, 0, 0))  
            janela.blit(texto_renderizado, (620, 360)) 
            pygame.display.update()
            pygame.time.wait(2000)
            return viscosidade_escolhida

# Tela gravidade
def tela_gravidade():
    janela = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Escolha a gravidade")
    janela.blit(fundo_gravidade, (0, 0)) # Troca img de fundo da janela
    desenhar_botao(lua_button, botao_padrao, "LUA", 150, 85)
    desenhar_botao(terra_button, botao_padrao, "TERRA", 110, 85)
    desenhar_botao(marte_button, botao_padrao, "MARTE", 110, 85)
    pygame.display.update()

    while True:
        gravidade_escolhida = None

        for event in pygame.event.get(): 
            if event.type == MOUSEBUTTONDOWN and event.button == 1: 
                if lua_button.collidepoint(event.pos):
                    gravidade_escolhida = "Lua" 
                elif terra_button.collidepoint(event.pos):
                    gravidade_escolhida =  "Terra" 
                elif marte_button.collidepoint(event.pos):
                    gravidade_escolhida =  "Marte"
            if event.type == QUIT:
                return
                
        if gravidade_escolhida is not None:
            texto = f"Você escolheu {gravidade_escolhida}!"
            janela.blit(balao_aviso, (500, 150))
            texto_renderizado = fonte.render(texto, True, (0, 0, 0))  
            janela.blit(texto_renderizado, (620, 360)) 
            pygame.display.update()
            pygame.time.wait(2000)
            return gravidade_escolhida

# Tela do jogo
def tela_jogo(personagem, viscosidade, gravidade):
    print(f"Selecionados: Personagem: {personagem}, Viscosidade: {viscosidade}, Gravidade: {gravidade}.")

    janela = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Jogo")

    # Tela (ambiente de jogo) de acordo com a gravidade selecionada
    if gravidade == "Lua":
        janela.blit(ambiente_lua, (0, 0)) # Troca img de fundo da janela
    elif gravidade == "Terra":
        janela.blit(ambiente_terra, (0, 0)) 
    else:
        janela.blit(ambiente_marte, (0, 0)) 

    pygame.display.update() # Atualiza as novas alterações na tela
    pygame.time.wait(4000) # Só para teste

    # for event in pygame.event.get(): 
    #     if event.type == QUIT:
    #         return
        # Lógica do jogo

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
            personagem, viscosidade, gravidade = tela_personagens()

            H = 50
            m = None
            g = None
            b = None

            if personagem == "rato":
                m = 0.2
            elif personagem == "gato":
                m = 4
            else:
                m = 100

            if viscosidade == "ar":
                b = 0.02
            elif viscosidade == "àgua":
                b = 1
            else:
                b = 24

            if gravidade == "Lua":
                g = 1.62
            elif gravidade == "Marte":
                g = 3.7
            else:
                g = 9.8

            plotar_grafico(g, b, m, H)

            if personagem == "sair":
                running = False
                break

            evento_jogo = tela_jogo(personagem, viscosidade, gravidade) 
            if evento_jogo == "sair": # Também fecha janela
                running = False
                break

    pygame.quit()

if __name__ == '__main__':
    game_loop()