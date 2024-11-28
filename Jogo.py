import pygame
from pygame.locals import *
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from matplotlib.animation import FuncAnimation

def tempo_queda(g, b, m, H):
    if b == 0:
        def r(t):
            return H - (g * t**2 / 2)
        tempo = fsolve(r, 0)
        return tempo[0]
    else:
        def r(t):
            T = m/b
            return H - g*t*T + (g*(T**2)*(1 - np.exp(-t/T)))
        tempo = fsolve(r, 1)
        
        return tempo[0]


def posicao(g, b, m, H, t):
    if b == 0:
        y = H - (g * t**2 / 2)
    else:
        T = m / b
        y = H - g * t * T + (g * (T**2) * (1 - np.exp(-t/T)))
    return y

def velocidade(g, b, m, H, t):
    if b == 0:
        y = -g * t
    else:
        T = m / b
        y = g * T * (1 - np.exp(-t / T))
    return y

import pygame
import time

def tela_adivinhar_tempo(tempo_real):
    janela = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Adivinhe o tempo de queda")
    janela.blit(fundo_adivinhe, (0, 0))
    
    # Fontes
    fonte_input = pygame.font.Font(None, int(80 * ESCALA))  # Fonte para input
    fonte_instrucao = pygame.font.Font(None, int(50 * ESCALA))  # Fonte para instrução
    fonte_resultado = pygame.font.Font(None, int(60 * ESCALA))  # Fonte para resultado
    
    # Caixa de entrada
    input_box = pygame.Rect(WIDTH // 2 - 150 * ESCALA, HEIGHT // 2 - 50 * ESCALA, 300 * ESCALA, 100 * ESCALA)
    cor_inativa = (0, 0, 0)  # Preto para borda da caixa inativa
    cor_ativa = (0, 0, 0)  # Preto para borda da caixa ativa
    
    ativa = False
    texto = ""
    resultado = None
    chute = None
    
    while True:
        # janela.fill((255, 255, 255))  # Fundo branco
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # Retorna para encerrar o jogo
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    ativa = True
                else:
                    ativa = False
            
            if event.type == pygame.KEYDOWN:
                if ativa:
                    if event.key == pygame.K_RETURN:
                        try:
                            chute = float(texto)
                            if abs(chute - tempo_real) < 1:  # Tolerância de 1 segundo
                                resultado = "Parabéns! Você acertou!"
                            else:
                                resultado = f"Errado! O tempo real é {tempo_real:.2f} segundos."
                        except ValueError:
                            resultado = "Por favor, insira um número válido."
                        texto = ""
                        
                        time.sleep(2.5)
                        
                        return chute
                        # pygame.quit()  # Fecha a janela do Pygame
                        # sys.exit()  # Encerra o programa
                        
                    elif event.key == pygame.K_BACKSPACE:
                        texto = texto[:-1]
                    else:
                        texto += event.unicode
        
        # Renderiza a interface
        cor_caixa = cor_ativa if ativa else cor_inativa
        pygame.draw.rect(janela, cor_caixa, input_box, 2)  # Bordas da caixa de entrada
        
        # Texto da entrada
        texto_renderizado = fonte_input.render(texto, True, (0, 0, 0))  # Texto em preto
        janela.blit(texto_renderizado, (input_box.x + 10, input_box.y + 10))
        
        # Mensagem de instrução
        # instrucao = fonte_instrucao.render("Adivinhe o tempo de queda (segundos):", True, (0, 0, 0))  # Texto em preto
        # janela.blit(instrucao, (WIDTH // 2 - instrucao.get_width() // 2, HEIGHT // 2 - 150 * ESCALA))

        pygame.display.flip()

    
    return chute
    pygame.quit()  # Fecha a janela do Pygame
    sys.exit()  # Encerra o programa


def renderizar_resultado(janela, fonte, resultado):
    """Função para exibir o resultado no centro da janela."""
    janela.fill((255, 255, 255))  # Fundo branco
    texto = fonte.render(resultado, True, (0, 0, 0))  # Texto em preto
    janela.blit(texto, (WIDTH // 2 - texto.get_width() // 2, HEIGHT // 2 - texto.get_height() // 2))



def simulacao_queda(g, b, m, H, tmax, chute):

    # Define os eixos do gráfico
    t = np.linspace(0, tmax, 100)
    r = posicao(g, b, m, H, t)
    v = velocidade(g, b, m, H, t)
    """
    # Cria a figura em um único eixo, com uma linha vazia a ser atualizada na animação
    fig, (eixo1, eixo2) = plt.subplots(1, 2, figsize=(10, 5))
    line1, = eixo1.plot([], [], label='Posição', color='blue')
    line2, = eixo2.plot([], [], label='Velocidade', color='red')

    # Define os limites do plot
    eixo1.set_xlim(0, max(t))
    eixo1.set_ylim(0, max(r) * 1.1)
   # eixo1.set_ylim(min(r)*1.1, max(r) * 1.1)
    eixo1.set_title("Posição")
    eixo1.set_xlabel("t (s)")
    eixo1.set_ylabel("r (m)")
    eixo1.legend()

    eixo2.set_xlim(0, max(t))
    eixo2.set_ylim(0, max(v) * 1.1)
   # eixo2.set_ylim(min(v) * 1.1, max(v) * 1.1)
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

    #chute = tela_adivinhar_tempo(tmax)"""
    
    # Inicialização do Pygame
    pygame.init()

    # Configuração da janela
    WIDTH, HEIGHT = int(1850 * ESCALA), int(960 * ESCALA)
    janela = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simulação de Queda Livre")

    # Cores
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    BLACK = (0, 0, 0)

    # Configurações da simulação no pygame
    tempo = t
    posicoes = posicao(g, b, m, H, tempo)
    velocidades = velocidade(g, b, m, H, tempo)

    # Normalização para escalas da simulação
    max_pos = max(posicoes)
    min_vel = 0
    #min_vel = min(velocidades)
    max_vel = max(velocidades)

    escala_y = HEIGHT // 1 / max_pos
    escala_t = WIDTH / len(tempo)

    # Objeto em queda
    raio_objeto = 50
    posicao_atual = H

    # Loop principal
    running = True
    clock = pygame.time.Clock()
    index_tempo = 0

    # Inicializar fonte
    fonte_tempo = pygame.font.Font(None, int(70 * ESCALA))  # Fonte com tamanho 36

    # Variáveis de texto
    tempo_decorrido = 0  # Em segundos
    velocidade_atual = 0  # Inicializa a velocidade


    # Imagem do objeto
    if m==30:
        objeto_img = pygame.image.load("imgs/personagens/porco.png")
        objeto_img = pygame.transform.scale(objeto_img, (100, 100))# Ajuste para o tamanho desejado
    elif m==4:
        objeto_img = pygame.image.load("imgs/personagens/gato.png")
        objeto_img = pygame.transform.scale(objeto_img, (100, 100))
    else:
        objeto_img = pygame.image.load("imgs/personagens/vaca.png")
        objeto_img = pygame.transform.scale(objeto_img, (100, 100))

    # Plano de fundo
    if g==1.62:
        fundo_img = pygame.image.load("imgs/ambientes/lua.jpeg")
        fundo_img = pygame.transform.scale(fundo_img, (WIDTH, HEIGHT))  # Redimensionar para o tamanho da janela
    elif g==3.7:
        fundo_img = pygame.image.load("imgs/ambientes/marte.jpeg")
        fundo_img = pygame.transform.scale(fundo_img, (WIDTH, HEIGHT))  # Redimensionar para o tamanho da janela
    else:
        fundo_img = pygame.image.load("imgs/ambientes/terra.png")
        fundo_img = pygame.transform.scale(fundo_img, (WIDTH, HEIGHT))  # Redimensionar para o tamanho da janela
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Atualiza o cronômetro
        if posicao_atual > 0:
            tempo_decorrido += clock.get_time() / 1000  # Convertendo milissegundos para segundos

        # Calcula o índice com base no tempo decorrido
        index_tempo = int(tempo_decorrido / (tmax / len(tempo)))

        # Atualiza a posição e velocidade do objeto
        if index_tempo < len(tempo):
            posicao_atual = posicoes[index_tempo]
            velocidade_atual = velocidades[index_tempo]
        else:
            posicao_atual = 0
            velocidade_atual = 0

        # Adiciona o plano de fundo
        janela.blit(fundo_img, (0, 0))

        # Renderiza o texto do cronômetro
        texto_tempo = fonte_tempo.render(f"Tempo: {tempo_decorrido:.2f}s", True, WHITE)
        janela.blit(texto_tempo, (10, 10))

        # Renderiza o texto da velocidade
        texto_velocidade = fonte_tempo.render(f"Velocidade: {velocidade_atual:.2f} m/s", True, WHITE)
        janela.blit(texto_velocidade, (10, 50))

        # Desenha o objeto em queda
        y_objeto = HEIGHT - posicao_atual * escala_y
        janela.blit(objeto_img, (WIDTH // 2 - raio_objeto, int(y_objeto) - raio_objeto))

        # Atualiza a tela
        pygame.display.flip()
        clock.tick(30)  # Limita a 30 quadros por segundo

        # Verifica se o objeto atingiu o solo
        if posicao_atual <= 0:
            running = False
            # Exibe o tempo de queda real

            if abs(chute - tempo_decorrido) < 1:
                texto_final = fonte_tempo.render(f"Acertou! Tempo total: {tempo_decorrido:.2f}s", True, (0, 255, 0))
                janela.blit(texto_final, (WIDTH // 2 - texto_final.get_width() // 2, HEIGHT // 2))
                pygame.display.flip()
                pygame.time.wait(3000)  # Mostra o texto por 3 segundos
            else:
                texto_final = fonte_tempo.render(f"Errou! Tempo total: {tempo_decorrido:.2f}s", True, (255, 0, 0))
                janela.blit(texto_final, (WIDTH // 2 - texto_final.get_width() // 2, HEIGHT // 2))
                pygame.display.flip()
                pygame.time.wait(3000)  # Mostra o texto por 3 segundos
        
    if not tela_adivinhar_tempo(tmax):
        pygame.quit()
        return
        

    pygame.quit()
    return


# Inicialização do Pygame
pygame.init()

# Fator de escala
ESCALA = 0.5

# Largura e altura da tela ajustadas
WIDTH, HEIGHT = int(1850 * ESCALA), int(960 * ESCALA)

# Configuração das imagens dos personagens
vaca_img = pygame.image.load("imgs/personagens/vaca.png")
vaca_img = pygame.transform.scale(vaca_img, (int(300 * ESCALA), int(200 * ESCALA)))

gato_img = pygame.image.load("imgs/personagens/gato.png")
gato_img = pygame.transform.scale(gato_img, (int(300 * ESCALA), int(200 * ESCALA)))

porco_img = pygame.image.load("imgs/personagens/porco.png")
porco_img = pygame.transform.scale(porco_img, (int(300 * ESCALA), int(200 * ESCALA)))

# Configuração das imagens de fundo e dos ambientes de jogo
fundo_img = pygame.image.load("imgs/fundos/start.png")
fundo_img = pygame.transform.scale(fundo_img, (WIDTH, HEIGHT))

fundo_personagens = pygame.image.load("imgs/fundos/personagens.png")
fundo_personagens = pygame.transform.scale(fundo_personagens, (WIDTH, HEIGHT))

fundo_gravidade = pygame.image.load("imgs/fundos/gravidade.png")
fundo_gravidade = pygame.transform.scale(fundo_gravidade, (WIDTH, HEIGHT))

fundo_viscosidade = pygame.image.load("imgs/fundos/viscosidade.png")
fundo_viscosidade = pygame.transform.scale(fundo_viscosidade, (WIDTH, HEIGHT))

fundo_adivinhe = pygame.image.load("imgs/fundos/adivinhe.png")
fundo_adivinhe = pygame.transform.scale(fundo_adivinhe, (WIDTH, HEIGHT))

ambiente_lua = pygame.image.load("imgs/ambientes/lua.jpeg")
ambiente_lua = pygame.transform.scale(ambiente_lua, (WIDTH, HEIGHT))

ambiente_terra = pygame.image.load("imgs/ambientes/terra.png")
ambiente_terra = pygame.transform.scale(ambiente_terra, (WIDTH, HEIGHT))

ambiente_marte = pygame.image.load("imgs/ambientes/marte.jpeg")
ambiente_marte = pygame.transform.scale(ambiente_marte, (WIDTH, HEIGHT))

# Configuração dos botões e adicionais
botao_start = pygame.image.load("imgs/botoes/botao_start.png")
botao_start = pygame.transform.scale(botao_start, (int(400 * ESCALA), int(200 * ESCALA)))

botao_padrao = pygame.image.load("imgs/botoes/personag_botao.png")
botao_padrao = pygame.transform.scale(botao_padrao, (int(400 * ESCALA), int(200 * ESCALA)))

balao_aviso = pygame.image.load("imgs/botoes/balao.png")
balao_aviso = pygame.transform.scale(balao_aviso, (int(700 * ESCALA), int(500 * ESCALA)))

# Configuração da janela inicial
janela = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo")
clock = pygame.time.Clock()

# Rect dos botões ajustados
start_button = pygame.Rect(int(750 * ESCALA), int(610 * ESCALA), int(400 * ESCALA), int(200 * ESCALA))
gato_button = pygame.Rect(int(150 * ESCALA), int(700 * ESCALA), int(300 * ESCALA), int(200 * ESCALA))
vaca_button = pygame.Rect(int(730 * ESCALA), int(700 * ESCALA), int(300 * ESCALA), int(200 * ESCALA))
porco_button = pygame.Rect(int(1270 * ESCALA), int(700 * ESCALA), int(300 * ESCALA), int(200 * ESCALA))
agua_button = pygame.Rect(int(150 * ESCALA), int(750 * ESCALA), int(300 * ESCALA), int(200 * ESCALA))
mel_button = pygame.Rect(int(730 * ESCALA), int(750 * ESCALA), int(300 * ESCALA), int(200 * ESCALA))
ar_button = pygame.Rect(int(1270 * ESCALA), int(750 * ESCALA), int(300 * ESCALA), int(200 * ESCALA))
lua_button = pygame.Rect(int(170 * ESCALA), int(750 * ESCALA), int(300 * ESCALA), int(200 * ESCALA))
terra_button = pygame.Rect(int(740 * ESCALA), int(750 * ESCALA), int(300 * ESCALA), int(200 * ESCALA))
marte_button = pygame.Rect(int(1280 * ESCALA), int(750 * ESCALA), int(300 * ESCALA), int(200 * ESCALA))

# Fonte ajustada
fonte = pygame.font.Font(None, int(70 * ESCALA))

# Função para desenhar botão (rect do botão, imagem, texto, x e y do texto)
def desenhar_botao(rect, img, texto, x, y):
    #x*=ESCALA
    #y*=ESCALA
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
    desenhar_botao(vaca_button, botao_padrao, "VACA", 130*ESCALA, 85*ESCALA)
    desenhar_botao(porco_button, botao_padrao, "PORCO", 110*ESCALA, 85*ESCALA)
    desenhar_botao(gato_button, botao_padrao, "GATO", 130*ESCALA, 85*ESCALA)
    pygame.display.update()

    while True:
        personagem_escolhido = None

        for event in pygame.event.get(): 
            if event.type == MOUSEBUTTONDOWN and event.button == 1: 
                if vaca_button.collidepoint(event.pos):
                    personagem_escolhido = "vaca" 
                elif gato_button.collidepoint(event.pos):
                    personagem_escolhido =  "gato" 
                elif porco_button.collidepoint(event.pos):
                    personagem_escolhido =  "porco"
            if event.type == QUIT:
                return 
                
        if personagem_escolhido is not None:
            texto = f"Você escolheu {personagem_escolhido}!"
            janela.blit(balao_aviso, (500*ESCALA, 150*ESCALA))
            texto_renderizado = fonte.render(texto, True, (0, 0, 0))  
            janela.blit(texto_renderizado, (620*ESCALA, 360*ESCALA)) 
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
    desenhar_botao(agua_button, botao_padrao, "ÀGUA", 120*ESCALA, 85*ESCALA)
    desenhar_botao(mel_button, botao_padrao, "MEL", 150*ESCALA, 85*ESCALA)
    desenhar_botao(ar_button, botao_padrao, "AR", 160*ESCALA, 85*ESCALA)
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
            janela.blit(balao_aviso, (500*ESCALA, 150*ESCALA))
            texto_renderizado = fonte.render(texto, True, (0, 0, 0))  
            janela.blit(texto_renderizado, (620*ESCALA, 360*ESCALA)) 
            pygame.display.update()
            pygame.time.wait(2000)
            return viscosidade_escolhida

# Tela gravidade
def tela_gravidade():
    janela = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Escolha a gravidade")
    janela.blit(fundo_gravidade, (0, 0)) # Troca img de fundo da janela
    desenhar_botao(lua_button, botao_padrao, "LUA", 150*ESCALA, 85*ESCALA)
    desenhar_botao(terra_button, botao_padrao, "TERRA", 110*ESCALA, 85*ESCALA)
    desenhar_botao(marte_button, botao_padrao, "MARTE", 110*ESCALA, 85*ESCALA)
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
            janela.blit(balao_aviso, (500*ESCALA, 150*ESCALA))
            texto_renderizado = fonte.render(texto, True, (0, 0, 0))  
            janela.blit(texto_renderizado, (620*ESCALA, 360*ESCALA)) 
            pygame.display.update()
            pygame.time.wait(2000)
            return gravidade_escolhida


# Função principal
def game_loop():
    running = True  # Loop infinito para o jogo
    personagem = None # Será string exemplo: "porco"
    viscosidade = None # Será string exemplo: "mel"
    gravidade = None # Será string exemplo: "lua"

    # Variáveis de texto
    tempo_decorrido = 0  # Em segundos
    velocidade_atual = 0  # Inicializa a velocidade
    cont =0

    while running:
        clock.tick(30)

        evento = tela_inicial()  

        if evento == "sair":
            running = False   
        
        elif evento == "personagens":
            personagem, viscosidade, gravidade = tela_personagens()

            H = 50
            m = None
            g = None
            b = None

            if personagem == "porco":
                m = 30
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

            tmax = tempo_queda(g, b, m, H)
            
            if cont==0:
                chute = tela_adivinhar_tempo(tmax)
                cont=1

            print(chute)

            simulacao_queda(g, b, m, H, tmax, chute)


    pygame.quit()

if __name__ == '__main__':
    game_loop()
