# core/hud.py

import pygame
from core.config import tamanho_coracao

def desenhar_HUD(tela, vidas, life, personagem, icones, imagens_coracao):
    icone = icones[personagem]
    tela.blit(icone, (20, 20))
    fonte_hud = pygame.font.Font(None, 36)
    tela.blit(fonte_hud.render(f"x {vidas}", True, (255, 255, 255)), (95, 40))
    for i in range(life):
        frame = int(pygame.time.get_ticks() / 150) % len(imagens_coracao)
        tela.blit(imagens_coracao[frame], (20 + i * (tamanho_coracao[0] + 5), 95))
