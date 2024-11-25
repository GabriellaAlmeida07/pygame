import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from matplotlib.animation import FuncAnimation


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
        tempo = fsolve(r, 1)
        
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

g = 9.8
b = 1
m = 500.0
H = 50.0

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