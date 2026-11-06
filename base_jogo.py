import sys
import pygame

import sys
import pygame

# ==========================================
# CONFIGURAÇÕES
# ==========================================

pygame.init()

LARGURA = 1000
ALTURA = 600
FPS = 60

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("The Uncanny Valley")

relogio = pygame.time.Clock()

# Cores
PRETO = (18, 18, 24)
BRANCO = (245, 245, 245)
CINZA = (65, 65, 75)
ROXO = (110, 80, 135)
ROXO_CLARO = (170, 135, 195)

# Fontes
fonte_titulo = pygame.font.SysFont("arial", 42, bold=True)
fonte_texto = pygame.font.SysFont("arial", 25)
fonte_botao = pygame.font.SysFont("arial", 24)


# ==========================================
# FUNÇÕES DE DESENHO
# ==========================================

def quebrar_texto(texto, fonte, largura_maxima):
    """Divide o texto em linhas para caber na área disponível."""
    palavras = texto.split()
    linhas = []
    linha_atual = ""

    for palavra in palavras:
        teste = f"{linha_atual} {palavra}".strip()

        if fonte.size(teste)[0] <= largura_maxima:
            linha_atual = teste
        else:
            if linha_atual:
                linhas.append(linha_atual)
            linha_atual = palavra

    if linha_atual:
        linhas.append(linha_atual)

    return linhas


def desenhar_texto(texto, x, y, fonte, cor, largura_maxima):
    """Desenha um texto com quebra automática de linha."""
    linhas = quebrar_texto(texto, fonte, largura_maxima)

    for indice, linha in enumerate(linhas):
        imagem = fonte.render(linha, True, cor)
        tela.blit(imagem, (x, y + indice * fonte.get_linesize()))


def desenhar_botao(texto, retangulo, posicao_mouse):
    """Desenha um botão e retorna se o mouse está sobre ele."""
    mouse_em_c_cima = retangulo.collidepoint(posicao_mouse)

    cor = ROXO_CLARO if mouse_em_c_cima else ROXO

    pygame.draw.rect(tela, cor, retangulo, border_radius=8)
    pygame.draw.rect(tela, BRANCO, retangulo, 2, border_radius=8)

    imagem_texto = fonte_botao.render(texto, True, BRANCO)
    posicao_texto = imagem_texto.get_rect(center=retangulo.center)

    tela.blit(imagem_texto, posicao_texto)

    return mouse_em_c_cima


def desenhar_caixa_dialogo(nome, texto):
    """Mostra o nome do personagem e sua fala."""
    caixa = pygame.Rect(40, 390, 920, 170)

    pygame.draw.rect(tela, PRETO, caixa, border_radius=10)
    pygame.draw.rect(tela, BRANCO, caixa, 2, border_radius=10)

    if nome:
        nome_renderizado = fonte_botao.render(nome, True, ROXO_CLARO)
        tela.blit(nome_renderizado, (65, 408))

    desenhar_texto(
        texto,
        65,
        445,
        fonte_texto,
        BRANCO,
        865
    )

    dica = fonte_texto.render("Clique ou pressione espaço para continuar", True, BRANCO)
    tela.blit(dica, (550, 530))


# ==========================================
# HISTÓRIA
# ==========================================

# Cada cena tem uma lista de falas.
# Uma fala possui: (nome do personagem, texto).
# Use nome vazio para a narração.

cenas = {
    "inicio": [
        ("", "Após a morte de sua mãe, Cecília e seu pai se mudam para uma cidade próxima à floresta."),
        ("", "A casa é nova. A escola é nova. Mas a saudade continua acompanhando Cecília."),
        ("Cecília", "Pai... você acha que a mamãe consegue nos encontrar aqui?"),
        ("Pai", "Acho que ela sempre vai estar com a gente, de alguma forma."),
        ("", "Cecília aperta Mr. Fluffy contra o peito."),
        ("Cecília", "Ainda não sei se gosto desta casa."),
        ("Pai", "Vamos descobrir juntos, está bem?")
    ],

    "casa": [
        ("", "Cecília caminha pelo corredor e observa as caixas ainda fechadas."),
        ("", "Sobre uma mesa, ela encontra um frasco de remédio e uma bula."),
        ("", "A bula menciona alucinações entre os possíveis efeitos adversos."),
        ("Cecília", "O que isso quer dizer?")
    ],

    "janela": [
        ("", "Cecília observa a floresta pela janela."),
        ("", "Por um instante, algo parece se mover entre as árvores."),
        ("Cecília", "Tem alguém ali?"),
        ("", "Quando pisca, o movimento desaparece.")
    ],

    "circe": [
        ("", "Mais tarde, Cecília brinca perto da casa quando escuta uma voz."),
        ("Circe", "Você está procurando alguma coisa?"),
        ("", "Entre as árvores, uma figura observa a menina."),
        ("Cecília", "Quem é você?"),
        ("Circe", "Pode me chamar de Circe."),
        ("Cecília", "Você mora na floresta?"),
        ("Circe", "De certa forma."),
        ("", "Circe sorri. Há algo estranho em seu sorriso, mas sua voz é gentil.")
    ],

    "fim": [
        ("", "Fim da introdução."),
        ("", "A história continuará nos próximos episódios.")
    ]
}


# ==========================================
# ESTADO DO JOGO
# ==========================================

estado = "menu"

cena_atual = "inicio"
indice_fala = 0

pistas_psicologicas = 0
pistas_sobrenaturais = 0


def avancar_fala():
    """Avança o diálogo ou muda para a próxima parte da história."""
    global indice_fala, estado, cena_atual

    indice_fala += 1

    if indice_fala >= len(cenas[cena_atual]):

        if cena_atual == "inicio":
            estado = "escolha"

        elif cena_atual in ("casa", "janela"):
            cena_atual = "circe"
            indice_fala = 0

        elif cena_atual == "circe":
            cena_atual = "fim"
            indice_fala = 0

        elif cena_atual == "fim":
            estado = "encerrado"


# ==========================================
# LOOP PRINCIPAL
# ==========================================

while True:
    posicao_mouse = pygame.mouse.get_pos()

    # ------------------------------
    # EVENTOS
    # ------------------------------

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

        if estado == "menu":

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                botao_iniciar = pygame.Rect(350, 330, 300, 60)

                if botao_iniciar.collidepoint(evento.pos):
                    estado = "historia"

        elif estado == "historia":

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                avancar_fala()

            elif evento.type == pygame.KEYDOWN and evento.key in (pygame.K_SPACE, pygame.K_RETURN):
                avancar_fala()

        elif estado == "escolha":

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:

                botao_casa = pygame.Rect(250, 230, 500, 60)
                botao_janela = pygame.Rect(250, 320, 500, 60)

                if botao_casa.collidepoint(evento.pos):
                    cena_atual = "casa"
                    indice_fala = 0
                    pistas_psicologicas += 1
                    estado = "historia"

                elif botao_janela.collidepoint(evento.pos):
                    cena_atual = "janela"
                    indice_fala = 0
                    pistas_sobrenaturais += 1
                    estado = "historia"

        elif estado == "encerrado":

            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                pygame.quit()
                sys.exit()

    # ------------------------------
    # DESENHO DA TELA
    # ------------------------------

    tela.fill(PRETO)

    if estado == "menu":

        titulo = fonte_titulo.render("THE UNCANNY VALLEY", True, BRANCO)
        tela.blit(titulo, titulo.get_rect(center=(LARGURA // 2, 220)))

        botao_iniciar = pygame.Rect(350, 330, 300, 60)
        desenhar_botao("Iniciar jogo", botao_iniciar, posicao_mouse)

    elif estado == "historia":

        # Fundo temporário para representar o cenário
        tela.fill(CINZA)

        nome, texto = cenas[cena_atual][indice_fala]
        desenhar_caixa_dialogo(nome, texto)

    elif estado == "escolha":

        titulo = fonte_texto.render("O que Cecília deve fazer?", True, BRANCO)
        tela.blit(titulo, titulo.get_rect(center=(LARGURA // 2, 150)))

        botao_casa = pygame.Rect(250, 230, 500, 60)
        botao_janela = pygame.Rect(250, 320, 500, 60)

        desenhar_botao("Explorar a casa", botao_casa, posicao_mouse)
        desenhar_botao("Olhar pela janela", botao_janela, posicao_mouse)

    elif estado == "encerrado":

        mensagem = fonte_texto.render(
            "Fim da demonstração. Pressione ENTER para sair.",
            True,
            BRANCO
        )

        tela.blit(mensagem, mensagem.get_rect(center=(LARGURA // 2, ALTURA // 2)))

        resumo = fonte_texto.render(
            f"Pistas psicológicas: {pistas_psicologicas} | "
            f"Pistas sobrenaturais: {pistas_sobrenaturais}",
            True,
            ROXO_CLARO
        )

        tela.blit(resumo, resumo.get_rect(center=(LARGURA // 2, 380)))

    pygame.display.flip()
    relogio.tick(FPS)