import pygame
from pygame.locals import *
import numpy as np
import time
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from matplotlib.animation import FuncAnimation
from scipy.optimize import fsolve
import numpy as np

def tempo_queda(g, b, m, H):
    """
    Calcula o tempo de queda de um objeto a partir de uma altura H,
    considerando a gravidade e a viscosidade do ambiente.

    Parâmetros:
        g (float): Aceleração da gravidade (m/s²).
        b (float): Coeficiente de viscosidade.
        m (float): Massa do objeto (kg).
        H (float): Altura inicial do objeto (m).

    Retorna:
        float: Tempo necessário para o objeto atingir o solo (s).
    """
    if b == 0:
        # Queda sem resistência do ar
        def r(t):
            return H - (g * t**2 / 2)
        tempo = fsolve(r, 0)
        return tempo[0]
    else:
        # Queda com resistência do ar
        def r(t):
            T = m / b
            return H - g * t * T + (g * (T**2) * (1 - np.exp(-t / T)))
        tempo = fsolve(r, 1)
        return tempo[0]

def posicao(g, b, m, H, t):
    """
    Calcula a posição de um objeto em queda livre a partir de uma altura H
    no instante de tempo t, considerando a gravidade e a viscosidade do ambiente.

    Parâmetros:
        g (float): Aceleração da gravidade (m/s²).
        b (float): Coeficiente de viscosidade.
        m (float): Massa do objeto (kg).
        H (float): Altura inicial do objeto (m).
        t (float): Tempo decorrido desde o início da queda (s).

    Retorna:
        float: Posição do objeto em relação ao solo (m).
    """
    if b == 0:
        # Posição sem resistência do ar
        y = H - (g * t**2 / 2)
    else:
        # Posição com resistência do ar
        T = m / b
        y = H - g * t * T + (g * (T**2) * (1 - np.exp(-t / T)))
    return y

def velocidade(g, b, m, t):
    """
    Calcula a velocidade de um objeto em queda livre no instante de tempo t,
    considerando a gravidade e a viscosidade do ambiente.

    Parâmetros:
        g (float): Aceleração da gravidade (m/s²).
        b (float): Coeficiente de viscosidade.
        m (float): Massa do objeto (kg).
        t (float): Tempo decorrido desde o início da queda (s).

    Retorna:
        float: Velocidade do objeto em relação ao solo (m/s).
    """
    if b == 0:
        # Velocidade sem resistência do ar
        y = -g * t
    else:
        # Velocidade com resistência do ar
        T = m / b
        y = g * T * (1 - np.exp(-t / T))
    return y


# Função para a tela de adivinhar o tempo de queda
def tela_adivinhar_tempo(tempo_real):
    # Configura a janela do pygame
    janela = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Adivinhe o tempo de queda")
    janela.blit(fundo_adivinhe, (0, 0))
    
    # Fontes
    fonte_input = pygame.font.Font(None, int(80 * ESCALA))  # Fonte para input
    
    # Caixa de entrada
    input_box = pygame.Rect(WIDTH // 2 - 150 * ESCALA, HEIGHT // 2 - 50 * ESCALA, 300 * ESCALA, 100 * ESCALA)
    cor_inativa = (0, 0, 0)  # Preto para borda da caixa inativa
    cor_ativa = (128, 128, 128)  # Cinza para borda da caixa ativa
    
    # Variáveis para controle do estado e entrada do usuário
    ativa = False  # Indica se a caixa de entrada está ativa
    texto = ""  # Armazena o texto digitado pelo usuário
    chute = None  # Armazena o valor numérico digitado pelo usuário
    
    # Loop principal da tela
    while True:
        # Processa eventos do pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # Encerra o jogo se o usuário fechar a janela
            
            # Ativa ou desativa a caixa de entrada dependendo de onde o usuário clicou
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    ativa = True
                else:
                    ativa = False
            
            if event.type == pygame.KEYDOWN:
                if ativa: # Se a caixa de entrada estiver ativa
                    if event.key == pygame.K_RETURN:
                        # Tenta converter o texto digitado em um número float
                        try:
                            chute = float(texto)
                        except ValueError:
                            chute = 0.0 # Caso o valor não seja válido, define como 0.0
                        texto = ""
                        time.sleep(1.5) # Pausa de 1.5 segundos 
                        return chute # Retorna o número inserido pelo usuário

                    # Remove o último caractere do texto se o usuário clicar na tecla BACKSPACE  
                    elif event.key == pygame.K_BACKSPACE:
                        texto = texto[:-1]
                    else:
                        # Adiciona o caractere digitado ao texto
                        texto += event.unicode
        
        # Desenha a interface gráfica
        cor_caixa = cor_ativa if ativa else cor_inativa  # Escolhe a cor da borda com base no estado da caixa
        pygame.draw.rect(janela, cor_caixa, input_box, 2)  # Desenha a borda da caixa de entrada
        
        # Renderiza o texto digitado pelo usuário
        texto_renderizado = fonte_input.render(texto, True, (0, 0, 0))  # Texto em preto
        janela.blit(texto_renderizado, (input_box.x + 10, input_box.y + 10))  # Exibe o texto na caixa de entrada

        # Atualiza a tela com as mudanças
        pygame.display.flip()


def simulacao_queda(g, b, m, H, tmax, chute):

    """
    Realiza uma simulação gráfica interativa de queda livre.

    Esta função utiliza a biblioteca Pygame para animar a queda de um objeto sob influência da gravidade 
    e da viscosidade do ambiente, além de comparar o tempo simulado com o tempo estimado pelo usuário.

    Parâmetros:
    - g (float): Aceleração da gravidade no local (m/s²).
    - b (float): Coeficiente de viscosidade.
    - m (float): Massa do objeto (kg).
    - H (float): Altura inicial de queda (m).
    - tmax (float): Tempo máximo da simulação (s).
    - chute (float): Tempo estimado pelo usuário para a queda do objeto.

    Retorno:
    - Nenhum valor é retornado, mas a função exibe uma janela interativa com a simulação e 
      informa ao usuário se sua estimativa de tempo foi correta.
    """

    # Define os parâmetros da queda livre
    t = np.linspace(0, tmax, 100)
    r = posicao(g, b, m, H, t)
    v = velocidade(g, b, m, t)

    """
    Simulação gráfica das variações de posição e velocidade pelo tempo

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
    plt.show()"""
    
    # Inicialização do Pygame
    pygame.init()

    # Configuração da janela
    WIDTH, HEIGHT = int(1850 * ESCALA), int(960 * ESCALA)
    janela = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simulação de Queda Livre")

    # Cores
    WHITE = (255, 255, 255)

    # Configurações da simulação
    tempo = t # Vetor de tempos
    posicoes = posicao(g, b, m, H, tempo) # Calcula posições
    velocidades = velocidade(g, b, m, tempo) # Calcula velocidades

    # Normalização para escalas da simulação
    max_pos = max(posicoes)
    escala_y = HEIGHT / max_pos  # Escala vertical baseada na altura máxima
    escala_t = WIDTH / len(tempo) # Escala horizontal baseada no número de pontos de tempo

    # Configuração do objeto em queda
    raio_objeto = 50
    posicao_atual = H

    # Configuração da fonte
    fonte_tempo = pygame.font.Font(None, int(70 * ESCALA))  # Fonte com tamanho 36

    # Inicialização de variáveis
    tempo_decorrido = 0  # Em segundos
    velocidade_atual = 0  # Inicializa a velocidade
    index_tempo = 0

    # Imagem do objeto(variável com base na massa)
    if m==30:
        objeto_img = pygame.image.load("imgs/personagens/porco.png")
        objeto_img = pygame.transform.scale(objeto_img, (100, 100))
    elif m==4:
        objeto_img = pygame.image.load("imgs/personagens/gato.png")
        objeto_img = pygame.transform.scale(objeto_img, (100, 100))
    else:
        objeto_img = pygame.image.load("imgs/personagens/vaca.png")
        objeto_img = pygame.transform.scale(objeto_img, (100, 100))

    # Plano de fundo(variável com base na gravidade)
    if g==1.62:
        fundo_img = pygame.image.load("imgs/ambientes/lua.jpeg")
        fundo_img = pygame.transform.scale(fundo_img, (WIDTH, HEIGHT)) 
    elif g==3.7:
        fundo_img = pygame.image.load("imgs/ambientes/marte.jpeg")
        fundo_img = pygame.transform.scale(fundo_img, (WIDTH, HEIGHT)) 
    else:
        fundo_img = pygame.image.load("imgs/ambientes/terra.png")
        fundo_img = pygame.transform.scale(fundo_img, (WIDTH, HEIGHT)) 
    
    # Loop principal
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Fecha a janela
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

        # Renderiza o plano de fundo e o objeto
        janela.blit(fundo_img, (0, 0))
        y_objeto = HEIGHT - posicao_atual * escala_y
        janela.blit(objeto_img, (WIDTH // 2 - raio_objeto, int(y_objeto) - raio_objeto))

        # Renderiza o texto
        texto_tempo = fonte_tempo.render(f"Tempo: {tempo_decorrido:.2f}s", True, WHITE)
        janela.blit(texto_tempo, (10, 10))
        texto_velocidade = fonte_tempo.render(f"Velocidade: {velocidade_atual:.2f} m/s", True, WHITE)
        janela.blit(texto_velocidade, (10, 50))

        # Atualiza a tela e controla FPS
        pygame.display.flip()
        clock.tick(30)  # Limita a 30 quadros por segundo

        # Verifica se o objeto atingiu o solo
        if posicao_atual <= 0:
            running = False
            # Exibe resultado da estimativa do usuário
            if abs(chute - tempo_decorrido) < 1:
                texto_final = fonte_tempo.render(f"Acertou! Tempo total: {tempo_decorrido:.2f}s", True, (0, 255, 0))
            else:
                texto_final = fonte_tempo.render(f"Errou! Tempo total: {tempo_decorrido:.2f}s", True, (255, 0, 0))
            janela.blit(texto_final, (WIDTH // 2 - texto_final.get_width() // 2, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.wait(3000)  # Mostra o texto por 3 segundos

    pygame.quit() #Encerra o pygame

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

# Função para desenhar
def desenhar_botao(rect, img, texto, x, y):
    """
    Desenha o botão na tela

    Parâmetros:
        rect: pygame.Rect do botão.
        img: Imagem que será o botão.
        texto: Texto que se deseja escrever dentro do botão.
        x: Posição no eixo x que o texto estará em relação ao botão.
        y: Posição no eixo y que o texto estará em relação ao botão.

    Retorna:
        Não há retorno na função.
    """
    # Desenha a imagem do botão
    janela.blit(img, (rect.x, rect.y))
    
    # Renderiza o texto com a fonte configurada em branco
    texto_renderizado = fonte.render(texto, True, (255, 255, 255))  

    # Calcula a posição do texto com base no deslocamento (x, y)
    texto_x = rect.x + x
    texto_y = rect.y + y

    # Desenha o texto sobre o botão
    janela.blit(texto_renderizado, (texto_x, texto_y))


# Função para o menu inicial
def tela_inicial():
    """
    Criação da tela inicial.

    Parâmetros:
        Não há parâmetros na função.

    Retorna:
        menu: Se o usuário não interagiu com a tela retorna "menu" para continuar nesta tela.
    """

    # Desenha o fundo da tela e o botão start
    janela.blit(fundo_img, (0, 0))
    desenhar_botao(start_button, botao_start, "", 0, 0) # Chama a função para desenhar o botão de "start"
    pygame.display.update() # Atualiza a tela para refletir as mudanças
    
    # Processa os eventos do usuário
    for event in pygame.event.get():            
        if event.type == QUIT:
            return "sair" # Se o usuário fechar a janela, retorna "sair" para encerrar o jogo
        
        if event.type == MOUSEBUTTONDOWN and event.button == 1: # Se o botão esquerdo do mouse for pressionado
            # Verifica se o clique ocorreu dentro da área do botão "start"
            if start_button.collidepoint(event.pos):
                return "personagens" # Retorna "personagens" para navegar para a tela de seleção de personagens 
    
    return "menu" 

# Tela de seleção do personagem
def tela_personagens():
    """
    Criação da tela para seleção do personagem.

    Parâmetros:
        Não há parâmetros na função.

    Retorna:
        personagem_escolhido: uma string que contém o animal escolhido.
        viscosidade: uma string que contém a viscosidade escolhida.
        gravidade: uma string que contém a gravidade escolhida.

    """

    # Configura a janela do Pygame e exibe o fundo da tela de personagens
    janela = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Escolha seu Personagem")
    janela.blit(fundo_personagens, (0, 0))

    # Desenha os botões para cada personagem (Vaca, Porco, Gato)
    desenhar_botao(vaca_button, botao_padrao, "VACA", 130*ESCALA, 85*ESCALA)
    desenhar_botao(porco_button, botao_padrao, "PORCO", 110*ESCALA, 85*ESCALA)
    desenhar_botao(gato_button, botao_padrao, "GATO", 130*ESCALA, 85*ESCALA)

    pygame.display.update() # Atualiza a tela para refletir as mudanças

    # Loop principal de interação da tela de personagens
    while True:
        personagem_escolhido = None # Inicializa a variável de personagem

        for event in pygame.event.get(): # Verifica os eventos gerados pela interação do usuário
            # Se o usuário clicar no botão esquerdo do mouse
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                # Verifica em qual botão o clique ocorreu e define o personagem escolhido 
                if vaca_button.collidepoint(event.pos):
                    personagem_escolhido = "vaca" 
                elif gato_button.collidepoint(event.pos):
                    personagem_escolhido =  "gato" 
                elif porco_button.collidepoint(event.pos):
                    personagem_escolhido =  "porco"
            # Se o usuário fechar a janela      
            if event.type == QUIT:
                return # Encerra a função e o jogo
        
        # Se um personagem foi escolhido, exibe uma mensagem de confirmação
        if personagem_escolhido is not None:
            texto = f"Você escolheu {personagem_escolhido}!" # Mensagem de confirmação da escolha
            janela.blit(balao_aviso, (500*ESCALA, 150*ESCALA)) # Desenha o balão de aviso
            texto_renderizado = fonte.render(texto, True, (0, 0, 0)) # Desenha o balão de aviso
            janela.blit(texto_renderizado, (620*ESCALA, 360*ESCALA)) # Desenha o texto na tela
            pygame.display.update() # Atualiza a tela
            pygame.time.wait(2000) # Espera 2 segundos para mostrar a mensagem

            # Chama as funções para selecionar viscosidade e gravidade
            viscosidade = tela_viscosidade()
            gravidade = tela_gravidade()

            # Retorna o personagem escolhido, a viscosidade e a gravidade
            return personagem_escolhido, viscosidade, gravidade

# Tela de seleção da viscosidade
def tela_viscosidade():
    """
    Criação da tela para seleção da viscosidade.

    Parâmetros:
        Não há parâmetros na função.

    Retorna:
        viscosidade_escolhida: uma string que contém a viscosidade escolhida.
    """

    # Configura a janela do Pygame e exibe o fundo da tela de viscosidade
    janela = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Escolha a viscosidade") # Define o título da janela
    janela.blit(fundo_viscosidade, (0, 0)) # # Desenha o fundo da tela

    # Desenha os botões para cada viscosidade (Água, Mel, Ar)
    desenhar_botao(agua_button, botao_padrao, "ÁGUA", 120*ESCALA, 85*ESCALA)
    desenhar_botao(mel_button, botao_padrao, "MEL", 150*ESCALA, 85*ESCALA)
    desenhar_botao(ar_button, botao_padrao, "AR", 160*ESCALA, 85*ESCALA)

    pygame.display.update() # Atualiza a tela para refletir as mudanças

    # Loop principal de interação da tela de viscosidade
    while True:
        viscosidade_escolhida = None # Inicializa a variável de viscosidade escolhida como None

        for event in pygame.event.get(): # Verifica os eventos gerados pela interação do usuário
            # Se o usuário clicar no botão esquerdo do mouse
            if event.type == MOUSEBUTTONDOWN and event.button == 1: 
                # Verifica em qual botão o clique ocorreu e define a viscosidade escolhida
                if agua_button.collidepoint(event.pos):
                    viscosidade_escolhida = "água" 
                elif mel_button.collidepoint(event.pos):
                    viscosidade_escolhida =  "mel" 
                elif ar_button.collidepoint(event.pos):
                    viscosidade_escolhida =  "ar"
            # Se o usuário fechar a janela
            if event.type == QUIT:
                return # Encerra a função

        # Se uma viscosidade foi escolhida, exibe uma mensagem de confirmação
        if viscosidade_escolhida is not None:
            texto = f"Você escolheu {viscosidade_escolhida}!" # Mensagem de confirmação da escolha
            janela.blit(balao_aviso, (500*ESCALA, 150*ESCALA)) # Desenha o balão de aviso
            texto_renderizado = fonte.render(texto, True, (0, 0, 0)) # Renderiza o texto
            janela.blit(texto_renderizado, (620*ESCALA, 360*ESCALA)) # Desenha o texto na tela
            pygame.display.update() # Atualiza a tela
            pygame.time.wait(2000) # Espera 2 segundos para mostrar a mensagem

            # Retorna a viscosidade escolhida
            return viscosidade_escolhida

# Tela gravidade
def tela_gravidade():
    """
    Criação da tela para seleção da gravidade.

    Parâmetros:
        Não há parâmetros na função.

    Retorna:
        gravidade_escolhida: uma string que contém a gravidade escolhida.

    """
    # Configura a janela do Pygame e exibe o fundo da tela de gravidade
    janela = pygame.display.set_mode((WIDTH, HEIGHT)) 
    pygame.display.set_caption("Escolha a gravidade") # Define o título da janela
    janela.blit(fundo_gravidade, (0, 0)) # Desenha o fundo da tela

    # Desenha os botões para cada gravidade (Lua, Terra, Marte)
    desenhar_botao(lua_button, botao_padrao, "LUA", 150*ESCALA, 85*ESCALA)
    desenhar_botao(terra_button, botao_padrao, "TERRA", 110*ESCALA, 85*ESCALA)
    desenhar_botao(marte_button, botao_padrao, "MARTE", 110*ESCALA, 85*ESCALA)

    pygame.display.update() # Atualiza a tela para refletir as mudanças

    # Loop principal de interação da tela de gravidade
    while True:
        gravidade_escolhida = None # Inicializa a variável de gravidade escolhida

         # Verifica os eventos gerados pela interação do usuário
        for event in pygame.event.get(): 
            # Se o usuário clicar no botão esquerdo do mouse
            if event.type == MOUSEBUTTONDOWN and event.button == 1: 
                # Verifica em qual botão o clique ocorreu e define a gravidade escolhida
                if lua_button.collidepoint(event.pos):
                    gravidade_escolhida = "Lua" 
                elif terra_button.collidepoint(event.pos):
                    gravidade_escolhida =  "Terra" 
                elif marte_button.collidepoint(event.pos):
                    gravidade_escolhida =  "Marte"
            # Se o usuário fechar a janela
            if event.type == QUIT:
                return # Encerra a função
        
        # Se uma gravidade foi escolhida, exibe uma mensagem de confirmação
        if gravidade_escolhida is not None:
            texto = f"Você escolheu {gravidade_escolhida}!" # Mensagem de confirmação da escolha
            janela.blit(balao_aviso, (500*ESCALA, 150*ESCALA)) # Desenha o balão de aviso
            texto_renderizado = fonte.render(texto, True, (0, 0, 0))  # Renderiza o texto
            janela.blit(texto_renderizado, (620*ESCALA, 360*ESCALA)) # Desenha o texto na tela
            pygame.display.update() # Atualiza a tela
            pygame.time.wait(2000) # Espera 2 segundos para mostrar a mensagem

            # Retorna a gravidade escolhida
            return gravidade_escolhida

# Função principal
def game_loop():
    """
    Função principal de loop do jogo (transição das janelas e ações).

    Parâmetros:
        Não há parâmetros na função.

    Retorna:
        Não há retorno na função.

    """
    running = True  # Inicia o loop principal do jogo
    personagem = None  # Inicializa a variável para o personagem escolhido
    viscosidade = None  # Inicializa a variável para a viscosidade escolhida
    gravidade = None  # Inicializa a variável para a gravidade escolhida

    # Inicializa variáveis para o tempo e velocidade durante a simulação
    tempo_decorrido = 0  
    velocidade_atual = 0  
    adivinhou_tempo = False  # Controla se a função para adivinhar o tempo já foi chamada

    while running:
        clock.tick(30) # Controla a taxa de atualização do jogo, limitando a 30 quadros por segundo

        # Chama a tela inicial e verifica o evento retornado (se o jogador vai sair ou selecionar o personagem)
        evento = tela_inicial()  

        # Se o jogador escolheu sair
        if evento == "sair":
            running = False # Encerra o loop principal e o jogo 
        
        # Se o jogador escolheu a tela de personagens
        elif evento == "personagens":
            # Chama a tela de personagens e armazena as escolhas feitas
            personagem, viscosidade, gravidade = tela_personagens()

            H = 50  # Altura inicial para a simulação de queda
            m = None  # Massa do personagem
            g = None  # Gravidade do planeta
            b = None  # Coeficiente de viscosidade

            # Define a massa com base no personagem escolhido
            if personagem == "porco":
                m = 30
            elif personagem == "gato":
                m = 4
            else:
                m = 100

            # Define o coeficiente de viscosidade com base na escolha do jogador
            if viscosidade == "ar":
                b = 0.02
            elif viscosidade == "água":
                b = 1
            else:
                b = 24

            # Define a gravidade com base no planeta escolhido
            if gravidade == "Lua":
                g = 1.62
            elif gravidade == "Marte":
                g = 3.7
            else:
                g = 9.8

            # Calcula o tempo máximo de queda com os parâmetros escolhidos
            tmax = tempo_queda(g, b, m, H)
            
            # Chama a função de adivinhar o tempo de queda, caso ainda não tenha sido chamada
            if not adivinhou_tempo:
                chute = tela_adivinhar_tempo(tmax)  # Chama a tela onde o jogador tenta adivinhar o tempo de queda
                adivinhou_tempo = True  # Marca que o tempo já foi adivinhado, evitando chamadas repetidas

            print(chute) # Exibe o chute do jogador (tempo adivinhado)

            # Inicia a simulação da queda com os parâmetros definidos e o chute do jogador
            simulacao_queda(g, b, m, H, tmax, chute)

    pygame.quit() # Encerra o Pygame quando o loop termina

if __name__ == '__main__':
    game_loop() # Chama a função principal
