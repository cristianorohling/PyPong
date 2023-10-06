import pygame
from pygame.locals import *
import random
import pygame.mixer
import random
import os

#Variaveis globais
pontuacao_maxima = 10
jogar_contra_IA = 1
pontos_jogador = 0
pontos_oponente = 0
diretorio_atual = os.path.dirname(os.path.abspath(__file__))

#Inicializando Sons
pygame.mixer.init()
som_intro = pygame.mixer.Sound(diretorio_atual + "\intro.wav")
som_pop = pygame.mixer.Sound(diretorio_atual + "\pop.wav")
som_erro = pygame.mixer.Sound(diretorio_atual + "\error.wav")
som_colisao_parede = pygame.mixer.Sound(diretorio_atual + "\popwall.wav")


# Inicialização do Pygame
pygame.init()

# Configurações da tela
largura_tela = 800      
altura_tela = 600
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("PyPong")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)

# Defina o caminho para a fonte
caminho_fonte = diretorio_atual + "\AtariSmall.ttf"

# Defina o tamanho da fonte
tamanho_fonte_grande = 150
tamanho_fonte_pequena = 30

# Carregue a fonte
fonte_grande = pygame.font.Font(caminho_fonte, tamanho_fonte_grande)
fonte_pequena = pygame.font.Font(caminho_fonte, tamanho_fonte_pequena)

# Dimensões do jogo
largura_moldura = 10
altura_raquete = 120
largura_raquete = 20
tamanho_bola = 15

# Posições iniciais
posicao_raquete_jogador = altura_tela // 2 - altura_raquete // 2
posicao_raquete_oponente = altura_tela // 2 - altura_raquete // 2
posicao_bola = [largura_tela // 2, altura_tela // 2]
velocidade_raquete = 8
velocidade_bola = [6, 6]

# Dicionário para armazenar o estado das teclas
teclas_press = {
    K_UP: False,
    K_DOWN: False,
    ord('w'): False,
    ord('s'): False
}


def mostrar_instrucoes():
    tela.fill(PRETO)
    
    instrucoes_ia = fonte_pequena.render("Contra IA:", True, VERMELHO)
    instrucoes_ia_controles = fonte_pequena.render("- W e S: Mover a raquete", True, VERDE)
    
    instrucoes_humano = fonte_pequena.render("Contra Humano:", True, VERMELHO)
    instrucoes_humano_controles_1 = fonte_pequena.render("- Jogador 1: W e S", True, VERDE)
    instrucoes_humano_controles_2 = fonte_pequena.render("- Jogador 2: Seta para cima e Seta para baixo", True, VERDE)
    
    tela.blit(instrucoes_ia, (largura_tela // 2 - instrucoes_ia.get_width() // 2, 100))
    tela.blit(instrucoes_ia_controles, (largura_tela // 2 - instrucoes_ia_controles.get_width() // 2, 150))
    
    tela.blit(instrucoes_humano, (largura_tela // 2 - instrucoes_humano.get_width() // 2, 300))
    tela.blit(instrucoes_humano_controles_1, (largura_tela // 2 - instrucoes_humano_controles_1.get_width() // 2, 350))
    tela.blit(instrucoes_humano_controles_2, (largura_tela // 2 - instrucoes_humano_controles_2.get_width() // 2, 400))
    
    # Adicionar o rodapé
    rodape_texto = fonte_pequena.render("2023 - Desenvolvido por Cristiano Rohling", True, VERMELHO)
    tela.blit(rodape_texto, (largura_tela // 2 - rodape_texto.get_width() // 2, altura_tela - rodape_texto.get_height() - 10))
    
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                tela_apresentacao()
                return



def zera_pontos():
    global pontos_jogador, pontos_oponente
    pontos_jogador = 0
    pontos_oponente = 0

def tela_apresentacao():
    tela.fill(PRETO)
    texto = fonte_grande.render("PONG.py", True, VERMELHO)
    tela.blit(texto, (largura_tela // 2 - texto.get_width() // 2, altura_tela // 2 - texto.get_height() // 2))
    
    # Opções de jogo    
    opcao_1 = fonte_pequena.render("(1) Jogar contra IA", True, VERDE)
    opcao_2 = fonte_pequena.render("(2) Jogar contra Humano", True, VERDE)
    opcao_3 = fonte_pequena.render("(3) Instruções", True, VERDE)
    opcao_4 = fonte_pequena.render("(ESC) Sair", True, VERDE)
    tela.blit(opcao_1, (largura_tela // 2 - opcao_1.get_width() // 2, altura_tela // 2 + 70))
    tela.blit(opcao_2, (largura_tela // 2 - opcao_2.get_width() // 2, altura_tela // 2 + 120))
    tela.blit(opcao_3, (largura_tela // 2 - opcao_3.get_width() // 2, altura_tela // 2 + 170))
    tela.blit(opcao_4, (largura_tela // 2 - opcao_4.get_width() // 2, altura_tela // 2 + 220))
    texto = fonte_grande.render("PONG.py", True, VERDE)
    
    # Adicionar o rodapé
    rodape_texto = fonte_pequena.render("2023 - Desenvolvido por Cristiano Rohling", True, VERMELHO)
    tela.blit(rodape_texto, (largura_tela // 2 - rodape_texto.get_width() // 2, altura_tela - rodape_texto.get_height() - 10))
    
    pygame.display.flip()
    som_intro.play()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:                    
                    jogar_contra_IA = 1
                    jogo_pong()                    
                    return False
                elif event.key == pygame.K_2:                    
                    jogar_contra_IA = 0
                    jogo_pong_contra_humano()
                    return True
                elif event.key == pygame.K_3:
                    mostrar_instrucoes()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()



def desenhar_moldura():
    pygame.draw.rect(tela, VERDE, (0, 0, largura_tela, altura_tela), largura_moldura)

def desenhar_linha_pontilhada():
    espessura_linha = 10
    comprimento_traco = 50
    espacamento_traco = 10
    y = 0

    while y < altura_tela:
        pygame.draw.line(tela, VERDE, (largura_tela // 2, y), (largura_tela // 2, y + comprimento_traco), espessura_linha)
        y += comprimento_traco + espacamento_traco


def desenhar_raquetes():
    pygame.draw.rect(tela, VERDE, (largura_raquete, posicao_raquete_jogador, largura_raquete, altura_raquete))
    pygame.draw.rect(tela, VERDE, (largura_tela - largura_raquete * 2, posicao_raquete_oponente, largura_raquete, altura_raquete))

def desenhar_bola():
    pygame.draw.rect(tela, VERMELHO, (posicao_bola[0] - tamanho_bola, posicao_bola[1] - tamanho_bola, tamanho_bola * 2, tamanho_bola * 2))


def mover_raquete_jogador():
    global posicao_raquete_jogador

    if teclas_press[ord('w')]:
        posicao_raquete_jogador -= velocidade_raquete
    if teclas_press[ord('s')]:
        posicao_raquete_jogador += velocidade_raquete

    # Limita a posição da raquete do jogador dentro da tela
    if posicao_raquete_jogador < 0:
        posicao_raquete_jogador = 0
    elif posicao_raquete_jogador > altura_tela - altura_raquete:
        posicao_raquete_jogador = altura_tela - altura_raquete

def mover_raquete_oponente():
    global posicao_raquete_oponente

    # Probabilidade de 30% para um movimento incorreto
    probabilidade_erro = 0.3

    if random.random() < probabilidade_erro:
        # Realiza um movimento incorreto aleatório
        movimento_incorreto = random.choice([-1, 1])
        posicao_raquete_oponente += movimento_incorreto * velocidade_raquete
    else:
        # Movimento correto baseado na posição da bola
        if posicao_raquete_oponente + altura_raquete // 2 < posicao_bola[1]:
            posicao_raquete_oponente += velocidade_raquete
        elif posicao_raquete_oponente + altura_raquete // 2 > posicao_bola[1]:
            posicao_raquete_oponente -= velocidade_raquete

    # Limita a posição da raquete do oponente dentro da tela
    if posicao_raquete_oponente < 0:
        posicao_raquete_oponente = 0
    elif posicao_raquete_oponente > altura_tela - altura_raquete:
        posicao_raquete_oponente = altura_tela - altura_raquete
        

def mover_raquete_oponente_humano():
    global posicao_raquete_oponente

    # Captura as teclas pressionadas pelo jogador humano
    if teclas_press[pygame.K_UP]:
        posicao_raquete_oponente -= velocidade_raquete
    elif teclas_press[pygame.K_DOWN]:
        posicao_raquete_oponente += velocidade_raquete

    # Limita a posição da raquete do oponente dentro da tela
    if posicao_raquete_oponente < 0:
        posicao_raquete_oponente = 0
    elif posicao_raquete_oponente > altura_tela - altura_raquete:
        posicao_raquete_oponente = altura_tela - altura_raquete


def mover_bola():
    global posicao_bola, velocidade_bola, pontos_jogador, pontos_oponente, perdedor_da_jogada

    posicao_bola[0] += velocidade_bola[0]
    posicao_bola[1] += velocidade_bola[1]

    # Verifica colisões com as bordas da tela
    if posicao_bola[1] > altura_tela - tamanho_bola or posicao_bola[1] < tamanho_bola:
        velocidade_bola[1] = -velocidade_bola[1]
        som_colisao_parede.play()

    # Verifica colisões com as raquetes
    if posicao_bola[0] < largura_raquete * 2 + tamanho_bola and posicao_raquete_jogador + 5 < posicao_bola[1] < posicao_raquete_jogador + altura_raquete - 5:
        velocidade_bola[0] = -velocidade_bola[0]
        som_pop.play()
    elif posicao_bola[0] > largura_tela - largura_raquete * 2 - tamanho_bola and posicao_raquete_oponente + 5 < posicao_bola[1] < posicao_raquete_oponente + altura_raquete - 5:
        velocidade_bola[0] = -velocidade_bola[0]
        som_pop.play()

    # Verifica se a bola passou da raquete do jogador
    if posicao_bola[0] < tamanho_bola:
        pontos_oponente += 1
        perdedor_da_jogada = 0
        if pontos_oponente >= pontuacao_maxima:
            jogo_terminado()
        else:
            reiniciar_jogo()
    elif posicao_bola[0] > largura_tela - tamanho_bola:
        pontos_jogador += 1
        perdedor_da_jogada = 1
        if pontos_jogador >= pontuacao_maxima:
            jogo_terminado()
        else:
            reiniciar_jogo()



def reiniciar_jogo():
    global posicao_bola, velocidade_bola, perdedor_da_jogada

    if perdedor_da_jogada == 1:
        posicao_bola = [largura_tela - largura_raquete * 2 - tamanho_bola, posicao_raquete_oponente + altura_raquete // 2]
        velocidade_bola = [velocidade_bola[0], velocidade_bola[1]]
    else:
        posicao_bola = [largura_raquete * 2 + tamanho_bola, posicao_raquete_jogador + altura_raquete // 2]
        velocidade_bola = [-velocidade_bola[0], velocidade_bola[1]]   

def exibir_pontuacao():
    fonte = pygame.font.Font(diretorio_atual + "\AtariSmall.ttf", 120)
    texto_jogador = fonte.render(str(pontos_jogador), True, VERDE)
    texto_oponente = fonte.render(str(pontos_oponente), True, VERDE)
    tela.blit(texto_jogador, (largura_tela // 2 - 100, 10))
    tela.blit(texto_oponente, (largura_tela // 2 + 30, 10))

def jogo_pong():
    global posicao_raquete_jogador, pontos_jogador, pontos_oponente    
    zera_pontos()
    # Loop principal do jogo
    rodando = True
    clock = pygame.time.Clock()

    while rodando:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                rodando = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    rodando = False
                elif event.key in teclas_press:
                    teclas_press[event.key] = True
            elif event.type == KEYUP:
                if event.key in teclas_press:
                    teclas_press[event.key] = False

        mover_raquete_jogador()
        mover_raquete_oponente()
        mover_bola()

        # Renderização do jogo
        tela.fill(PRETO)
        desenhar_moldura()
        desenhar_linha_pontilhada()
        desenhar_raquetes()
        desenhar_bola()
        exibir_pontuacao()
        pygame.display.flip()
        
        
def jogo_pong_contra_humano():
    global posicao_raquete_jogador, posicao_raquete_oponente, pontos_jogador, pontos_oponente    
    
    zera_pontos()
    # Loop principal do jogo
    rodando = True
    clock = pygame.time.Clock()

    while rodando:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    rodando = False
                elif event.key == pygame.K_w:
                    teclas_press[pygame.K_w] = True
                elif event.key == pygame.K_s:
                    teclas_press[pygame.K_s] = True
                elif event.key == pygame.K_UP:
                    teclas_press[pygame.K_UP] = True
                elif event.key == pygame.K_DOWN:
                    teclas_press[pygame.K_DOWN] = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    teclas_press[pygame.K_w] = False
                elif event.key == pygame.K_s:
                    teclas_press[pygame.K_s] = False
                elif event.key == pygame.K_UP:
                    teclas_press[pygame.K_UP] = False
                elif event.key == pygame.K_DOWN:
                    teclas_press[pygame.K_DOWN] = False

        mover_raquete_jogador()
        mover_raquete_oponente_humano()
        mover_bola()

        # Renderização do jogo
        tela.fill(PRETO)
        desenhar_moldura()
        desenhar_linha_pontilhada()
        desenhar_raquetes()
        desenhar_bola()
        exibir_pontuacao()
        pygame.display.flip()

        
def jogo_terminado():
    global pontos_jogador, pontos_oponente

    if pontos_jogador >= pontuacao_maxima:
        tela.fill(PRETO)
        mensagem = fonte_pequena.render("Player 1 Venceu!", True, VERMELHO)
        tela.blit(mensagem, (largura_tela // 2 - mensagem.get_width() // 2, altura_tela // 2 - mensagem.get_height() // 2))
        zera_pontos()        
        som_intro.play()
    elif pontos_oponente >= pontuacao_maxima:
        tela.fill(PRETO)
        mensagem = fonte_pequena.render("Player 2 Venceu", True, VERMELHO)
        tela.blit(mensagem, (largura_tela // 2 - mensagem.get_width() // 2, altura_tela // 2 - mensagem.get_height() // 2))
        zera_pontos()        
        som_erro.play()    
    
    pygame.display.update()    

    aguardando_tecla = True
    while aguardando_tecla:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                aguardando_tecla = False
                tela_apresentacao()

        pygame.time.Clock().tick(60)


def main():
    # Reinicia as posições e pontuações
    global posicao_raquete_jogador, pontos_jogador, pontos_oponente, posicao_raquete_jogador, posicao_raquete_oponente
    posicao_raquete_jogador = altura_tela // 2 - altura_raquete // 2
    posicao_raquete_oponente = altura_tela // 2 - altura_raquete // 2
    posicao_bola = [largura_tela // 2, altura_tela // 2]
    zera_pontos()
    
    #reinicia
    # Inicia a tela de apresentação
    tela_apresentacao()

    # Aguarda 3 segundos
    #pygame.time.wait(3000)

    # Inicia o jogo
    #jogo_pong()

    # Encerra o Pygame
    pygame.quit()

# Inicia o jogo
if __name__ == '__main__':
    main()