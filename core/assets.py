# core/assets.py
import pygame
import os
from .config import TELA_LARGURA, TELA_ALTURA, tamanho_icone, tamanho_coracao

def carregar_assets():
    """
    Carrega todos os assets compartilhados do jogo de uma só vez.
    Retorna um dicionário com todos os recursos para fácil acesso.
    """
    assets = {}
    
    # Carregamento de imagens
    assets['menu_imagem'] = pygame.transform.scale(pygame.image.load('assets/images/imagemmenu.png').convert(), (TELA_LARGURA, TELA_ALTURA))
    assets['selecao_imagem'] = pygame.transform.scale(pygame.image.load('assets/images/selecao_personagem.png').convert(), (TELA_LARGURA, TELA_ALTURA))
    assets['bloco_imagem'] = pygame.transform.scale(pygame.image.load('assets/images/bloco.png').convert_alpha(), (40, 40))
    assets['cenario'] = pygame.transform.scale(pygame.image.load('assets/images/cenariofase1.png').convert(), (3000, TELA_ALTURA))
    assets['missel_imagem'] = pygame.transform.scale(pygame.image.load('assets/images/missil.png').convert_alpha(), (70, 70))
    
    # Carregamento de sons
    assets['som_pulo'] = pygame.mixer.Sound('assets/sounds/sompulo.mp3')
    
    # Dados do jogo
    assets['plataformas'] = [{"x": i * 200, "y": 550 - (i % 5) * 50, "width": 100, "height": 40} for i in range(50)]
    
    # Recursos do HUD
    assets['icones'] = {
        "tete": pygame.transform.scale(pygame.image.load("assets/images/tete_icone.png").convert_alpha(), tamanho_icone),
        "lilice": pygame.transform.scale(pygame.image.load("assets/images/lilice_icone.png").convert_alpha(), tamanho_icone)
    }
    assets['imagens_coracao'] = [
        pygame.transform.scale(pygame.image.load(f"assets/images/coracao{i}.png").convert_alpha(), tamanho_coracao)
        for i in range(1, 6)
    ]
    
    return assets

def carregar_assets_personagem(nome):
    """Carrega os assets específicos de um personagem."""
    # O tamanho precisa ser o mesmo para todos os frames para o Rect não ficar errado
    tamanho_personagem = (70, 90) 
    
    imagens_andar = []
    for i in range(4): # 4 frames de animação
        img = pygame.image.load(f'assets/images/{nome}_frame{i}.png').convert_alpha()
        imagens_andar.append(pygame.transform.scale(img, tamanho_personagem))
        
    imagem_pulo = pygame.image.load(f'assets/images/{nome}_frame_pulo.png').convert_alpha()
    imagem_pulo = pygame.transform.scale(imagem_pulo, tamanho_personagem)
    
    imagem_parado = pygame.image.load(f'assets/images/{nome}_frame_parado.png').convert_alpha()
    imagem_parado = pygame.transform.scale(imagem_parado, tamanho_personagem)
    
    return imagens_andar, imagem_pulo, imagem_parado