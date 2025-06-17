# SuperTetê v1.3.2
Essa versão é a mesma da 1.3 e 1.3.1, mas com a principal mudança que é um novo refatoramento que touxe SUPER MELHORIAS de desempenho, estética e jogabilidade.

Super Tetê 🎮
Um vibrante jogo de plataforma 2D em pixel art, desenvolvido em Python com a biblioteca Pygame-CE. Acompanhe Tetê e Lilice em uma aventura cheia de desafios, pulos precisos e mísseis a serem desviados!

🚀 Sobre o Jogo
Super Tetê é um projeto criado para estudo e aprimoramento de técnicas de desenvolvimento de jogos. O foco principal foi a criação de uma arquitetura de software limpa e escalável, separando a lógica do jogo, os assets e as configurações em módulos distintos.

🏛️ Estrutura do Projeto
O código foi refatorado para seguir uma arquitetura baseada em estados, onde cada tela do jogo (Menu, Jogo, Game Over) é uma classe autocontida, gerenciada por um "maestro" principal (main.py).

SuperTete/
├── assets/            # Contém todos os recursos visuais e sonoros
│   ├── images/        # Imagens, sprites, cenários
│   └── sounds/        # Músicas e efeitos sonoros
│
├── core/              # Código-fonte principal do jogo
│   ├── __init__.py    # Permite que 'core' seja um módulo Python
│   ├── assets.py      # Funções para carregar e gerenciar assets
│   ├── config.py      # Constantes e configurações globais (tamanho da tela, FPS)
│   ├── game.py        # Classe e lógica da tela principal do jogo (gameplay)
│   ├── gameover.py    # Lógica da tela de Game Over
│   ├── hud.py         # Lógica do Heads-Up Display (vidas, score)
│   └── menu.py        # Classe e lógica da tela de Menu
│
├── main.py            # Ponto de entrada do jogo (o "Maestro" que gerencia os estados)
└── README.md          # Este arquivo de documentação
🛠️ Como Rodar
Para executar o projeto em sua máquina local, siga os passos abaixo.

1. Pré-requisitos:

Ter o Python 3 instalado.
2. Clone o Repositório:

Bash

git clone https://github.com/PedroSatalinn/SuperTete-v1.3.2.git
cd SuperTete

3. Instale as Dependências:
O projeto depende apenas da biblioteca pygame-ce. Você pode instalá-la com o pip:

Bash

pip install pygame-ce
(Dica profissional: Você pode criar um arquivo requirements.txt com o comando pip freeze > requirements.txt para que outras pessoas possam instalar tudo com pip install -r requirements.txt)

4. Execute o Jogo:
Na pasta raiz do projeto, rode o seguinte comando no seu terminal:

Bash

python main.py
💻 Tecnologias Utilizadas
Linguagem: Python 3
Biblioteca: Pygame Community Edition (Pygame-CE)
🎯 Próximos Passos
O projeto está em constante evolução. Os próximos recursos planejados são:

[x] Implementar um Nível 2 com novos desafios.
[x] Adicionar um novo tipo de inimigo terrestre.
[x] Criar power-ups para o jogador (ex: invencibilidade temporária).
[ ] Adicionar um sistema de pontuação.
