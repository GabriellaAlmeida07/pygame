import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from matplotlib.animation import FuncAnimation


def tempo_queda(g, b, m, H):
    '''
        Calcula o tempo de queda de um corpo em queda livre com velocidade inicial nula.

        g - gravidade (m/s^2);
        b - viscosidade (mPa);
        m - massa (m);
        H - altura inicial (m).

        São retornados 100 valores de tempo em segundos (s) entre 0 e o tempo de queda para realizar a animação.
    '''

    # Com viscosidade nula, o cálculo é simplificado.
    if b == 0:
        tempo = np.sqrt(2 * H / g)
        return np.linspace(0, tempo, 100)
    
    # Com viscosidade não nula, calculamos a raiz da equação da posição.
    else:
        def r(t):
            T = m/b
            return H - g*t*T + (g*(T**2)*(1 - (1/np.exp(t/T))))

        tempo = fsolve(r, 1, xtol=1e-6, maxfev=5000)
        return np.linspace(0, tempo[0], 100)
    
def posicao(g, b, m, H, t):
    '''
        Calcula a trajetória do corpo em queda livre com velocidade inicial nula.
        Realiza o cálculo baseado nos valores de tempo fornecidos.

        g - gravidade (m/s^2);
        b - viscosidade (mPa);
        m - massa (m);
        H - altura inicial (m);
        t - tempo (s).

        Retorna 100 valores da posição em metros (m) dentro do intervalo de tempo fornecido para realizar a animação.
    '''

    # Cálculo com e sem viscosidade.
    if b == 0:
        y = H - (g * t**2 / 2)
    else:
        T = m/b
        y = H - g*t*T + (g*(T**2)*(1 - (1/np.exp(t/T))))

    return y

def velocidade(g, b, m, H, t):
    '''
        Calcula a velocidade do corpo em queda livre com velocidade inicial nula.
        Realiza o cálculo baseado nos valores de tempo fornecidos.

        g - gravidade (m/s^2);
        b - viscosidade (mPa);
        m - massa (m);
        H - altura inicial (m);
        t - tempo (s).

        Retorna 100 valores da velocidade em metros por segundo (m/s) dentro do intervalo de tempo fornecido para realizar a animação.
    '''

    # Cálculo com e sem viscosidade.
    if b == 0:
        y = g * t
    else:
        T = m/b
        y = g * T * (1 - (1/np.exp(t / T)))

    return y

# Define os parâmetros variáveis da queda livre.
print("Selecione a gravidade(m/s^2):")
g = float(input())

print("Selecione a viscosidade(mPa):")
b = float(input())

print("Selecione a massa(Kg):")
m = float(input())

print("Selecione a altura(m):")
H = float(input())

# Define os eixos do gráfico
t = tempo_queda(g, b, m, H)
r = posicao(g, b, m, H, t)
v = velocidade(g, b, m, H, t)

# Cria a figura com uma linha vazia a ser atualizada na animação
fig, (eixo1, eixo2) = plt.subplots(1, 2, figsize=(10, 5))
line1, = eixo1.plot([], [], label='Posição', color='blue')
line2, = eixo2.plot([], [], label='Velocidade', color='red')

# Define os limites dos plots
eixo1.set_xlim(0, max(t))
eixo1.set_ylim(min(r)*1.1, max(r) * 1.1)
eixo1.set_title("Posição")
eixo1.set_xlabel("t (s)")
eixo1.set_ylabel("r (m)")
eixo1.grid(True)
eixo1.legend()

eixo2.set_xlim(0, max(t))
eixo2.set_ylim(min(v) * 1.1, max(v) * 1.1)
eixo2.set_title("Velocidade")
eixo2.set_xlabel("t (s)")
eixo2.set_ylabel("v (m/s)")
eixo2.grid(True)
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
plt.show()