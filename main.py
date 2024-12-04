import pygame 
import pygame.mixer as mixer
import math
import random
import sys
import os

# Organizacao da pasta de assets
def asset_path(subpasta, nome_arquivo):
    return os.path.join(os.path.dirname(__file__), "assets", subpasta, nome_arquivo)
    # retorna o diretorio onde esta o main, e acessa as subpastas da pasta assets

# Inicializar o pygame e Criar a janela do jogo 
pygame.init()

pygame.key.set_repeat(1, 1)  # 1ms de delay inicial, repetição a cada 10ms

clock = pygame.time.Clock()
FPS = 200 # taxa de quadros

# Timer e controle de velocidade
tempo_jogo = 0 # Tempo total de jogo em segundos
ultimo_incremento = 0 # Controla o último incremento de velocidade
incremento_velocidade = 1  # Velocidade extra adicionada a cada 5 segundos

altura = 720
largura = 1280
screen = pygame.display.set_mode((largura,altura)) # criando a tela
game_state = "start_menu"

pygame.display.set_caption("Air Combat")

# FUNDO
fundo = pygame.image.load(asset_path("imagens", "Fundo.png"))
tela_inicio = pygame.image.load(asset_path("imagens", 'Tela_inicio.png'))
tela_game_over = pygame.image.load(asset_path("imagens", 'Game_Over.png'))

# JOGADOR
velocidadeJogador = 4

JogadorIMG = pygame.image.load(asset_path("imagens", "Jogador.png")) # Imagem da nave Jogador
JogadorLarguraIMG = 128 # pra subtrair na hora da borda
JogadorX = largura * 0.45 # pos inicial eixo X da nave
JogadorY = altura * 0.83 # pos inicial eixo Y da nave
Jogador_MudaX = 0 # isso sera somado ao JogadorX.

def posicionar_jogador():
    Jogador_MudaX = 0 
    JogadorIMG = pygame.image.load(asset_path("imagens", "Jogador.png"))
    JogadorLarguraIMG = 128 
    JogadorX = largura * 0.45 
    JogadorY = altura * 0.83 
    


# MISSIL
velocidadeMissil = 7
MissilIMG = pygame.image.load(asset_path("imagens", 'Missil.png'))
MissilX = 0
MissilY = altura * 0.50
Missil_MudaX = 0 
Missil_MudaY = velocidadeMissil 
MissilEstado = "Carregado"


# SOM
mixer.Channel(0).play(mixer.Sound(asset_path("sons", "Soundtrack.mp3")))
#mixer.Channel(0).set_volume(0.025)
#mixer.Channel(1).set_volume(0.01)

def ajustar_volume(volume_geral):
    volume_musica = 1.6 * volume_geral  # Volume proporcional ao volume geral
    volume_explosao = 0.64 * volume_geral  # Volume proporcional ao volume geral

    mixer.Channel(0).set_volume(volume_musica)  # Ajusta o canal de música
    mixer.Channel(1).set_volume(volume_explosao)  # Ajusta o canal de explosão

volume_geral = 0.1  # Valor entre 0 (mudo) e 1 (máximo)
ajustar_volume(volume_geral)



# INIMIGO
velocidadeInimigo = 2

# lista para os atributos de cada inimigo
InimigoIMG = []
InimigoLarguraIMG = []
InimigoX = []
InimigoY = []
Inimigo_MudaX = []
Inimigo_MudaY = []

# quantidade de inimigos
InimigoQuant = 3

# insercao de dados de cada inimigo
def criaInimigos():
    for i in range(InimigoQuant):
        InimigoIMG.append(pygame.image.load(asset_path("imagens", 'Inimigo.png'))) # Imagem pro Inimigo 
        InimigoIMG.append(pygame.image.load(asset_path("imagens", 'Inimigo.png'))) # Imagem pro Inimigo
        InimigoLarguraIMG.append(50) # pra subtrair na hora da borda 
        InimigoX.append(random.randint(0, largura - InimigoLarguraIMG[i])) # pos inicial eixo X randomizado 
        InimigoY.append(altura * 0.05) # posicao inicial Y comum
        Inimigo_MudaX.append(random.choice([-1, 1]) * velocidadeInimigo) #  Deixamos uma velocidade randomica pra esquerda e direita para o eixo x 
        Inimigo_MudaY.append(random.randint(1, 2) * 0.25)  # Randomizamos um pouco a velocidade de queda 

def deletaInimigos():
    del InimigoIMG [:]
    del InimigoLarguraIMG [:]
    del InimigoX [:]
    del InimigoY [:]
    del Inimigo_MudaX [:]
    del Inimigo_MudaY [:]


# utilizando formula de distancia entre cordenadas de dois pontos
def Colisao(X1,Y1,X2,Y2):
    Distancia = math.sqrt(math.pow(X1 - X2, 2) + (math.pow(Y1 - Y2, 2)))
    if Distancia <=60  :
        ExplosaoIMG = pygame.image.load(asset_path("imagens", 'Explosao.png'))
        screen.blit(ExplosaoIMG, (MissilX, MissilY))
        return True
    else:
        return False

# funcoes para cada objeto aparecer na tela.
def Jogador(x,y):
    screen.blit(JogadorIMG, (x,y)) # inserçao do aviao sobre a janela
def Inimigo(x,y,i):
    screen.blit(InimigoIMG[i], (x,y)) 
def AtirarMissil(x,y): # comeca o lancamento do Missil 
    global MissilEstado
    MissilEstado = "Descarregado"
    screen.blit(MissilIMG, (x,y))

def Menu_Inicio():
   screen.fill((0, 0, 0))
   screen.blit(tela_inicio,(0,0))
   # Centralizar ou redimensionar
   tela_inicio_redimensionada = pygame.transform.scale(tela_inicio, (largura, altura))
   screen.blit(tela_inicio_redimensionada, (0, 0))  # Redimensionada para preencher a janela
   pygame.display.update()

def Menu_Game_Over():
   screen.fill((0, 0, 0, 0.6))

   # Centralizar ou redimensionar
   tela_game_over_redimensionada = pygame.transform.scale(tela_game_over, (largura, altura))
   screen.blit(tela_game_over_redimensionada, (0, 0))  # Redimensionada para preencher a janela

   # Texto adicional
   font = pygame.font.SysFont('arial', 40)
   texto_tempo_final = font.render(f"Você sobreviveu por {int(tempo_jogo)} segundos!", True, (255, 255, 255))
   screen.blit(texto_tempo_final, (largura / 2 - texto_tempo_final.get_width() / 2, altura / 2))
   
   restart_button = font.render('R - Reiniciar', True, (255, 255, 255))
   quit_button = font.render('Q - Fechar a janela', True, (255, 255, 255))
   
   texto_tempo_final = font.render(f"Você sobreviveu por {int(tempo_jogo)} segundos!", True, (255, 255, 255))
   screen.blit(texto_tempo_final, (largura / 2 - texto_tempo_final.get_width() / 2, altura / 2))
   pygame.display.update()   

game_over = False



# LOOP PRINCIPAL DO JOGO
while True:
    clock.tick(FPS) # controla taxa de quadros
    delta_time = clock.get_time() / 1000  # tempo em segundos por frame

    # Aumentar a velocidade dos inimigos a cada 5 segundos
    if tempo_jogo - ultimo_incremento >= 5:
        velocidadeInimigo += incremento_velocidade  # Incrementa a velocidade dos inimigos
        ultimo_incremento = tempo_jogo  # Atualiza o último incremento

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if game_state == "start_menu":
       Menu_Inicio()
       keys = pygame.key.get_pressed()
       if keys[pygame.K_SPACE]:
           game_state = "game"
           game_over = False
        
    if game_state == "game_over":
        Menu_Game_Over()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
           deletaInimigos()
           posicionar_jogador()
           tempo_jogo = 0  # Reseta o timer
           ultimo_incremento = 0  # Reseta o controle de incremento
           velocidadeInimigo = 2  # Reseta a velocidade inicial dos inimigos
           game_state = "start_menu"
        if keys[pygame.K_q]:
            pygame.quit()
            quit()
        
    elif game_state == "game":
        tempo_jogo += delta_time  # Incrementa o tempo total do jogo
        
        # Exibir o timer na tela
        fonte_timer = pygame.font.SysFont('arial', 30)
        texto_timer = fonte_timer.render(f"Tempo: {int(tempo_jogo)}s", True, (255, 255, 255))
        screen.blit(texto_timer, (largura - texto_timer.get_width() - 20, altura - texto_timer.get_height() - 20))

        posicionar_jogador()
        criaInimigos()

        screen.fill((255,255,255)) # mudando a cor da janela pra branco
        screen.blit(fundo,(0,0))

        # Atualizar a velocidade dos inimigos a cada 5 segundos
        if tempo_jogo - ultimo_incremento >= 5:
            velocidadeInimigo += incremento_velocidade
            ultimo_incremento = tempo_jogo

        # Exibir o timer na tela
        fonte_timer = pygame.font.SysFont('arial', 30)
        texto_timer = fonte_timer.render(f"Tempo: {int(tempo_jogo)}s", True, (255, 255, 255))
        screen.blit(texto_timer, (largura - texto_timer.get_width() - 20, altura - texto_timer.get_height() - 20))

        for event in pygame.event.get():
            if(event.type == pygame.QUIT): # caso o evento quit() é acionado, o programa fecha. o evento quit() é clicar no X na janela.
                running = False
        
        # Teclado Jogador
            # Teclado Jogador (no loop principal)
            keys = pygame.key.get_pressed()  # Captura o estado de todas as teclas pressionadas

            # Movimentação do Jogador
            if keys[pygame.K_LEFT]:  # Se a tecla A estiver pressionada, movimenta a nave para a esquerda
                Jogador_MudaX = -velocidadeJogador
            elif keys[pygame.K_RIGHT]:  # Se a tecla D estiver pressionada, movimenta a nave para a direita
                Jogador_MudaX = velocidadeJogador
            else:  # Se nenhuma tecla direcional estiver pressionada, a nave para
                Jogador_MudaX = 0
            JogadorX += Jogador_MudaX     
                    

            # Disparo do Míssil
            if keys[pygame.K_SPACE] and MissilEstado == "Carregado":  # Se a tecla de espaço for pressionada e o míssil estiver carregado
                MissilX = JogadorX + JogadorLarguraIMG / 4  # Calcula a posição do míssil com base na nave
                AtirarMissil(MissilX, MissilY)  # Chama a função para disparar o míssil


        # Movimentos Missil
        if (MissilY < 0): 
            MissilY = altura * 0.90
            MissilEstado = "Carregado" # no momento que o Missil atinge o final do mapa, ele reseta.   
        if (MissilEstado == "Descarregado"): # enquanto o Missil nao chega no final do mapa, ele vai andando
            AtirarMissil(MissilX,MissilY)
            MissilY -= Missil_MudaY

        for i in range(InimigoQuant):
            # Movimentos Inimigo
            InimigoX[i] = InimigoX[i] + Inimigo_MudaX[i]  
            InimigoY[i] = InimigoY[i] + Inimigo_MudaY[i] 
            # Borda da tela para Inimigo
            if(InimigoX[i] < 0):
                Inimigo_MudaX[i] = velocidadeInimigo
            if(largura - InimigoLarguraIMG[i] < InimigoX[i]): 
                Inimigo_MudaX[i] = -velocidadeInimigo
            if(JogadorY <= InimigoY[i]): # Perdeu, deixou passar o asteroid
                for i in range(InimigoQuant):
                    Inimigo_MudaX[i] = 0 # inimigos param
                    Inimigo_MudaY[i] = 0 # inimigos param        
                game_over = True
                game_state = "game_over"
            # verificar se teve colisao entre o inimigo e o Missil
            Resultado = Colisao(InimigoX[i],InimigoY[i],MissilX,MissilY)
            if (Resultado):
                mixer.Channel(1).play(mixer.Sound(asset_path("sons", 'explosao.mp3')))
                MissilY = altura * 0.90
                MissilEstado = "Carregado" # caso aconteceu uma colisao, resetar o Missil
                InimigoX[i] = random.randint(0, largura - InimigoLarguraIMG[i]) # pos inicial eixo X da nave
                InimigoY[i] = altura * 0.01 # pos inicial eixo Y da nave
            Inimigo(InimigoX[i],InimigoY[i], i) # chamada da funcao para movimentar inimigo

        # Borda da tela para Jogador
        if(JogadorX < 0):
            JogadorX = 0.1
        if(largura - JogadorLarguraIMG < JogadorX):
            JogadorX = largura - JogadorLarguraIMG 
        
        # Chamadas 
        Jogador(JogadorX,JogadorY) # chamada da funcao Jogador para atualizar a pocisao do Jogador em cada frame
        pygame.display.update()

