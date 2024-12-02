# Queda Livre

## Descrição do projeto
Esse projeto é um jogo, criado para representar fenômenos específicos da física. Ele busca demonstrar os conceitos de queda livre, gravidade e viscosidade de uma forma interativa e divertida. O jogo consiste em selecionar um personagem, os quais possuem massas distintas, uma viscosidade e um ambiente que representa diferentes gravidades. Ao seleciona-los, é solicitado que o jogador tente adivinhar o tempo de queda nas condições escolhidas. Por fim, há uma animação que demonstra a queda e revela qual foi o verdadeiro tempo de queda atingido.


### **Escolha do personagem, viscosidade e gravidade do ambiente. E a tela para adivinhar o tempo de queda:**

<p float="left">
  <img src="https://github.com/user-attachments/assets/8761249a-282a-451e-9478-6955c89e2f7d" width="40%" />
  <img src="https://github.com/user-attachments/assets/dddac601-86cd-4a97-8728-7dca09350abe" width="40%" />
  <img src="https://github.com/user-attachments/assets/bde36ba0-397a-4ba2-8c9f-59947d964bbb" width="40%" />
  <img src="https://github.com/user-attachments/assets/87b9b736-ec59-4d9c-b452-37352171c501" width="40%" />
</p>


### **Animação do personagem em queda livre no ambiente e viscosidade selecionada:** 

<p float="left">
<img src="https://github.com/user-attachments/assets/25843ae6-637f-4c52-a27a-3f75e99f2828" width="80%" />
</p>


## Conceitos de Física e Modelo 

### Queda Livre

A queda livre ocorre quando um objeto é solto de uma determinada altura $H$, a massa fica sujeita exclusivamente à força gravitacional $\vec{F}_g$. Neste cenário, nenhuma outra força, como a resistência do ar, interfere no movimento de queda livre, o que torna a gravidade a única responsável pela aceleração do objeto, neste movimento a gravidade ($g$) permanece constante. Na Terra a gavidade tem um valor aproximado de $9,8 \ \text{m/s}^2$, em outros ambientes (corpos celestes), como a Lua ou Marte, a gravidade é significativamente menor.
Características principais da queda livre:

* A velocidade do objeto aumenta gradualmente durante o movimento em direção ao solo.
* A trajetória é influenciada somente pela gravidade, o que torna o movimento previsível e calculável (objetivo do nosso jogo).

Este gráfico (Figura 1), ilustra o movimento de um objeto em queda livre, tem as seguintes componentes: 

- Eixo vertical (z): Representa a altura ou posição do objeto em **função do tempo**, ao longo da direção vertical.
- Ponto $O$: Marca a origem da queda, no nível do solo.
- Vetores:
  - $\vec{F}_g$ (vetor de força gravitacional): Tem direção para baixo, representando a aceleração devido à gravidade.
  - $\hat{k}$ (vetor unitário, versor): Indica a direção positiva do eixo vertical (para cima).
- Trajetória do objeto $(\vec{r}(t))$: Representa a posição do objeto ao longo do tempo, mostra a mudança de altura durante a queda.
- Altura $H$: A altura inicial a partir da qual o objeto é solto.
- Velocidade inicial $\vec{v(t_i)} = 0$: A velocidade inicial do objeto é zero.
- Tempos:
  - ($\vec{t_i})$: O instante inicial, quando o objeto é solto (tempo $t = 0$)
  - ($\vec{t_q})$: O instante de impacto com o solo.
  - ($\vec{t})$: Tempo variável durante a queda.
    
No gráfico vemos o movimento do objeto e das forças que atuam sobre ele, mostrando a posição e o tempo de queda, com destaque para a aceleração (gravidade).

<p align="center">
  <img width="350" alt="queda_livre_grafico" src="https://github.com/user-attachments/assets/a9ae8df0-b591-4381-8c72-0f7ab7f01d48">
  <br>
  <em> Figura 1</em>
</p>

### Equações:

A força $\vec{F}_g$ (força gravitacional) que atua no objeto de massa $m$ caindo da altura $H$, é dada pela equação:

$$\begin{equation}
\vec{F}_g = - m \cdot g \hat{k}
\end{equation}$$

Definição dos vetores posição, velocidade e aceleração: 

$$\begin{equation}
\vec{r}(t) =  z(t)\hat{k}
\end{equation}$$

$$\begin{equation}
\vec{v}(t) =  \dot{z} (t) \hat{k}
\end{equation}$$

$$\begin{equation}
\vec{a}(t) = \ddot{z} (t) \hat{k}
\end{equation}$$

Usando a força da gravidade na forma de coornadas temos: 

$$\begin{equation}
-m \cdot g  \hat{k} = - m \cdot \ddot{z} \hat{k}  
\end{equation}$$

Neste sistema, a gravidade é a aceleração, único movimento presente. Isso implica que $g = \ddot{z}$. Resolvendo a EDO acima, encontramos a seguinte solução: 

**$$\begin{equation}
z(t) = z_0 + v_0 t - \frac{1}{2} g t^2 
\end{equation}$$**

Quando substituimos os dados das condições iniciais da queda livre, ($v_0 = 0$ e $z_0 = H$), encontramos: 

$$\begin{equation}
z(t) = H - \frac{1}{2} g t^2 
\end{equation}$$

### Considerando a Viscosidade
Agora, quando introduzimos a viscosidade, o movimento do objeto é afetado pela **força de resistência viscosa**, dada por:

$$ F_{\text{viscosa}} = -\eta v $$

Onde:
- $\eta$: é a viscosidade do fluido
- $v$: é a velocidade do objeto.

A equação de movimento agora:

$$m \frac{dv}{dt} = - m g - \eta v$$

Isso resulta em uma solução para a velocidade do objeto que leva em conta a resistência do fluido, como a água ou o mel. A solução dessa equação diferencial, levando em consideração a viscosidade, pode ser expressa como:

$$v(t) = \frac{m g}{\eta} \left( 1 - e^{-\frac{\eta}{m} t} \right)$$


### Aplicação de queda livre no jogo
No jogo, ampliamos o conceito clássico de queda livre para explorar como diferentes variáveis afetam o movimento:

**1. Gravidades Variadas:** O jogador pode experimentar quedas em diferentes ambientes gravitacionais, como:
* Terra: $g = 9,8 \ \text{m/s}^2$
* Lua: $g = 1,6 \ \text{m/s}^2$
* Marte: $g = 3,7 \ \text{m/s}^2$

**2. Viscosidades:** No jogo temos três fluidos diferenets, cada um com sua própria viscosidade, que afeta o tempo de queda. Valores de viscosidade aplicados aos fluidos:
* Ar: $\eta = 0,001 \ \text{mP}$ - Baixa viscosidade, resistência quase insignificante ao movimento
* Água: $\eta = 1 \ \text{mP}$ - Viscosidade moderada, resistência perceptível ao movimento
* Mel: $\eta = 10.000 \ \text{mP}$ - Alta viscosidade, grande resistência ao movimento


**3. Peso dos Objetos:** O jogador pode escolher personagens com diferentes massas, representando objetos variados. Embora o peso não afete o tempo de queda em condições ideais, ele desempenha um papel importante em meios com viscosidade. São três opções de massa:
* Gato: $m = 4 \ \text{Kg}$
* Porco: $m = 30 \ \text{Kg}$
* Vaca: $m = 100 \ \text{Kg}$


## Implementação
**Linguagens e Pacotes:**
O projeto foi implementado em Python3, utilizando os pacotes PyGame, NumPy, Scipy e Matplotlib. Cada um desses pacotes oferecem ferrametas específicas que foram necessárias para criar a interface do jogo.

## Como jogar?
- **Instalação de Dependências:**
  - Abra o terminal 
  - Certifique-se de que o Python 3.6+ e Git estão instalados.
  - Clone o repositório, usando:
    ```bash
    git clone https://github.com/GabriellaAlmeida07/pygame
    cd pygame
  
  - Instale pygame:
    ```bash
    python -m pip install -U pygame --user
    
  - Instale numpy:
    ```bash
    python -m pip install -U numpy --user

  - Instale matplotlib:
    ```bash
    python -m pip install -U matplotlib --user

  - Instale scipy:
    ```bash
    python -m pip install -U scipy --user

      
- **Abrindo o jogo:**  
  - Para rodar o jogo, utilize o código:
    ```python
      python3 Jogo.py
    ```
- **No jogo:**
  - Passo 1: Clique em start para começar o jogo;
  - Passo 2: Selecione um personagem entre gato, vaca e porco;
  - Passo 3: Selecione a viscosidade entre água, mel e ar;
  - Passo 4: Selecione a gravidade entre Lua, Terra e Marte;
  - Passo 5: Digite sua adivanhação do tempo de queda;
  - Passo 6: Assista seu personagem em queda livre e descubra se acertou o tempo de queda.
   

## Informações sobre o projeto
Este projeto foi desenvolvido por:
```
Gabriella Almeida: 15528121 - gabriella_almeida@usp.br
Johana Jimena Pizarro Laquise: 10248986 - johana_pizarro.l@usp.br
Kauany Fernandes Santos: 15522379 - kauanysantos@usp.br
Laura Pazini Medeiros: 15468452 - laurapazinimedeiros@usp.br
Luysa de Souza Gonçalves: 15474077 - luysasouzag@usp.br
```
Como parte do processo avaliativo da disciplina 7600105 - Física Básica I (2024) da USP-São Carlos ministrada pela Prof. Krissia de Zawadzki.



