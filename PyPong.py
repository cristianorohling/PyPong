import pygame
from pygame.locals import *
import random
import pygame.mixer
import os
import sys
import math
import json

# --- Configurações Globais ---
# Correção para o Executável encontrar os arquivos
if getattr(sys, 'frozen', False):
    DIRETORIO_ATUAL = os.path.dirname(sys.executable)
else:
    DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))

LARGURA_ORIGINAL = 800
ALTURA_ORIGINAL = 600
PONTUACAO_MAXIMA = 10
ARQUIVO_CONFIG = os.path.join(DIRETORIO_ATUAL, "config.json")
ESPESSURA_BORDA = 15

# --- Cores Modernas (Paleta Neon) ---
COR_FUNDO = (5, 5, 10)       
NEON_VERDE = (57, 255, 20)
NEON_AZUL = (0, 255, 255)
NEON_ROSA = (255, 20, 147)
NEON_AMARELO = (255, 255, 0)
NEON_ROXO = (148, 0, 211)
NEON_LARANJA = (255, 69, 0)
BRANCO = (255, 255, 255)
CINZA_GRID = (40, 20, 60) 

LISTA_CORES_NEON = [NEON_VERDE, NEON_AZUL, NEON_ROSA, NEON_AMARELO, NEON_ROXO, NEON_LARANJA]

# --- SISTEMA DE IDIOMAS ---
IDIOMAS = ["pt", "en", "es", "it", "de", "fr"]
NOMES_IDIOMAS = {
    "pt": "IDIOMA: PORTUGUÊS", "en": "LANGUAGE: ENGLISH", "es": "IDIOMA: ESPAÑOL",
    "it": "LINGUA: ITALIANO", "de": "SPRACHE: DEUTSCH", "fr": "LANGUE: FRANÇAIS"
}
TEXTOS = {
    "pt": { "vs_ia": "VS CPU", "vs_player": "VS P2", "options": "OPÇÕES", "exit": "SAIR", "sfx_on": "EFEITOS: ON", "sfx_off": "EFEITOS: OFF", "music_on": "MÚSICA: ON", "music_off": "MÚSICA: OFF", "screen_full": "TELA: CHEIA", "screen_win": "TELA: JANELA", "back": "VOLTAR", "record": "RECORD", "go": "VAI!", "win_p1": "P1 VENCEU!", "win_p2": "P2 VENCEU!", "win_cpu": "CPU VENCEU!", "click_back": "CLIQUE P/ VOLTAR", "footer": "F11: Tela Cheia | ESC: Voltar" },
    "en": { "vs_ia": "VS CPU", "vs_player": "VS P2", "options": "OPTIONS", "exit": "EXIT", "sfx_on": "SFX: ON", "sfx_off": "SFX: OFF", "music_on": "MUSIC: ON", "music_off": "MUSIC: OFF", "screen_full": "FULLSCREEN", "screen_win": "WINDOWED", "back": "BACK", "record": "RECORD", "go": "GO!", "win_p1": "P1 WINS!", "win_p2": "P2 WINS!", "win_cpu": "CPU WINS!", "click_back": "CLICK TO RETURN", "footer": "F11: Fullscreen | ESC: Back" },
    "es": { "vs_ia": "VS CPU", "vs_player": "VS P2", "options": "OPCIONES", "exit": "SALIR", "sfx_on": "EFECTOS: ON", "sfx_off": "EFECTOS: OFF", "music_on": "MÚSICA: ON", "music_off": "MÚSICA: OFF", "screen_full": "PANTALLA: FULL", "screen_win": "VENTANA", "back": "VOLVER", "record": "RÉCORD", "go": "¡VAMOS!", "win_p1": "¡P1 GANA!", "win_p2": "¡P2 GANA!", "win_cpu": "¡CPU GANA!", "click_back": "CLIC PARA VOLVER", "footer": "F11: Fullscreen | ESC: Volver" },
    "it": { "vs_ia": "VS CPU", "vs_player": "VS P2", "options": "OPZIONI", "exit": "ESCI", "sfx_on": "EFFETTI: ON", "sfx_off": "EFFETTI: OFF", "music_on": "MUSICA: ON", "music_off": "MUSICA: OFF", "screen_full": "INTERO", "screen_win": "FINESTRA", "back": "INDIETRO", "record": "RECORD", "go": "VIA!", "win_p1": "P1 VINCE!", "win_p2": "P2 VINCE!", "win_cpu": "CPU VINCE!", "click_back": "CLICCA PER TORNARE", "footer": "F11: Fullscreen | ESC: Indietro" },
    "de": { "vs_ia": "VS CPU", "vs_player": "VS P2", "options": "OPTIONEN", "exit": "ENDE", "sfx_on": "EFFEKTE: EIN", "sfx_off": "EFFEKTE: AUS", "music_on": "MUSIK: EIN", "music_off": "MUSIK: AUS", "screen_full": "VOLLBILD", "screen_win": "FENSTER", "back": "ZURÜCK", "record": "REKORD", "go": "LOS!", "win_p1": "P1 SIEGT!", "win_p2": "P2 SIEGT!", "win_cpu": "CPU SIEGT!", "click_back": "KLICKEN ZURÜCK", "footer": "F11: Vollbild | ESC: Zurück" },
    "fr": { "vs_ia": "VS CPU", "vs_player": "VS P2", "options": "OPTIONS", "exit": "QUITTER", "sfx_on": "EFFETS: ON", "sfx_off": "EFFETS: OFF", "music_on": "MUSIQUE: ON", "music_off": "MUSIQUE: OFF", "screen_full": "PLEIN ÉCRAN", "screen_win": "FENÊTRE", "back": "RETOUR", "record": "RECORD", "go": "ALLEZ!", "win_p1": "P1 GAGNE!", "win_p2": "P2 GAGNE!", "win_cpu": "CPU GAGNE!", "click_back": "CLIQUER POUR RETOUR", "footer": "F11: Plein Écran | ESC: Retour" }
}

# --- Inicialização ---
pygame.mixer.init()
pygame.mixer.set_num_channels(8) 
pygame.init()

# --- Gerenciador de Configurações ---
class ConfigManager:
    def __init__(self):
        self.dados = {
            "fullscreen": True, 
            "sfx_ativo": True, 
            "musica_ativa": True, 
            "high_score": 0, 
            "idioma": "pt"
        }
        self.carregar()

    def carregar(self):
        try:
            if os.path.exists(ARQUIVO_CONFIG):
                with open(ARQUIVO_CONFIG, 'r') as f: self.dados.update(json.load(f))
        except: pass

    def salvar(self):
        try:
            with open(ARQUIVO_CONFIG, 'w') as f: json.dump(self.dados, f)
        except: pass

    def get(self, chave): return self.dados.get(chave)
    def set(self, chave, valor): self.dados[chave] = valor; self.salvar()
    def txt(self, chave): return TEXTOS[self.dados.get("idioma", "pt")].get(chave, chave)

config = ConfigManager()

if config.get("fullscreen"):
    janela_real = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
else:
    janela_real = pygame.display.set_mode((LARGURA_ORIGINAL, ALTURA_ORIGINAL), pygame.RESIZABLE)

tela_virtual = pygame.Surface((LARGURA_ORIGINAL, ALTURA_ORIGINAL))
overlay_scanlines = pygame.Surface((LARGURA_ORIGINAL, ALTURA_ORIGINAL), pygame.SRCALPHA)
pygame.display.set_caption("PyPong: Crystal Clear")

def alternar_tela_cheia():
    global janela_real
    novo_estado = not config.get("fullscreen")
    config.set("fullscreen", novo_estado)
    if novo_estado:
        janela_real = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        janela_real = pygame.display.set_mode((LARGURA_ORIGINAL, ALTURA_ORIGINAL), pygame.RESIZABLE)

def gerar_scanlines():
    overlay_scanlines.fill((0,0,0,0))
    for y in range(0, ALTURA_ORIGINAL, 4):
        pygame.draw.line(overlay_scanlines, (0, 0, 0, 20), (0, y), (LARGURA_ORIGINAL, y), 1)

gerar_scanlines()

class DummySound:
    def play(self): pass

try:
    som_intro = pygame.mixer.Sound(os.path.join(DIRETORIO_ATUAL, "intro.wav"))
    som_pop = pygame.mixer.Sound(os.path.join(DIRETORIO_ATUAL, "pop.wav"))
    som_erro = pygame.mixer.Sound(os.path.join(DIRETORIO_ATUAL, "error.wav"))
    som_colisao_parede = pygame.mixer.Sound(os.path.join(DIRETORIO_ATUAL, "popwall.wav"))
    som_pop.set_volume(0.6)
    
    music_path = os.path.join(DIRETORIO_ATUAL, "music.mp3")
    if os.path.exists(music_path):
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(0.4)
        if config.get("musica_ativa"):
            pygame.mixer.music.play(-1) 
except:
    som_intro = som_pop = som_erro = som_colisao_parede = DummySound()

def tocar_som(som):
    if config.get("sfx_ativo"): som.play()

caminho_fonte = os.path.join(DIRETORIO_ATUAL, "Retro Gaming.ttf")
try:
    fonte_titulo = pygame.font.Font(caminho_fonte, 100)
    fonte_menu_grande = pygame.font.Font(caminho_fonte, 40)
    fonte_menu_media = pygame.font.Font(caminho_fonte, 30)
    fonte_menu_pequena = pygame.font.Font(caminho_fonte, 20)
    fonte_placar = pygame.font.Font(caminho_fonte, 80)
    fonte_grande_countdown = pygame.font.Font(caminho_fonte, 150)
except:
    fonte_titulo = pygame.font.SysFont("impact", 100)
    fonte_menu_grande = pygame.font.SysFont("arial", 40)
    fonte_menu_media = pygame.font.SysFont("arial", 30)
    fonte_menu_pequena = pygame.font.SysFont("arial", 20)
    fonte_placar = pygame.font.SysFont("arial", 80)
    fonte_grande_countdown = pygame.font.SysFont("arial", 150)

class Particula:
    def __init__(self, x, y, cor):
        self.x = x; self.y = y; self.cor = cor
        angulo = random.uniform(0, 2 * math.pi)
        velocidade = random.uniform(2, 9)
        self.vx = math.cos(angulo) * velocidade
        self.vy = math.sin(angulo) * velocidade
        self.vida = random.randint(20, 60)
        self.tamanho = random.randint(2, 5)

    def atualizar(self):
        self.x += self.vx; self.y += self.vy
        self.vida -= 1; self.tamanho *= 0.95 

    def desenhar(self, surface):
        if self.vida > 0:
            alpha = min(255, self.vida * 5)
            surf = pygame.Surface((int(self.tamanho)*4, int(self.tamanho)*4), pygame.SRCALPHA)
            pygame.draw.circle(surf, (*self.cor, alpha), (int(self.tamanho)*2, int(self.tamanho)*2), int(self.tamanho))
            surface.blit(surf, (int(self.x) - self.tamanho*2, int(self.y) - self.tamanho*2), special_flags=pygame.BLEND_ADD)

class GerenciadorJogo:
    def __init__(self):
        self.particulas = []
        self.rastro_bola = []
        self.shake_timer = 0
        self.largura_raquete = 20
        self.altura_raquete = 100
        self.tamanho_bola = 15
        self.hue_borda = 0 
        self.bola_pulsar = 0
        self.resetar_round()
        self.pontos_p1 = 0
        self.pontos_p2 = 0
        self.modo_ia = True
        self.teclas = {K_w: False, K_s: False, K_UP: False, K_DOWN: False}

    def resetar_round(self):
        self.pos_p1 = ALTURA_ORIGINAL // 2 - self.altura_raquete // 2
        self.pos_p2 = ALTURA_ORIGINAL // 2 - self.altura_raquete // 2
        self.pos_bola = [LARGURA_ORIGINAL // 2, ALTURA_ORIGINAL // 2]
        self.vel_bola = [7 * random.choice([-1, 1]), 7 * random.choice([-1, 1])]
        self.rastro_bola = []

    def adicionar_particulas(self, x, y, cor=None):
        cor_explosao = cor if cor else random.choice(LISTA_CORES_NEON)
        for _ in range(25): self.particulas.append(Particula(x, y, cor_explosao))

    def aplicar_shake(self): 
        self.shake_timer = 15

    def atualizar_input_mouse(self):
        mx, my = pygame.mouse.get_pos()
        _, h_real = janela_real.get_size()
        escala_y = ALTURA_ORIGINAL / h_real
        self.pos_p1 = (my * escala_y) - (self.altura_raquete / 2)
        self.pos_p1 = max(ESPESSURA_BORDA, min(ALTURA_ORIGINAL - ESPESSURA_BORDA - self.altura_raquete, self.pos_p1))

    def desenhar(self):
        grid_bg.desenhar(tela_virtual)
        ox, oy = 0, 0
        if self.shake_timer > 0:
            ox = random.randint(-6, 6); oy = random.randint(-6, 6)
            self.shake_timer -= 1
        
        cor_borda = pygame.Color(0)
        cor_borda.hsva = (self.hue_borda, 90, 100, 100)
        self.hue_borda = (self.hue_borda + 3) % 360
        
        pygame.draw.rect(tela_virtual, cor_borda, (ox, oy, LARGURA_ORIGINAL, ESPESSURA_BORDA)) 
        pygame.draw.rect(tela_virtual, cor_borda, (ox, ALTURA_ORIGINAL - ESPESSURA_BORDA+oy, LARGURA_ORIGINAL, ESPESSURA_BORDA))
        pygame.draw.line(tela_virtual, cor_borda, (ox, 0), (ox, ALTURA_ORIGINAL), 4)
        pygame.draw.line(tela_virtual, cor_borda, (LARGURA_ORIGINAL+ox-4, 0), (LARGURA_ORIGINAL+ox-4, ALTURA_ORIGINAL), 4)

        for i, pos in enumerate(self.rastro_bola):
            alpha = (i + 1) * 15
            s = pygame.Surface((self.tamanho_bola*2, self.tamanho_bola*2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*NEON_ROSA, alpha), (self.tamanho_bola, self.tamanho_bola), self.tamanho_bola)
            tela_virtual.blit(s, (pos[0]-self.tamanho_bola + ox, pos[1]-self.tamanho_bola + oy))

        self.bola_pulsar += 0.2
        tamanho_extra = math.sin(self.bola_pulsar) * 3
        cor_bola = BRANCO
        pygame.draw.circle(tela_virtual, cor_bola, 
                          (int(self.pos_bola[0] + ox), int(self.pos_bola[1] + oy)), 
                          int(self.tamanho_bola + tamanho_extra))
        
        def desenhar_raquete_glow(x, y, cor):
            s = pygame.Surface((self.largura_raquete + 20, self.altura_raquete + 20), pygame.SRCALPHA)
            pygame.draw.rect(s, (*cor, 100), (0, 0, self.largura_raquete + 20, self.altura_raquete + 20), border_radius=10)
            tela_virtual.blit(s, (x - 10 + ox, y - 10 + oy), special_flags=pygame.BLEND_ADD)
            pygame.draw.rect(tela_virtual, cor, (x + ox, y + oy, self.largura_raquete, self.altura_raquete), border_radius=5)

        desenhar_raquete_glow(20, self.pos_p1, NEON_AZUL)
        desenhar_raquete_glow(LARGURA_ORIGINAL - 40, self.pos_p2, NEON_VERDE)

        txt_p1 = fonte_placar.render(str(self.pontos_p1), True, NEON_AZUL)
        txt_p2 = fonte_placar.render(str(self.pontos_p2), True, NEON_VERDE)
        tela_virtual.blit(txt_p1, (LARGURA_ORIGINAL//4, 40))
        tela_virtual.blit(txt_p2, (LARGURA_ORIGINAL*3//4, 40))

        recorde = config.get("high_score")
        txt_rec = fonte_menu_pequena.render(f"{config.txt('record')}: {recorde}", True, NEON_AMARELO)
        tela_virtual.blit(txt_rec, (LARGURA_ORIGINAL//2 - txt_rec.get_width()//2, ALTURA_ORIGINAL - 30))

        for p in self.particulas: p.desenhar(tela_virtual)
        
        tela_virtual.blit(overlay_scanlines, (0,0))
        
        frame = pygame.transform.scale(tela_virtual, janela_real.get_size())
        janela_real.blit(frame, (0, 0))

    def atualizar(self):
        grid_bg.atualizar() 
        self.atualizar_input_mouse()
        limite_sup, limite_inf = ESPESSURA_BORDA, ALTURA_ORIGINAL - ESPESSURA_BORDA - self.altura_raquete

        if self.teclas[K_w]: self.pos_p1 -= 8
        if self.teclas[K_s]: self.pos_p1 += 8
        self.pos_p1 = max(limite_sup, min(limite_inf, self.pos_p1))

        self.particulas = [p for p in self.particulas if p.vida > 0]
        for p in self.particulas: p.atualizar()

        self.rastro_bola.append(list(self.pos_bola))
        if len(self.rastro_bola) > 6: self.rastro_bola.pop(0)

        if not self.modo_ia:
            if self.teclas[K_UP]: self.pos_p2 -= 8
            if self.teclas[K_DOWN]: self.pos_p2 += 8
        else:
            centro = self.pos_p2 + self.altura_raquete // 2
            if random.random() > 0.1: 
                if centro < self.pos_bola[1] - 15: self.pos_p2 += 7
                elif centro > self.pos_bola[1] + 15: self.pos_p2 -= 7
        self.pos_p2 = max(limite_sup, min(limite_inf, self.pos_p2))

        self.pos_bola[0] += self.vel_bola[0]; self.pos_bola[1] += self.vel_bola[1]
        
        if self.pos_bola[1] <= ESPESSURA_BORDA + self.tamanho_bola:
            self.pos_bola[1] = ESPESSURA_BORDA + self.tamanho_bola + 1
            self.vel_bola[1] *= -1
            tocar_som(som_colisao_parede)
            self.adicionar_particulas(self.pos_bola[0], self.pos_bola[1])
            
        elif self.pos_bola[1] >= ALTURA_ORIGINAL - ESPESSURA_BORDA - self.tamanho_bola:
            self.pos_bola[1] = ALTURA_ORIGINAL - ESPESSURA_BORDA - self.tamanho_bola - 1
            self.vel_bola[1] *= -1
            tocar_som(som_colisao_parede)
            self.adicionar_particulas(self.pos_bola[0], self.pos_bola[1])

        col_p1 = (self.pos_bola[0] < 40 + self.tamanho_bola and self.pos_p1 < self.pos_bola[1] < self.pos_p1 + self.altura_raquete)
        col_p2 = (self.pos_bola[0] > LARGURA_ORIGINAL - 40 - self.tamanho_bola and self.pos_p2 < self.pos_bola[1] < self.pos_p2 + self.altura_raquete)

        if col_p1:
            self.vel_bola[0] = abs(self.vel_bola[0]) * 1.05
            self.vel_bola[1] = ((self.pos_bola[1] - (self.pos_p1 + self.altura_raquete/2)) / (self.altura_raquete/2)) * 12
            tocar_som(som_pop); self.adicionar_particulas(self.pos_bola[0], self.pos_bola[1], NEON_AZUL); self.aplicar_shake()
        
        if col_p2:
            self.vel_bola[0] = -abs(self.vel_bola[0]) * 1.05
            self.vel_bola[1] = ((self.pos_bola[1] - (self.pos_p2 + self.altura_raquete/2)) / (self.altura_raquete/2)) * 12
            tocar_som(som_pop); self.adicionar_particulas(self.pos_bola[0], self.pos_bola[1], NEON_VERDE); self.aplicar_shake()

        if self.pos_bola[0] < 0:
            self.pontos_p2 += 1; tocar_som(som_erro); self.resetar_round()
        elif self.pos_bola[0] > LARGURA_ORIGINAL:
            self.pontos_p1 += 1; tocar_som(som_intro); self.resetar_round()
            if self.pontos_p1 > config.get("high_score") and self.modo_ia: config.set("high_score", self.pontos_p1)

        return self.pontos_p1 >= PONTUACAO_MAXIMA or self.pontos_p2 >= PONTUACAO_MAXIMA

class RetroGrid:
    def __init__(self):
        self.offset_y = 0
        self.velocidade = 2
        # Apenas linhas simples agora
        self.linhas_v = []
        for x in range(-LARGURA_ORIGINAL, LARGURA_ORIGINAL * 2, 150): # Mais espaçado
            self.linhas_v.append(x)

    def atualizar(self):
        self.offset_y += self.velocidade
        if self.offset_y >= 60: self.offset_y = 0

    def desenhar(self, surface):
        horizonte_y = ALTURA_ORIGINAL // 2
        
        # Fundo do céu (Simples)
        pygame.draw.rect(surface, (5, 0, 15), (0, 0, LARGURA_ORIGINAL, horizonte_y))
        
        # Fundo do chão (Escuro para contraste)
        pygame.draw.rect(surface, (10, 0, 20), (0, horizonte_y, LARGURA_ORIGINAL, ALTURA_ORIGINAL))

        centro_x = LARGURA_ORIGINAL // 2
        centro_y = horizonte_y
        
        # Linhas Verticais (Perspectiva Limpa)
        for x_base in self.linhas_v:
            # Desenhando com opacidade baixa fake (cor mais escura)
            pygame.draw.line(surface, CINZA_GRID, (centro_x, centro_y), (x_base, ALTURA_ORIGINAL), 2)

        # Linhas Horizontais (Movimento)
        for i in range(8): # Menos linhas
            # Espaçamento mais suave
            dist = (i * 60 + self.offset_y)
            y_pos = horizonte_y + int(dist ** 1.1) 
            
            if y_pos < ALTURA_ORIGINAL and y_pos > horizonte_y:
                pygame.draw.line(surface, CINZA_GRID, (0, y_pos), (LARGURA_ORIGINAL, y_pos), 2)

        # Linha do Horizonte Brilhante
        pygame.draw.line(surface, NEON_ROSA, (0, horizonte_y), (LARGURA_ORIGINAL, horizonte_y), 2)

grid_bg = RetroGrid()

def desenhar_botao(texto, x, y, w, h, ativo):
    cor = NEON_AZUL if ativo else (30, 30, 40)
    cor_txt = BRANCO if ativo else (180, 180, 180)
    pygame.draw.rect(tela_virtual, cor, (x, y, w, h), border_radius=10)
    if ativo: 
        pygame.draw.rect(tela_virtual, (255, 255, 255), (x, y, w, h), 2, border_radius=10)

    fonte = fonte_menu_grande
    surf = fonte.render(texto, True, cor_txt)
    if surf.get_width() > w - 20:
        fonte = fonte_menu_media
        surf = fonte.render(texto, True, cor_txt)
        if surf.get_width() > w - 20:
            fonte = fonte_menu_pequena
            surf = fonte.render(texto, True, cor_txt)

    tela_virtual.blit(surf, (x + (w - surf.get_width()) // 2, y + (h - surf.get_height()) // 2))
    return pygame.Rect(x, y, w, h)

def obter_mouse_virtual():
    mx, my = pygame.mouse.get_pos()
    w_real, h_real = janela_real.get_size()
    return mx * (LARGURA_ORIGINAL / w_real), my * (ALTURA_ORIGINAL / h_real)

def contagem_regressiva(jogo):
    for i in range(3, 0, -1):
        tela_virtual.fill(COR_FUNDO)
        grid_bg.desenhar(tela_virtual)
        jogo.desenhar()
        txt = fonte_grande_countdown.render(str(i), True, NEON_ROSA)
        tela_virtual.blit(txt, (LARGURA_ORIGINAL//2 - txt.get_width()//2, ALTURA_ORIGINAL//2 - txt.get_height()//2))
        frame = pygame.transform.scale(tela_virtual, janela_real.get_size())
        janela_real.blit(frame, (0, 0))
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == QUIT: pygame.quit(); sys.exit()
            if event.type == KEYDOWN and event.key == K_F11: alternar_tela_cheia()

        tocar_som(som_colisao_parede)
        pygame.time.wait(800)

    jogo.desenhar()
    txt = fonte_grande_countdown.render(config.txt("go"), True, NEON_VERDE)
    tela_virtual.blit(txt, (LARGURA_ORIGINAL//2 - txt.get_width()//2, ALTURA_ORIGINAL//2 - txt.get_height()//2))
    frame = pygame.transform.scale(tela_virtual, janela_real.get_size())
    janela_real.blit(frame, (0, 0))
    pygame.display.flip()
    tocar_som(som_pop)
    pygame.time.wait(500)

def menu_opcoes():
    global janela_real
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(True)
    L_BTN, X_BTN = 400, LARGURA_ORIGINAL//2 - 200

    while True:
        clock.tick(60)
        grid_bg.atualizar()
        tela_virtual.fill(COR_FUNDO)
        grid_bg.desenhar(tela_virtual)
        vmx, vmy = obter_mouse_virtual()

        tit = fonte_menu_grande.render(config.txt("options"), True, BRANCO)
        tela_virtual.blit(tit, (LARGURA_ORIGINAL//2 - tit.get_width()//2, 40))

        click = False
        for event in pygame.event.get():
            if event.type == QUIT: pygame.quit(); sys.exit()
            if event.type == MOUSEBUTTONDOWN and event.button == 1: click = True
            if event.type == KEYDOWN and event.key == K_F11: alternar_tela_cheia()

        txt_sfx = config.txt("sfx_on") if config.get("sfx_ativo") else config.txt("sfx_off")
        if desenhar_botao(txt_sfx, X_BTN, 110, L_BTN, 60, X_BTN < vmx < X_BTN + L_BTN and 110 < vmy < 170).collidepoint((vmx, vmy)) and click:
            config.set("sfx_ativo", not config.get("sfx_ativo"))

        txt_music = config.txt("music_on") if config.get("musica_ativa") else config.txt("music_off")
        if desenhar_botao(txt_music, X_BTN, 180, L_BTN, 60, X_BTN < vmx < X_BTN + L_BTN and 180 < vmy < 240).collidepoint((vmx, vmy)) and click:
            novo_estado = not config.get("musica_ativa")
            config.set("musica_ativa", novo_estado)
            if novo_estado: pygame.mixer.music.play(-1)
            else: pygame.mixer.music.stop()

        txt_full = config.txt("screen_full") if config.get("fullscreen") else config.txt("screen_win")
        if desenhar_botao(txt_full, X_BTN, 250, L_BTN, 60, X_BTN < vmx < X_BTN + L_BTN and 250 < vmy < 310).collidepoint((vmx, vmy)) and click:
            alternar_tela_cheia()

        if desenhar_botao(NOMES_IDIOMAS[config.get("idioma")], X_BTN, 320, L_BTN, 60, X_BTN < vmx < X_BTN + L_BTN and 320 < vmy < 380).collidepoint((vmx, vmy)) and click:
            idx = IDIOMAS.index(config.get("idioma")); config.set("idioma", IDIOMAS[(idx + 1) % len(IDIOMAS)])

        if desenhar_botao(config.txt("back"), X_BTN, 450, L_BTN, 60, X_BTN < vmx < X_BTN + L_BTN and 450 < vmy < 510).collidepoint((vmx, vmy)) and click: return

        frame = pygame.transform.scale(tela_virtual, janela_real.get_size())
        janela_real.blit(frame, (0, 0))
        pygame.display.flip()

def menu_principal(jogo):
    global janela_real
    clock = pygame.time.Clock()
    anim_y = 0; dir_anim = 0.5
    pygame.mouse.set_visible(True)
    L_BTN, X_BTN = 400, LARGURA_ORIGINAL//2 - 200

    while True:
        clock.tick(60)
        grid_bg.atualizar()
        tela_virtual.fill(COR_FUNDO)
        grid_bg.desenhar(tela_virtual)
        vmx, vmy = obter_mouse_virtual()
        
        anim_y += dir_anim
        if abs(anim_y) > 8: dir_anim *= -1
        
        tit = fonte_titulo.render("PyPong 2077", True, NEON_ROSA)
        sombra = fonte_titulo.render("PyPong 2077", True, NEON_AZUL)
        tela_virtual.blit(sombra, (LARGURA_ORIGINAL//2 - tit.get_width()//2 + 4, 80 + anim_y + 4))
        tela_virtual.blit(tit, (LARGURA_ORIGINAL//2 - tit.get_width()//2, 80 + anim_y))

        click = False
        for event in pygame.event.get():
            if event.type == QUIT: pygame.quit(); sys.exit()
            if event.type == MOUSEBUTTONDOWN and event.button == 1: click = True
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: pygame.quit(); sys.exit()
                if event.key == K_F11: alternar_tela_cheia()

        if desenhar_botao(config.txt("vs_ia"), X_BTN, 250, L_BTN, 60, X_BTN < vmx < X_BTN + L_BTN and 250 < vmy < 310).collidepoint((vmx, vmy)) and click: return True
        if desenhar_botao(config.txt("vs_player"), X_BTN, 330, L_BTN, 60, X_BTN < vmx < X_BTN + L_BTN and 330 < vmy < 390).collidepoint((vmx, vmy)) and click: return False
        if desenhar_botao(config.txt("options"), X_BTN, 410, L_BTN, 60, X_BTN < vmx < X_BTN + L_BTN and 410 < vmy < 470).collidepoint((vmx, vmy)) and click: menu_opcoes()
        if desenhar_botao(config.txt("exit"), X_BTN, 490, L_BTN, 60, X_BTN < vmx < X_BTN + L_BTN and 490 < vmy < 550).collidepoint((vmx, vmy)) and click: pygame.quit(); sys.exit()

        rodape = fonte_menu_pequena.render(config.txt("footer"), True, (100, 100, 120))
        tela_virtual.blit(rodape, (LARGURA_ORIGINAL//2 - rodape.get_width()//2, ALTURA_ORIGINAL - 30))

        frame = pygame.transform.scale(tela_virtual, janela_real.get_size())
        janela_real.blit(frame, (0, 0))
        pygame.display.flip()

def tela_vencedor(vencedor_texto, cor):
    tela_virtual.fill(COR_FUNDO)
    grid_bg.desenhar(tela_virtual)
    txt = fonte_placar.render(vencedor_texto, True, cor)
    sub = fonte_menu_grande.render(config.txt("click_back"), True, BRANCO)
    tela_virtual.blit(txt, (LARGURA_ORIGINAL//2 - txt.get_width()//2, ALTURA_ORIGINAL//2 - 50))
    tela_virtual.blit(sub, (LARGURA_ORIGINAL//2 - sub.get_width()//2, ALTURA_ORIGINAL//2 + 50))
    
    frame = pygame.transform.scale(tela_virtual, janela_real.get_size())
    janela_real.blit(frame, (0, 0))
    pygame.display.flip()
    pygame.mouse.set_visible(True)
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT: pygame.quit(); sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_F11: alternar_tela_cheia()
                else: return
            if event.type == MOUSEBUTTONDOWN: return

def main():
    global janela_real
    jogo = GerenciadorJogo()
    while True:
        jogo.modo_ia = menu_principal(jogo)
        jogo.pontos_p1 = 0; jogo.pontos_p2 = 0; jogo.resetar_round()
        
        contagem_regressiva(jogo)
        
        # PRENDE O MOUSE AO COMEÇAR O JOGO
        pygame.event.set_grab(True)
        
        rodando = True
        clock = pygame.time.Clock()
        pygame.mouse.set_visible(False) 

        while rodando:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == QUIT: pygame.quit(); sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE: 
                        pygame.event.set_grab(False) # SOLTA O MOUSE
                        rodando = False 
                    if event.key == K_F11: alternar_tela_cheia()
                    if event.key in jogo.teclas: jogo.teclas[event.key] = True
                if event.type == KEYUP:
                    if event.key in jogo.teclas: jogo.teclas[event.key] = False
            
            if jogo.atualizar(): rodando = False
            jogo.desenhar()
            pygame.display.flip()
        
        # SOLTA O MOUSE SE ACABAR A PARTIDA
        pygame.event.set_grab(False)
        
        if jogo.pontos_p1 >= PONTUACAO_MAXIMA: tela_vencedor(config.txt("win_p1"), NEON_AZUL)
        elif jogo.pontos_p2 >= PONTUACAO_MAXIMA: tela_vencedor(config.txt("win_cpu") if jogo.modo_ia else config.txt("win_p2"), NEON_VERDE)

if __name__ == "__main__":
    main()