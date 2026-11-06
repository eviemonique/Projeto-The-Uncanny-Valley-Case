import sys
import pygame
import random

from historia import cenas, cenario_por_cena
from dados_jogo import descricoes_pistas, personagens
from dataclasses import dataclass, field

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

botao_pistas = pygame.Rect(800, 25, 170, 50)
botao_voltar = pygame.Rect(780, 520, 170, 50)

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

# Cores provisórias para os cenários
cores_cenarios = {
    "casa": (95, 85, 100),
    "jardim": (55, 85, 65),
    "escuro": (18, 18, 24)
}


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

    dica = fonte_botao.render(
        "Clique ou ESPAÇO: continuar  |  I: pistas",
        True,
        BRANCO
    )
    tela.blit(dica, (480, 530))

# ==========================================
# ESTADO DO JOGO
# ==========================================

estado = "menu"

cena_atual = "inicio"
indice_fala = 0

pistas_psicologicas = 0
pistas_sobrenaturais = 0

# Guarda os nomes das pistas encontradas pelo jogador
inventario = []
# Guarda a tela em que o jogador estava antes de abrir o caderno
estado_anterior = None


def avancar_fala():
    """Avança o diálogo ou muda para a próxima parte da história."""
    global indice_fala, estado, cena_atual

    indice_fala += 1
    
    # Registra a bula quando a fala sobre ela aparece
    if cena_atual == "casa" and indice_fala == 1:
        if "Bula do remédio" not in inventario:
            inventario.append("Bula do remédio")
            
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
            
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if estado == "historia" and botao_pistas.collidepoint(evento.pos):
                estado_anterior = estado
                estado = "inventario"
                continue
            elif estado == "inventario" and botao_voltar.collidepoint(evento.pos):
                estado = estado_anterior
                continue

        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_i:
            if estado == "historia":
                estado_anterior = estado
                estado = "inventario"
            elif estado == "inventario":
                estado = estado_anterior
            continue

        if estado == "menu":
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if pygame.Rect(350, 330, 300, 60).collidepoint(evento.pos):
                    estado = "historia"
        elif estado == "historia":
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                avancar_fala()
            elif evento.type == pygame.KEYDOWN and evento.key in (pygame.K_SPACE, pygame.K_RETURN):
                avancar_fala()
        elif estado == "escolha":
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if pygame.Rect(250, 230, 500, 60).collidepoint(evento.pos):
                    cena_atual = "casa"
                    indice_fala = 0
                    pistas_psicologicas += 1
                    estado = "historia"
                elif pygame.Rect(250, 320, 500, 60).collidepoint(evento.pos):
                    cena_atual = "janela"
                    indice_fala = 0
                    pistas_sobrenaturais += 1
                    if "Movimento entre as árvores" not in inventario:
                        inventario.append("Movimento entre as árvores")
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

    # Descobre qual cenário corresponde à cena atual
        nome_cenario = cenario_por_cena[cena_atual]

    # Desenha a cor provisória do cenário
        tela.fill(cores_cenarios[nome_cenario])

    # Mostra a fala atual por cima do cenário
        nome, texto = cenas[cena_atual][indice_fala]
        desenhar_caixa_dialogo(nome, texto)
        desenhar_botao("Pistas", botao_pistas, posicao_mouse)

    elif estado == "escolha":

        titulo = fonte_texto.render("O que Cecília deve fazer?", True, BRANCO)
        tela.blit(titulo, titulo.get_rect(center=(LARGURA // 2, 150)))

        botao_casa = pygame.Rect(250, 230, 500, 60)
        botao_janela = pygame.Rect(250, 320, 500, 60)

        desenhar_botao("Explorar a casa", botao_casa, posicao_mouse)
        desenhar_botao("Olhar pela janela", botao_janela, posicao_mouse)

    elif estado == "inventario":
        tela.fill(PRETO)
        titulo = fonte_titulo.render("Caderno de pistas", True, ROXO_CLARO)
        tela.blit(titulo, (60, 50))
        if not inventario:
            mensagem = fonte_texto.render("Você ainda não encontrou nenhuma pista.", True, BRANCO)
            tela.blit(mensagem, (60, 140))
        else:
            for indice, pista in enumerate(inventario):
                posicao_y = 140 + indice * 110
                texto_pista = fonte_botao.render(f"• {pista}", True, ROXO_CLARO)
                tela.blit(texto_pista, (60, posicao_y))
                descricao = descricoes_pistas.get(pista, "Descrição ainda não disponível.")
                desenhar_texto(descricao, 80, posicao_y + 35, fonte_texto, BRANCO, 820)
        instrucao = fonte_texto.render("Pressione I para voltar à história", True, BRANCO)
        tela.blit(instrucao, (60, 520))
        desenhar_botao("Voltar", botao_voltar, posicao_mouse)

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