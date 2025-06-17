# core/menu.py
import pygame
import sys
from .config import TELA_LARGURA, TELA_ALTURA, COR_BOTAO, COR_BOTAO_HOVER, ESTADO_JOGANDO, ESTADO_SAIR

class TelaMenu:
    def __init__(self, tela, assets):
        """
        Construtor da classe TelaMenu.
        Inicializa todos os recursos necessários para o menu.
        """
        self.tela = tela
        self.assets = assets
        self.menu_imagem = self.assets['menu_imagem']
        self.selecao_imagem = self.assets['selecao_imagem']
        
        # Estado interno para controlar se estamos no menu principal ou na seleção
        self.etapa = 'principal'  # Pode ser 'principal' ou 'selecao'

        # Recursos para o menu principal
        self.fonte = pygame.font.Font(None, 48)
        self.texto_jogar = self.fonte.render("Jogar", True, (255, 255, 255))
        self.texto_sair = self.fonte.render("Sair", True, (255, 255, 255))
        self.jogar_btn_rect = pygame.Rect(TELA_LARGURA / 2 - 125, TELA_ALTURA / 2, 250, 60)
        self.sair_btn_rect = pygame.Rect(TELA_LARGURA / 2 - 125, TELA_ALTURA / 2 + 100, 250, 60)

        # Recursos para a seleção de personagem (retângulos clicáveis)
        self.tete_rect = pygame.Rect(0, 0, TELA_LARGURA / 2, TELA_ALTURA)
        self.lilice_rect = pygame.Rect(TELA_LARGURA / 2, 0, TELA_LARGURA / 2, TELA_ALTURA)

    def _desenhar_menu_principal(self):
        """Desenha a tela com os botões 'Jogar' e 'Sair'."""
        self.tela.blit(self.menu_imagem, (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        # Desenha botão Jogar
        cor_jogar = COR_BOTAO_HOVER if self.jogar_btn_rect.collidepoint(mouse_pos) else COR_BOTAO
        pygame.draw.rect(self.tela, cor_jogar, self.jogar_btn_rect, border_radius=15)
        pos_texto_jogar = self.texto_jogar.get_rect(center=self.jogar_btn_rect.center)
        self.tela.blit(self.texto_jogar, pos_texto_jogar)

        # Desenha botão Sair
        cor_sair = COR_BOTAO_HOVER if self.sair_btn_rect.collidepoint(mouse_pos) else COR_BOTAO
        pygame.draw.rect(self.tela, cor_sair, self.sair_btn_rect, border_radius=15)
        pos_texto_sair = self.texto_sair.get_rect(center=self.sair_btn_rect.center)
        self.tela.blit(self.texto_sair, pos_texto_sair)

    def _desenhar_selecao_personagem(self):
        """Desenha a tela de seleção de personagem."""
        self.tela.blit(self.selecao_imagem, (0, 0))

    def rodar(self):
        """
        Roda o loop principal do menu. Gerencia eventos e desenho.
        Retorna uma tupla: (PROXIMO_ESTADO, personagem_escolhido).
        """
        pygame.mixer.music.load("assets/sounds/musicamenu.mp3")
        pygame.mixer.music.play(-1)

        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    return (ESTADO_SAIR, None) # Retorna o estado SAIR e nenhum personagem

                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if self.etapa == 'principal':
                        if self.jogar_btn_rect.collidepoint(evento.pos):
                            # Se clicou em "Jogar", muda para a etapa de seleção
                            self.etapa = 'selecao'
                        elif self.sair_btn_rect.collidepoint(evento.pos):
                            pygame.mixer.music.stop()
                            return (ESTADO_SAIR, None)
                    
                    elif self.etapa == 'selecao':
                        personagem = None
                        if self.tete_rect.collidepoint(evento.pos):
                            personagem = 'tete'
                        elif self.lilice_rect.collidepoint(evento.pos):
                            personagem = 'lilice'
                        
                        if personagem:
                            pygame.mixer.music.stop()
                            # Retorna o estado JOGANDO e o nome do personagem escolhido
                            return (ESTADO_JOGANDO, personagem)

            # Lógica de desenho baseada na etapa atual
            if self.etapa == 'principal':
                self._desenhar_menu_principal()
            elif self.etapa == 'selecao':
                self._desenhar_selecao_personagem()
            
            pygame.display.flip()