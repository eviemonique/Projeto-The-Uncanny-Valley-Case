import sys
import pygame
import random
import json

#Imports externos
from pathlib import Path
from historia import (
    cenas,
    cenario_por_cena,
    proximas_cenas,
    escolhas,
    pistas_por_fala,
    episodios, 
    informacoes_cenas,
    locais_por_episodio,
    inicio_dos_episodios,
    musica_por_cena
)
from dados_jogo import (
    descricoes_pistas, 
    personagens,
    desafios,
    pontos_por_pista
)
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

#Botões: 
#Basicos:
botao_pistas = pygame.Rect(800, 25, 170, 50)
botao_voltar = pygame.Rect(780, 520, 170, 50)
botao_personagens = pygame.Rect(350, 420, 300, 55)

#Salvamento:
#Durante as falas:
botao_salvar_historia = pygame.Rect(30, 85, 150, 45)
botao_carregar_historia = pygame.Rect(195, 85, 150, 45)
#Tela de locais:
botao_salvar_locais = pygame.Rect(30, 20, 150, 45)
botao_carregar_locais = pygame.Rect(195, 20, 150, 45)
#Tela inicial:
botao_continuar_jogo = pygame.Rect(350, 410, 300, 60)
#Tela de encerramento:
botao_jogar_novamente = pygame.Rect(180, 495, 300, 55)
botao_sair = pygame.Rect(520, 495, 300, 55)

#Mudança de página no caderno:
botao_pagina_anterior = pygame.Rect(250, 400, 200, 50)
botao_pagina_proxima = pygame.Rect(550, 400, 200, 50)

#Abrir o progresso:
botao_progresso_historia = pygame.Rect(360, 85, 150, 45)
botao_progresso_locais = pygame.Rect(360, 20, 150, 45)

#Voltar da tela de progresso:
botao_voltar_progresso = pygame.Rect(400, 500, 200, 55)

#Acessar personagens:
botao_personagens_anterior = pygame.Rect(250, 420, 200, 50)
botao_personagens_proxima = pygame.Rect(550, 420, 200, 50)

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

# Arquivo correspondente a cada cenário
arquivos_cenarios = {
    "casa": "casa.jpg",
    "jardim": "jardim.jpg"
}

# Imagens associadas aos nomes usados nos diálogos
arquivos_personagens = {
    "Cecília": "cecilia.png",
    "Pai": "pai.png",
    "Circe": "circe.png"
}

# Guarda as imagens já carregadas
imagens_personagens = {}

# Guarda as imagens depois de carregadas
imagens_cenarios = {}

#Arquivo de salvamento
ARQUIVO_SALVAMENTO = Path(__file__).resolve().parent / "salvamento.json"

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
    """Desenha um botão e centraliza seu texto."""
    mouse_em_cima = retangulo.collidepoint(posicao_mouse)

    cor = ROXO_CLARO if mouse_em_cima else ROXO

    pygame.draw.rect(tela, cor, retangulo, border_radius=8)
    pygame.draw.rect(tela, BRANCO, retangulo, 2, border_radius=8)

    # Divide o texto para caber dentro da largura do botão
    linhas = quebrar_texto(
        texto,
        fonte_botao,
        retangulo.width - 20
    )

    altura_total = len(linhas) * fonte_botao.get_linesize()
    posicao_y = retangulo.centery - altura_total // 2

    for linha in linhas:
        imagem_texto = fonte_botao.render(linha, True, BRANCO)

        posicao_texto = imagem_texto.get_rect(
            centerx=retangulo.centerx,
            top=posicao_y
        )

        tela.blit(imagem_texto, posicao_texto)
        posicao_y += fonte_botao.get_linesize()

    return mouse_em_cima


def desenhar_caixa_dialogo(nome, texto):
    """Mostra o nome do personagem e sua fala."""
    caixa = pygame.Rect(40, 390, 920, 170)

    pygame.draw.rect(tela, PRETO, caixa, border_radius=10)
    pygame.draw.rect(tela, BRANCO, caixa, 2, border_radius=10)

    if nome:
        nome_renderizado = fonte_botao.render(
            nome,
            True,
            ROXO_CLARO
        )
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
    
def mostrar_mensagem(texto):
    """Exibe uma mensagem temporária dentro do jogo."""
    global mensagem_tela, mensagem_ate

    mensagem_tela = texto

    #Duração de 3 segundos
    mensagem_ate = pygame.time.get_ticks() + 3000

def salvar_jogo():
    """Salva o progresso atual em um arquivo JSON."""

    if estado not in ("historia", "locais"):
        mostrar_mensagem("Salve durante uma fala ou na tela de locais.")
        return

    dados = {
        "estado": estado,
        "cena_atual": cena_atual,
        "indice_fala": indice_fala,
        "inventario": inventario,
        "locais_visitados": {
            str(episodio): list(locais)
            for episodio, locais in locais_visitados.items()
        },
        "pontos": pontos,
        "acertos": acertos,
        "erros": erros,
        "desafios_respondidos": desafios_respondidos,
        "pistas_psicologicas": pistas_psicologicas,
        "pistas_sobrenaturais": pistas_sobrenaturais,
        "personagens_conhecidos": personagens_conhecidos,
    }

    try:
        with ARQUIVO_SALVAMENTO.open("w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)

        mostrar_mensagem("Jogo salvo com sucesso!")

    except OSError as erro:
        print(f"Erro ao salvar: {erro}")
        mostrar_mensagem("Não foi possível salvar o jogo.")

def carregar_jogo():
    """Carrega o progresso salvo anteriormente."""

    global estado, cena_atual, indice_fala, inventario
    global locais_visitados, pontos, acertos, erros
    global desafios_respondidos
    global pistas_psicologicas, pistas_sobrenaturais
    global pagina_caderno
    global personagens_conhecidos
    global pagina_personagens
        
    if not ARQUIVO_SALVAMENTO.exists():
        mostrar_mensagem("Nenhum jogo salvo foi encontrado.")
        return

    try:
        with ARQUIVO_SALVAMENTO.open("r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
            
        personagens_salvos = dados.get(
            "personagens_conhecidos",
            ["Cecília", "Pai"]
        )

        #Verifica os dados antes de alterar a partida atual
        estado_salvo = dados["estado"]
        cena_salva = dados["cena_atual"]
        fala_salva = dados["indice_fala"]

        if estado_salvo not in ("historia", "locais"):
            raise ValueError("A tela salva não é válida.")

        if cena_salva not in cenas:
            raise ValueError("A cena salva não foi encontrada.")

        if not isinstance(fala_salva, int):
            raise ValueError("A posição da fala não é válida.")

        if estado_salvo == "historia" and not (
            0 <= fala_salva < len(cenas[cena_salva])
        ):
            raise ValueError("A fala salva não foi encontrada.")

        locais_salvos = {
            int(episodio): set(locais)
            for episodio, locais in dados["locais_visitados"].items()
        }

        # Recupera informações
        inventario_salvo = dados["inventario"]
        pontos_salvos = dados["pontos"]
        acertos_salvos = dados["acertos"]
        erros_salvos = dados["erros"]
        desafios_salvos = dados["desafios_respondidos"]
        psicologicas_salvas = dados["pistas_psicologicas"]
        sobrenaturais_salvas = dados["pistas_sobrenaturais"]
        pagina_caderno = 0
        pagina_personagens = 0

    except (OSError, ValueError, KeyError, TypeError) as erro:
        print(f"Erro ao carregar: {erro}")
        mostrar_mensagem("Não foi possível carregar o jogo.")
        return

    #Atualiza a partida depois de ler os dados
    estado = estado_salvo
    cena_atual = cena_salva
    indice_fala = fala_salva
    inventario = inventario_salvo
    locais_visitados = locais_salvos
    pontos = pontos_salvos
    acertos = acertos_salvos
    erros = erros_salvos
    desafios_respondidos = desafios_salvos
    pistas_psicologicas = psicologicas_salvas
    pistas_sobrenaturais = sobrenaturais_salvas
    personagens_conhecidos = personagens_salvos

    mostrar_mensagem("Jogo carregado com sucesso!")

# ==========================================
# ESTADO DO JOGO
# ==========================================

#Variaveis
estado = "menu"
personagens_conhecidos = ["Cecília", "Pai"]
pagina_personagens = 0

cena_atual = "inicio"
indice_fala = 0

pistas_psicologicas = 0
pistas_sobrenaturais = 0

# Mensagem temporária exibida na tela
mensagem_tela = ""
mensagem_ate = 0

#Guarda as pistas
inventario = []
pagina_caderno = 0

#Personagens Iniciais
personagens_conhecidos = ["Cecília", "Pai"]

desafio_atual = None
resultado_desafio = ""
# Pontuação e desempenho nos desafios
pontos = 0
acertos = 0
erros = 0
# Guarda o resultado de cada desafio já respondido
desafios_respondidos = {}

# Guarda os locais visitados em cada episódio
locais_visitados = {
    1: set()
}
#Guarda a tela de antes de abrir o inventario
estado_anterior = None

def reiniciar_partida():
    """Apaga o progresso da partida atual e volta ao menu."""
    global estado, cena_atual, indice_fala
    global inventario, locais_visitados
    global pontos, acertos, erros, desafios_respondidos
    global pistas_psicologicas, pistas_sobrenaturais
    global desafio_atual, resultado_desafio, estado_anterior
    global pagina_caderno
    global personagens_conhecidos
    global pagina_personagens

    estado = "menu"
    cena_atual = "inicio"
    indice_fala = 0
    personagens_conhecidos = ["Cecília", "Pai"]
    pagina_personagens = 0

    inventario = []
    locais_visitados = {1: set()}
    pagina_caderno = 0
    pontos = 0
    acertos = 0
    erros = 0
    desafios_respondidos = {}

    pistas_psicologicas = 0
    pistas_sobrenaturais = 0

    desafio_atual = None
    resultado_desafio = ""
    estado_anterior = None

def registrar_pista_da_fala():
    """Registra e pontua uma pista encontrada pela primeira vez."""
    global pontos

    chave = (cena_atual, indice_fala)
    pista = pistas_por_fala.get(chave)

    if pista is not None and pista not in inventario:
        inventario.append(pista)

        valor = pontos_por_pista.get(pista, 0)
        pontos += valor

        if valor > 0:
            mostrar_mensagem(f"Nova pista: {pista} | +{valor} pontos")
        else:
            mostrar_mensagem(f"Nova pista: {pista}")

def avancar_fala():
    """Avança a fala e consulta o próximo destino da cena."""
    global indice_fala, estado, cena_atual
    global desafio_atual, resultado_desafio

    indice_fala += 1
    registrar_pista_da_fala()

    #Consulta o próximo destino.
    if indice_fala >= len(cenas[cena_atual]):
        proximo = proximas_cenas[cena_atual]

        if proximo == "escolha":
            estado = "escolha"

        elif proximo == "locais":
            estado = "locais"
            
        elif proximo in desafios:
            desafio_atual = proximo

            if desafio_atual in desafios_respondidos:
                #Mostra o resultado de novo, sem contar ponto
                resultado_desafio = desafios_respondidos[desafio_atual]
                estado = "resultado_desafio"
            else:
                resultado_desafio = ""
                estado = "desafio"
            
        elif proximo == "encerrado":
            estado = "encerrado"

        else:
            cena_atual = proximo
            indice_fala = 0
            registrar_pista_da_fala()

# Música que o jogo tentou carregar por último
musica_atual = None

def atualizar_musica(nome_cena):
    """Troca a música quando a cena usa uma faixa diferente."""
    global musica_atual

    nome_musica = musica_por_cena.get(nome_cena)

    # Continua tocando se a próxima cena usar a mesma faixa
    if nome_musica == musica_atual:
        return

    musica_atual = nome_musica

    # Se o áudio não estiver disponível, o jogo continua sem música
    if pygame.mixer.get_init() is None:
        return

    if nome_musica is None:
        pygame.mixer.music.stop()
        return

    caminho = Path(__file__).resolve().parent / "assets" / "audio" / nome_musica

    if not caminho.is_file():
        pygame.mixer.music.stop()
        print(f"Áudio ainda não encontrado: {caminho}")
        return

    try:
        pygame.mixer.music.load(str(caminho))
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)  # Repete até a música mudar

    except pygame.error as erro:
        print(f"Não foi possível tocar {nome_musica}: {erro}")

def desenhar_cenario(nome_cenario):
    """Mostra a imagem do cenário ou sua cor provisória."""

    # Desenha primeiro a cor de fundo
    cor = cores_cenarios.get(nome_cenario, PRETO)
    tela.fill(cor)

    nome_arquivo = arquivos_cenarios.get(nome_cenario)

    # Se não houver imagem cadastrada, mantém a cor
    if nome_arquivo is None:
        return

    # Carrega cada imagem apenas na primeira vez que for usada
    if nome_cenario not in imagens_cenarios:
        caminho = (
            Path(__file__).resolve().parent
            / "assets"
            / "cenarios"
            / nome_arquivo
        )

        imagem = None

        if caminho.is_file():
            try:
                imagem_original = pygame.image.load(str(caminho)).convert()

                imagem = pygame.transform.smoothscale(
                    imagem_original,
                    (LARGURA, ALTURA)
                )

            except pygame.error as erro:
                print(f"Não foi possível carregar {nome_arquivo}: {erro}")
        else:
            print(f"Cenário ainda não encontrado: {caminho}")

        # None também é guardado para não tentar carregar a cada quadro
        imagens_cenarios[nome_cenario] = imagem

    imagem = imagens_cenarios[nome_cenario]

    if imagem is not None:
        tela.blit(imagem, (0, 0))
 
def desenhar_personagem(nome):
    """Mostra a imagem do personagem que está falando."""

    nome_arquivo = arquivos_personagens.get(nome)

    # Narração ou personagem sem imagem cadastrada
    if nome_arquivo is None:
        return

    if nome not in imagens_personagens:
        caminho = (
            Path(__file__).resolve().parent
            / "assets"
            / "personagens"
            / nome_arquivo
        )

        imagem = None

        if caminho.is_file():
            try:
                imagem_original = pygame.image.load(
                    str(caminho)
                ).convert_alpha()

                # Ajusta a imagem proporcionalmente,
                # sem ultrapassar 350 × 380 pixels.
                largura, altura = imagem_original.get_size()
                escala = min(350 / largura, 380 / altura)

                novo_tamanho = (
                    max(1, int(largura * escala)),
                    max(1, int(altura * escala))
                )

                imagem = pygame.transform.smoothscale(
                    imagem_original,
                    novo_tamanho
                )

            except pygame.error as erro:
                print(f"Não foi possível carregar {nome_arquivo}: {erro}")

        else:
            print(f"Personagem ainda não encontrado: {caminho}")

        # Evita tentar abrir o mesmo arquivo a cada quadro
        imagens_personagens[nome] = imagem

    imagem = imagens_personagens[nome]

    if imagem is not None:
        posicao = imagem.get_rect(midbottom=(LARGURA // 2, 410))
        tela.blit(imagem, posicao)
                
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
       
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_F5:
                salvar_jogo()
                continue

            elif evento.key == pygame.K_F9:
                carregar_jogo()
                continue
            
        # Troca de página das fichas de personagens
        if estado == "personagens":
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:

                if botao_personagens_anterior.collidepoint(evento.pos):
                    pagina_personagens = max(0, pagina_personagens - 1)
                    continue

                elif botao_personagens_proxima.collidepoint(evento.pos):
                    ultima_pagina = max(
                        0,
                        (len(personagens_conhecidos) - 1) // 2
                    )

                    pagina_personagens = min(
                        pagina_personagens + 1,
                        ultima_pagina
                    )
                    continue
            
        #Abre e fecha a ficha de personagens
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:

            if estado == "progresso":
                if botao_personagens.collidepoint(evento.pos):
                    estado = "personagens"
                    continue

            elif estado == "personagens":
                if botao_voltar_progresso.collidepoint(evento.pos):
                    estado = "progresso"
                    continue
            
        #Botões de salvar e carregar
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:

            if estado == "menu":
                if botao_continuar_jogo.collidepoint(evento.pos):
                    carregar_jogo()
                    continue

            elif estado == "historia":
                if botao_salvar_historia.collidepoint(evento.pos):
                    salvar_jogo()
                    continue

                elif botao_carregar_historia.collidepoint(evento.pos):
                    carregar_jogo()
                    continue

            elif estado == "locais":
                if botao_salvar_locais.collidepoint(evento.pos):
                    salvar_jogo()
                    continue

                elif botao_carregar_locais.collidepoint(evento.pos):
                    carregar_jogo()
                    continue
                
        # Abre e fecha a tela de progresso
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:

            if estado == "historia":
                if botao_progresso_historia.collidepoint(evento.pos):
                    estado_anterior = estado
                    estado = "progresso"
                    continue

            elif estado == "locais":
                if botao_progresso_locais.collidepoint(evento.pos):
                    estado_anterior = estado
                    estado = "progresso"
                    continue

            elif estado == "progresso":
                if botao_voltar_progresso.collidepoint(evento.pos):
                    estado = estado_anterior
                    continue
        
        #Abre e fecha o caderno com o mouse
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if estado == "historia" and botao_pistas.collidepoint(evento.pos):
                estado_anterior = estado
                estado = "inventario"
                continue
            elif estado == "inventario" and botao_voltar.collidepoint(evento.pos):
                estado = estado_anterior
                continue
            
        # Troca de página do caderno com o mouse
        if estado == "inventario":
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:

                if botao_pagina_anterior.collidepoint(evento.pos):
                    pagina_caderno = max(0, pagina_caderno - 1)
                    continue

                elif botao_pagina_proxima.collidepoint(evento.pos):
                    ultima_pagina = max(0, (len(inventario) - 1) // 2)
                    pagina_caderno = min(
                        pagina_caderno + 1,
                        ultima_pagina
                    )
                    continue

        # Troca de página enquanto o caderno está aberto
        if estado == "inventario" and evento.type == pygame.KEYDOWN:

            if evento.key == pygame.K_RIGHT:
                ultima_pagina = max(0, (len(inventario) - 1) // 2)
                pagina_caderno = min(pagina_caderno + 1, ultima_pagina)
                continue

            elif evento.key == pygame.K_LEFT:
                pagina_caderno = max(0, pagina_caderno - 1)
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

                opcoes = escolhas[cena_atual]["opcoes"]

                for indice, opcao in enumerate(opcoes):
                    botao = pygame.Rect(
                        250,
                        230 + indice * 90,
                        500,
                        60
                    )

                    if botao.collidepoint(evento.pos):
                        cena_atual = opcao["destino"]
                        indice_fala = 0
                        registrar_pista_da_fala()

                        #Mantem a contagem
                        if cena_atual == "casa":
                            pistas_psicologicas += 1

                        elif cena_atual == "janela":
                            pistas_sobrenaturais += 1

                        estado = "historia"
                        break
                    
        elif estado == "locais":
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:

                #Puxa o episodio por cena atual
                numero_episodio = informacoes_cenas[cena_atual]["episodio"]
                locais = locais_por_episodio[numero_episodio]

                for indice, local in enumerate(locais):
                    botao_local = pygame.Rect(
                        250,
                        200 + indice * 80,
                        500,
                        60
                    )

                    if botao_local.collidepoint(evento.pos):
                        locais_visitados.setdefault(numero_episodio, set()).add(local["nome"])
                        cena_atual = local["destino"]
                        indice_fala = 0
                        registrar_pista_da_fala()
                        estado = "historia"
                        break

                # Botão para terminar a demonstração
                botao_finalizar = pygame.Rect(250, 440, 500, 60)

                if botao_finalizar.collidepoint(evento.pos):
                    nomes_dos_locais = {
                        local["nome"] for local in locais
                    }

                    visitados = locais_visitados.get(
                        numero_episodio,
                        set()
                    )

                    if nomes_dos_locais.issubset(visitados):
                        proximo_episodio = numero_episodio + 1

                        # Procura a cena inicial do próximo episódio
                        cena_inicial = inicio_dos_episodios.get(
                            proximo_episodio
                        )

                        if cena_inicial is None:
                            mostrar_mensagem(
                                "O próximo episódio ainda não foi cadastrado."
                            )

                        elif cena_inicial not in cenas:
                            mostrar_mensagem(
                                "A cena inicial do próximo episódio não foi encontrada."
                            )
                            print(f"Cena não encontrada: {cena_inicial}")

                        else:
                            cena_atual = cena_inicial
                            indice_fala = 0
                            registrar_pista_da_fala()
                            estado = "historia"
                        
        elif estado == "desafio":
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                desafio = desafios[desafio_atual]

                for indice, opcao in enumerate(desafio["opcoes"]):
                    botao_resposta = pygame.Rect(
                        100,
                        310 + indice * 90,
                        800,
                        60
                    )

                    if botao_resposta.collidepoint(evento.pos):
                        if indice == desafio["resposta_correta"]:
                            pontos += 10
                            acertos += 1
                            resultado_desafio = (
                                "Resposta correta! +10 pontos. "
                                + desafio["explicacao_correta"]
                            )
                        else:
                            erros += 1
                            resultado_desafio = (
                                "Resposta incorreta. "
                                + desafio["explicacao_incorreta"]
                            )

                        desafios_respondidos[desafio_atual] = resultado_desafio
                        estado = "resultado_desafio"
                        break
                    
        elif estado == "resultado_desafio":
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                botao_continuar = pygame.Rect(350, 440, 300, 60)

                if botao_continuar.collidepoint(evento.pos):
                    destino = desafios[desafio_atual]["proxima_cena"]

                    if destino == "locais":
                        # Retorna aos locais do episódio da cena atual
                        estado = "locais"

                    elif destino == "encerrado":
                        estado = "encerrado"

                    elif destino in desafios:
                        # Abre outro desafio ou mostra seu resultado anterior
                        desafio_atual = destino

                        if desafio_atual in desafios_respondidos:
                            resultado_desafio = desafios_respondidos[
                                desafio_atual
                            ]
                            estado = "resultado_desafio"
                        else:
                            resultado_desafio = ""
                            estado = "desafio"

                    elif destino in cenas:
                        cena_atual = destino
                        indice_fala = 0
                        registrar_pista_da_fala()
                        estado = "historia"

                    else:
                        mostrar_mensagem(
                            "Destino do desafio não encontrado."
                        )
                        print(f"Destino inválido no desafio: {destino}")
                        
        elif estado == "encerrado":
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:

                if botao_jogar_novamente.collidepoint(evento.pos):
                    reiniciar_partida()

                elif botao_sair.collidepoint(evento.pos):
                    pygame.quit()
                    sys.exit()

            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
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
        
        desenhar_botao(
            "Continuar jogo",
            botao_continuar_jogo,
            posicao_mouse
        )

    elif estado == "historia":
        atualizar_musica(cena_atual)

        nome_cenario = cenario_por_cena[cena_atual]
        desenhar_cenario(nome_cenario)

    #Fala atual por cima da cena
        nome, texto = cenas[cena_atual][indice_fala]
        
        #Registra o personagem quando fala:
        if nome in personagens and nome not in personagens_conhecidos:
            personagens_conhecidos.append(nome)
            
        desenhar_personagem(nome)   
        desenhar_caixa_dialogo(nome, texto)
        desenhar_botao("Pistas", botao_pistas, posicao_mouse)
        desenhar_botao("Salvar", botao_salvar_historia, posicao_mouse)
        desenhar_botao("Carregar", botao_carregar_historia, posicao_mouse)
        desenhar_botao("Progresso", botao_progresso_historia, posicao_mouse)
        
        # Mostra o episódio e o local da cena
        info = informacoes_cenas[cena_atual]
        numero_episodio = info["episodio"]
        local_atual = info["local"]

        texto_local = (
            f"Episódio {numero_episodio} — "
            f"{episodios[numero_episodio]['titulo']} | {local_atual}"
        )

        identificacao = fonte_botao.render(
            texto_local,
            True,
            BRANCO
        )
        tela.blit(identificacao, (30, 35))

    elif estado == "escolha":
        escolha_atual = escolhas[cena_atual]

        #Pergunta atual
        titulo = fonte_texto.render(
            escolha_atual["pergunta"],
            True,
            BRANCO
        )
        tela.blit(
            titulo,
            titulo.get_rect(center=(LARGURA // 2, 150))
        )

        #Cria os botões para cada opção
        for indice, opcao in enumerate(escolha_atual["opcoes"]):
            botao = pygame.Rect(
                250,
                230 + indice * 90,
                500,
                60
            )

            desenhar_botao(
                opcao["texto"],
                botao,
                posicao_mouse
            )
            
    elif estado == "locais":
        desenhar_botao("Salvar", botao_salvar_locais, posicao_mouse)
        desenhar_botao("Carregar", botao_carregar_locais, posicao_mouse)
        desenhar_botao("Progresso", botao_progresso_locais, posicao_mouse)
        
        numero_episodio = informacoes_cenas[cena_atual]["episodio"]
        locais = locais_por_episodio[numero_episodio]
        visitados = locais_visitados.get(numero_episodio, set())

        titulo = fonte_titulo.render(
            "Onde você quer investigar?",
            True,
            BRANCO
        )
        tela.blit(titulo, titulo.get_rect(center=(LARGURA // 2, 120)))

        for indice, local in enumerate(locais):
            botao_local = pygame.Rect(
                250,
                200 + indice * 80,
                500,
                60
            )
            nome_botao = local["nome"]

            if local["nome"] in visitados:
                nome_botao += " — visitado"

            desenhar_botao(nome_botao, botao_local, posicao_mouse)

        botao_finalizar = pygame.Rect(250, 440, 500, 60)
        desenhar_botao(
            "Próximo episódio",
            botao_finalizar,
            posicao_mouse
        )
        if len(visitados) < len(locais):
            aviso = fonte_botao.render(
                "Visite todos os locais para continuar.",
                True,
                BRANCO
            )
            tela.blit(aviso, aviso.get_rect(center=(LARGURA // 2, 540)))
    elif estado == "desafio":
        desafio = desafios[desafio_atual]

        titulo = fonte_titulo.render(
            "Desafio de investigação",
            True,
            ROXO_CLARO
        )
        tela.blit(titulo, (60, 25))

        # Mostra as premissas:
        premissas = desafio.get("premissas", [])

        for indice, premissa in enumerate(premissas):
            texto_premissa = fonte_botao.render(
                premissa,
                True,
                BRANCO
            )
            tela.blit(texto_premissa, (60, 85 + indice * 30))

        posicao_pergunta = 100 + len(premissas) * 30

        desenhar_texto(
            desafio["pergunta"],
            60,
            posicao_pergunta,
            fonte_texto,
            BRANCO,
            880
        )

        for indice, opcao in enumerate(desafio["opcoes"]):
            botao_resposta = pygame.Rect(
                100,
                310 + indice * 90,
                800,
                60
            )

            desenhar_botao(
                opcao,
                botao_resposta,
                posicao_mouse
            )
    elif estado == "resultado_desafio":
        titulo = fonte_titulo.render(
            "Resultado",
            True,
            ROXO_CLARO
        )
        tela.blit(titulo, (60, 60))

        desenhar_texto(
            resultado_desafio,
            60,
            180,
            fonte_texto,
            BRANCO,
            880
        )

        botao_continuar = pygame.Rect(350, 440, 300, 60)
        desenhar_botao("Continuar", botao_continuar, posicao_mouse)
        
    elif estado == "progresso":
        tela.fill(PRETO)

        titulo = fonte_titulo.render(
            "Progresso da investigação",
            True,
            ROXO_CLARO
        )
        tela.blit(titulo, (60, 50))

        linhas = [
            f"Pistas encontradas: {len(inventario)}",
            f"Desafios respondidos: {len(desafios_respondidos)}",
            f"Respostas corretas: {acertos}",
            f"Respostas incorretas: {erros}",
            f"Pontuação: {pontos}"
        ]

        for indice, linha in enumerate(linhas):
            texto = fonte_texto.render(linha, True, BRANCO)
            tela.blit(texto, (80, 150 + indice * 50))

        desenhar_botao(
            "Voltar",
            botao_voltar_progresso,
            posicao_mouse
        )
        
        desenhar_botao(
            "Personagens",
            botao_personagens,
            posicao_mouse
        )
    
    elif estado == "personagens":
        tela.fill(PRETO)

        titulo = fonte_titulo.render(
            "Personagens",
            True,
            ROXO_CLARO
        )
        tela.blit(titulo, (60, 40))

        inicio = pagina_personagens * 2
        personagens_da_pagina = personagens_conhecidos[inicio:inicio + 2]

        for indice, nome_personagem in enumerate(personagens_da_pagina):
            dados = personagens[nome_personagem]
            posicao_y = 120 + indice * 110

            nome_renderizado = fonte_botao.render(
                nome_personagem,
                True,
                ROXO_CLARO
            )
            tela.blit(nome_renderizado, (60, posicao_y))

            desenhar_texto(
                dados["descricao"],
                80,
                posicao_y + 30,
                fonte_texto,
                BRANCO,
                820
            )

        desenhar_botao(
            "Voltar",
            botao_voltar_progresso,
            posicao_mouse
        )
        
        desenhar_botao(
            "Anterior",
            botao_personagens_anterior,
            posicao_mouse
        )

        desenhar_botao(
            "Próxima",
            botao_personagens_proxima,
            posicao_mouse
        )

        total_paginas = max(
            1,
            (len(personagens_conhecidos) + 1) // 2
        )

        texto_pagina = fonte_botao.render(
            f"Página {pagina_personagens + 1}/{total_paginas}",
            True,
            BRANCO
        )

        tela.blit(
            texto_pagina,
            texto_pagina.get_rect(center=(LARGURA // 2, 390))
        )

    elif estado == "inventario":
        tela.fill(PRETO)
        titulo = fonte_titulo.render("Caderno de pistas", True, ROXO_CLARO)
        tela.blit(titulo, (60, 50))
        if not inventario:
            mensagem = fonte_texto.render("Você ainda não encontrou nenhuma pista.", True, BRANCO)
            tela.blit(mensagem, (60, 140))
        else:
            inicio = pagina_caderno * 2
            pistas_da_pagina = inventario[inicio:inicio + 2]

            for indice, pista in enumerate(pistas_da_pagina):
                posicao_y = 140 + indice * 110
                texto_pista = fonte_botao.render(f"• {pista}", True, ROXO_CLARO)
                tela.blit(texto_pista, (60, posicao_y))
                descricao = descricoes_pistas.get(pista, "Descrição ainda não disponível.")
                desenhar_texto(descricao, 80, posicao_y + 35, fonte_texto, BRANCO, 820)
        instrucao = fonte_texto.render("Pressione I para voltar à história", True, BRANCO)
        tela.blit(instrucao, (60, 520))
        
        desenhar_botao("Voltar", botao_voltar, posicao_mouse)
        desenhar_botao("Anterior", botao_pagina_anterior, posicao_mouse)
        desenhar_botao("Próxima", botao_pagina_proxima, posicao_mouse)
        
        total_paginas = max(1, (len(inventario) + 1) // 2)

        texto_pagina = fonte_botao.render(
            f"Página {pagina_caderno + 1}/{total_paginas}  |  "
            "Setas: trocar página",
            True,
            BRANCO
        )

        tela.blit(texto_pagina, (60, 470))

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
        desempenho = fonte_texto.render(
            f"Pontos: {pontos} | Acertos: {acertos} | Erros: {erros}",
            True,
            BRANCO
        )

        tela.blit(
            desempenho,
            desempenho.get_rect(center=(LARGURA // 2, 430))
        )
        desenhar_botao(
            "Jogar novamente",
            botao_jogar_novamente,
            posicao_mouse
        )

        desenhar_botao(
            "Sair",
            botao_sair,
            posicao_mouse
        )

    #Mostra a mensagem por cima da tela atual
    if mensagem_tela and pygame.time.get_ticks() < mensagem_ate:
        faixa = pygame.Rect(0, ALTURA - 38, LARGURA, 38)
        pygame.draw.rect(tela, PRETO, faixa)

        texto_mensagem = fonte_botao.render(
            mensagem_tela,
            True,
            BRANCO
        )

        tela.blit(
            texto_mensagem,
            texto_mensagem.get_rect(center=faixa.center)
        )
        
    pygame.display.flip()
    relogio.tick(FPS)