# main.py
import pygame
import sys

from core.config import TELA_LARGURA, TELA_ALTURA, ESTADO_MENU, ESTADO_JOGANDO, ESTADO_GAMEOVER, ESTADO_SAIR
from core.assets import carregar_assets
from core.menu import TelaMenu
from core.game import TelaJogo
# from core.gameover import TelaGameOver # Futuramente, a tela de GameOver também pode virar uma classe

def main():
    """
    Função principal do jogo.
    Inicializa o Pygame e gerencia a máquina de estados (menu, jogo, etc.).
    """
    # --- Inicialização ---
    pygame.init()
    pygame.mixer.init()
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    pygame.display.set_caption("Super Tetê")
    
    # --- Carregamento de Assets ---
    # Carrega todos os assets compartilhados de uma única vez no início
    assets = carregar_assets()

    # --- Máquina de Estados ---
    estado_atual = ESTADO_MENU
    personagem_escolhido = None
    
    rodando = True
    while rodando:
        
        # --- Gerenciador de Telas (Estados) ---
        if estado_atual == ESTADO_MENU:
            # Cria e roda a tela de menu
            tela_menu = TelaMenu(tela, assets) 
            proximo_estado, personagem_selecionado = tela_menu.rodar()
            
            # Atualiza o estado e guarda a escolha do personagem
            estado_atual = proximo_estado
            if personagem_selecionado:
                personagem_escolhido = personagem_selecionado

        elif estado_atual == ESTADO_JOGANDO:
            # Garante que um personagem foi escolhido antes de iniciar o jogo
            if not personagem_escolhido:
                print("Erro: Nenhum personagem selecionado. Voltando ao menu.")
                estado_atual = ESTADO_MENU
                continue

            # Cria e roda a tela de jogo
            tela_jogo = TelaJogo(tela, assets, personagem_escolhido)
            proximo_estado = tela_jogo.rodar()
            
            # Atualiza o estado para o que o jogo retornou (MENU ou SAIR)
            estado_atual = proximo_estado

        elif estado_atual == ESTADO_GAMEOVER:
            # Futuramente, aqui você pode rodar a classe TelaGameOver
            print("Estado GameOver não implementado como classe. Voltando ao menu.")
            estado_atual = ESTADO_MENU
        
        elif estado_atual == ESTADO_SAIR:
            # Quebra o loop principal para encerrar o jogo
            rodando = False

    # --- Encerramento ---
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()