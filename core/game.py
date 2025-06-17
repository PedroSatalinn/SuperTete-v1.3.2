# core/game.py
import pygame
import sys
import random

from .config import (TELA_LARGURA, TELA_ALTURA, vidas_maximas, life_maximo, 
                     ESTADO_GAMEOVER, ESTADO_SAIR, ESTADO_MENU)
from .hud import desenhar_HUD
from .gameover import desenhar_gameover
from .assets import carregar_assets_personagem

class TelaJogo:
    def __init__(self, tela, assets, personagem_escolhido):
        """
        Construtor da classe TelaJogo.
        Inicializa todos os recursos e variáveis para a fase.
        """
        # --- Configuração básica ---
        self.tela = tela
        self.assets_gerais = assets
        self.personagem_escolhido = personagem_escolhido
        self.clock = pygame.time.Clock()
        self.fonte = pygame.font.Font(None, 36)

        # --- Carrega assets específicos da fase e do personagem ---
        self.assets_personagem = carregar_assets_personagem(self.personagem_escolhido)
        self.imagens_andar, self.imagem_pulo, self.imagem_parado = self.assets_personagem
        
        # Recupera assets gerais que foram pré-carregados
        self.cenario = self.assets_gerais['cenario']
        self.bloco_imagem = self.assets_gerais['bloco_imagem']
        self.missel_imagem = self.assets_gerais['missel_imagem']
        self.som_pulo = self.assets_gerais['som_pulo']
        self.icones = self.assets_gerais['icones']
        self.imagens_coracao = self.assets_gerais['imagens_coracao']
        self.plataformas = self.assets_gerais['plataformas']

        # --- Inicialização do estado do jogo ---
        self.player_rect = pygame.Rect(0, 0, 70, 90) # Posição inicial será definida em _reiniciar_jogador
        self.misseis = []
        for i in range(10):
            pos_x = random.randint(TELA_LARGURA, 10000)
            pos_y = random.randint(100, TELA_ALTURA - 200)
            missel_rect = pygame.Rect(pos_x, pos_y, 70, 70) # Rect da imagem
            missel_hitbox = pygame.Rect(pos_x, pos_y, 40, 25) # Hitbox menor
            self.misseis.append({'rect': missel_rect, 'hitbox': missel_hitbox})

        self.checkpoint = self.plataformas[0]

        # --- Variáveis de estado ---
        self.personagem_velocidade_x = 10
        self.personagem_velocidade_y = 0
        self.gravidade = 2 * (TELA_ALTURA / 600)
        self.camera_x = 0
        self.vidas = vidas_maximas
        self.life = life_maximo
        self.no_chao = False
        self.movimento = False
        self.morreu = False
        self.pause = False
        self.direcao = "direita"
        self.ultimo_x_respawn_missel = self.camera_x + TELA_LARGURA
        
        self._reiniciar_jogador(primeira_vez=True)

    def _reiniciar_jogador(self, primeira_vez=False):
        self.player_rect.x = self.checkpoint["x"] + 10
        self.player_rect.y = self.checkpoint["y"] - self.player_rect.height
        self.personagem_velocidade_y = 0
        self.camera_x = self.player_rect.x - TELA_LARGURA // 4
        self.morreu = False
        self.life = life_maximo
        if not primeira_vez:
            self.vidas -= 1

    def _processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return ESTADO_SAIR
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and self.no_chao and not self.pause:
                    self.personagem_velocidade_y = -20 * (TELA_ALTURA / 600)
                    self.som_pulo.play()
                if evento.key == pygame.K_ESCAPE:
                    self.pause = not self.pause
                if evento.key == pygame.K_r and self.morreu and self.vidas > 0:
                    self._reiniciar_jogador()
        return None # Nenhum evento especial, continua no estado atual

    def _atualizar_logica(self):
        if self.pause or self.morreu:
            return

        # Movimento e física do jogador
        teclas = pygame.key.get_pressed()
        self.movimento = False
        if teclas[pygame.K_a]:
            self.player_rect.x -= self.personagem_velocidade_x
            self.direcao = "esquerda"
            self.movimento = True
        if teclas[pygame.K_d]:
            self.player_rect.x += self.personagem_velocidade_x
            self.direcao = "direita"
            self.movimento = True

        self.camera_x = max(self.player_rect.x - TELA_LARGURA // 2, 0)
        self.player_rect.x = max(0, self.player_rect.x)
        self.personagem_velocidade_y += self.gravidade
        self.player_rect.y += self.personagem_velocidade_y
        self.no_chao = False

        # Colisão do jogador com plataformas
        for plataforma in self.plataformas:
            rect_plataforma = pygame.Rect(plataforma["x"], plataforma["y"], plataforma["width"], plataforma["height"])
            if self.player_rect.colliderect(rect_plataforma) and self.personagem_velocidade_y > 0:
                # --- MUDANÇA 3: Ajuste para o "pé não afundar" ---
                self.player_rect.bottom = rect_plataforma.top + 1 # O "+1" evita que a imagem afunde
                self.personagem_velocidade_y = 0
                self.no_chao = True
        
        if self.player_rect.y > TELA_ALTURA + 200:
            if self.vidas > 1: self._reiniciar_jogador()
            else: self.morreu = True; self.vidas = 0

        # Lógica dos Mísseis
        for missel in self.misseis:
            # Movimenta o rect da imagem
            missel['rect'].x -= 8
            # Sincroniza a hitbox para ficar no centro do rect da imagem
            missel['hitbox'].center = missel['rect'].center

            # --- MUDANÇA 4: Colisão usa a hitbox do míssel ---
            if self.player_rect.colliderect(missel['hitbox']):
                self.life -= 1
                missel['rect'].x = self.camera_x + TELA_LARGURA + 5000 
            
            if missel['rect'].right < self.camera_x:
                distancia_minima = 400
                distancia_extra = random.randint(100, 500)
                missel['rect'].x = self.ultimo_x_respawn_missel + distancia_minima + distancia_extra
                missel['rect'].y = random.randint(100, TELA_ALTURA - 200)
                self.ultimo_x_respawn_missel = missel['rect'].x

        if self.life <= 0:
            if self.vidas > 1: self._reiniciar_jogador()
            else: self.morreu = True; self.vidas = 0

    def _desenhar(self):
        self.tela.fill((0, 0, 0))
        largura_cenario = self.cenario.get_width()
        for i in range((TELA_LARGURA // largura_cenario) + 2):
            self.tela.blit(self.cenario, (i * largura_cenario - (self.camera_x / 2) % largura_cenario, 0))

        for plataforma in self.plataformas:
            rect = pygame.Rect(plataforma["x"] - self.camera_x, plataforma["y"], plataforma["width"], plataforma["height"])
            x_bloco = rect.x
            while x_bloco < rect.x + rect.width:
                self.tela.blit(self.bloco_imagem, (x_bloco, rect.y))
                x_bloco += self.bloco_imagem.get_width()

        # Desenho do jogador
        if not self.morreu:
            img_atual = self.imagem_pulo if not self.no_chao else (
                self.imagens_andar[int(pygame.time.get_ticks() / 150) % len(self.imagens_andar)] if self.movimento else self.imagem_parado)
            if self.direcao == "esquerda":
                img_atual = pygame.transform.flip(img_atual, True, False)
            self.tela.blit(img_atual, (self.player_rect.x - self.camera_x, self.player_rect.y))

        # Desenho dos mísseis
        for missel in self.misseis:
            self.tela.blit(self.missel_imagem, (missel['rect'].x - self.camera_x, missel['rect'].y))

        # HUD e telas de Game Over/Pause
        if self.morreu and self.vidas <= 0:
            desenhar_gameover(self.tela, self.personagem_escolhido, TELA_LARGURA, TELA_ALTURA)
        else:
            desenhar_HUD(self.tela, self.vidas, self.life, self.personagem_escolhido, self.icones, self.imagens_coracao)
        if self.pause:
            sombra = pygame.Surface((TELA_LARGURA, TELA_ALTURA))
            sombra.set_alpha(150)
            sombra.fill((0, 0, 0))
            self.tela.blit(sombra, (0,0))
            texto_pause = self.fonte.render("Pausado (ESC para continuar)", True, (255, 255, 255))
            pos_texto = texto_pause.get_rect(center=(TELA_LARGURA/2, TELA_ALTURA/2))
            self.tela.blit(texto_pause, pos_texto)

        pygame.display.flip()

    def rodar(self):
        """O loop principal da fase. Retorna o próximo estado do jogo."""
        pygame.mixer.music.stop()
        pygame.mixer.music.load("assets/sounds/musicafase1.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        
        tempo_gameover = 0

        while True:
            proximo_estado = self._processar_eventos()
            if proximo_estado: return proximo_estado

            self._atualizar_logica()
            self._desenhar()

            # Se o jogador morreu de vez, espera um pouco e vai para a tela de menu
            if self.morreu and self.vidas <= 0:
                if tempo_gameover == 0:
                    tempo_gameover = pygame.time.get_ticks()
                if pygame.time.get_ticks() - tempo_gameover > 4000: # Espera 4 segundos
                    return ESTADO_MENU

            self.clock.tick(60)