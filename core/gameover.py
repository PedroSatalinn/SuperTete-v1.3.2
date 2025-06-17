# core/gameover.py

import pygame

def desenhar_gameover(tela, personagem, largura, altura):
    gameover_path = "assets/images/tetegameover.png" if personagem == "tete" else "assets/images/lilicegameover.png"
    gameover_img = pygame.image.load(gameover_path)
    gameover_img = pygame.transform.scale(gameover_img, (largura, altura))
    tela.blit(gameover_img, (0, 0))
