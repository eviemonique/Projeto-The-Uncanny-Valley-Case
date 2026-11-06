"""The Uncanny Valley: protótipo de terminal, Python 3, sem dependências.

Textos/deduções são uma base editável, não a formalização final da disciplina.
Edite EPISODIOS para modificar a história e DESAFIOS para alterar as questões.
"""

LOCAIS = ("Quarto de Cecília", "Sala de casa", "Cozinha", "Sala da escola", "Jardim", "Clareira")

# Um registro: (primeiro episódio disponível, local, título, texto).
# A posição do jornal é sorteada apenas entre locais onde ele pode ser consultado.
PISTAS = {
    "fluffy": (1, 0, "Mr. Fluffy", "Cecília conversa com a pelúcia. Para ela, Fluffy responde; o pai não escuta uma voz independente."),
    "retrato": (1, 0, "Retrato da mãe", "A fotografia é uma lembrança da mãe, falecida em um acidente."),
    "flores": (2, 4, "Flores no jardim", "Cecília atribui as flores a Circe. O objeto existe, mas sua origem ainda não foi demonstrada."),
    "classe": (3, 3, "Diário de Mrs. Diana", "Diana registra brincadeiras com colegas e momentos em que Cecília parece conversar sozinha. Não viu Circe."),
    "marie": (3, 1, "Registro de Mrs. Marie", "Marie conversa com a família: os relatos envolvem luto, mas os pedidos de segredo precisam ser investigados. Nenhum diagnóstico é deduzido dessas observações."),
    "imitacao": (4, 0, "Página do diário", "Depois que mostrei a foto, Circe começou a sorrir como a mamãe. Mas ela errou nossa brincadeira favorita."),
    "jornal": (5, -1, "Jornais antigos", "Notícias relatam desaparecimentos perto da floresta. Algumas vítimas mencionavam uma companhia desconhecida e encontros secretos. Uma foto mostra uma coroa de flores."),
    "coroa": (6, 3, "Nova anotação de Diana", "Cecília voltou do jardim com uma coroa. Diana não viu quem a entregou. A montagem lembra a fotografia do jornal; isso não identifica quem a fez."),
    "convite": (7, 0, "O convite", "Circe prometeu me levar até a mamãe na clareira ao anoitecer. Preciso ir sozinha e deixar o Fluffy em casa."),
}

# As duas campanhas compartilham fatos; apenas o acesso narrativo muda.
EPISODIOS = [
    ("Uma casa diferente", (0, 2),
     "Você organiza seu quarto. Fluffy diz que a casa ficará menos assustadora depois que vocês inventarem novas brincadeiras.",
     "Você organiza a casa com sua filha. No quarto, ela conversa com Fluffy. Na cozinha, os dois evitam falar da cadeira vazia."),
    ("A fada do jardim", (4, 0),
     "Uma mulher entre as árvores diz se chamar Circe. Ela oferece flores e sorri por tempo demais. 'Adultos não entendem magia. Nosso encontro é segredo.'",
     "Cecília volta do jardim com flores. Diz que conheceu Circe, uma fada. Você não viu ninguém entre as árvores."),
    ("Duas companhias", (3, 1),
     "Diana pergunta sobre suas companhias. Depois, Marie visita sua casa e escuta suas histórias sobre Fluffy e Circe.",
     "Diana relata mudanças no comportamento de Cecília. Em visita domiciliar, Marie pede atenção aos encontros e aos pedidos de segredo."),
    ("Um rosto conhecido", (4, 0, 2),
     "Você mostra a foto da mamãe a Circe. Em outro encontro, a fada lembra mais seu rosto. Ela repete suas palavras, mas não conhece uma lembrança que você guardou.",
     "Sua filha diz que Circe está parecida com a mãe. O diário sugere que essa semelhança cresceu depois que Cecília mostrou a fotografia."),
    ("As crianças do jornal", (3, 1),
     "Na atividade escolar, você vê uma notícia sobre uma criança desaparecida. A coroa da foto lembra as flores de Circe.",
     "Um recorte levado da escola chama sua atenção. Você compara notícias sobre desaparecimentos nas proximidades da floresta."),
    ("As flores que ficaram", (3, 4, 1),
     "Diana pergunta de onde veio sua coroa. Você diz que foi Circe. A professora só viu você voltar do jardim.",
     "Diana apresenta sua anotação e a coroa. Ela não encontrou Circe. A semelhança com os jornais gera suspeita, mas admite outras explicações."),
    ("O convite", (4, 0, 1),
     "Circe promete levar você até sua mãe. Exige que vá sozinha à clareira. Quando você menciona Fluffy, sua voz perde a gentileza.",
     "Você encontra um convite descrito no diário: clareira, anoitecer, sem companhia. Agora precisa relacioná-lo às outras informações."),
    ("O que ficou entre as árvores", (0, 1, 5),
     "O anoitecer se aproxima. Você relembra as conversas, as flores e as notícias. É hora de interpretar as pistas.",
     "Os registros estão sobre a mesa. A interpretação do caso encerrará esta investigação. O desfecho verdadeiro será conhecido tarde demais."),
]

DESAFIOS = {
    3: ("O que conversar com Fluffy demonstra sobre Circe?",
        ("Circe também é necessariamente imaginária.", "Ainda é preciso investigar a origem dos relatos sobre Circe."), "2",
        "Uma experiência não determina a origem da outra."),
    5: ("O que a semelhança com os jornais permite concluir?",
        ("Existe um padrão que merece investigação.", "Circe já foi comprovada como autora de todos os casos."), "1",
        "Semelhança justifica investigação, mas não comprova identidade ou autoria."),
    6: ("Diana não viu Circe. Logo, Circe não existe. Essa inferência é válida?",
        ("Sim.", "Não; ausência de observação não prova inexistência."), "2",
        "Diana só pode relatar o que observou; não viu a origem da coroa."),
    7: ("Que conclusão as pistas sustentam antes da revelação?",
        ("O convite secreto repete um padrão de risco dos relatos antigos.", "Um diagnóstico clínico foi demonstrado pela investigação."), "1",
        "O padrão indica risco. Não demonstra um diagnóstico nem, sozinho, a natureza sobrenatural de Circe."),
}


@dataclass
class Partida:
    perspectiva: str
    flor: str = field(default_factory=lambda: random.choice(("violetas", "margaridas", "rosas brancas")))
    local_jornal: int = field(default_factory=lambda: random.choice((1, 3)))
    episodio: int = 1
    pontos: int = 0
    erros: int = 0
    dicas: int = 0
    pistas: set = field(default_factory=set)
    visitados: set = field(default_factory=set)
    respondidos: set = field(default_factory=set)
    acertos: set = field(default_factory=set)


def escolher(texto, opcoes):
    while True:
        resposta = input(texto).strip()
        if resposta in opcoes:
            return resposta
        print("Opção inválida. Tente novamente.")


def local_da_pista(codigo, estado):
    return estado.local_jornal if codigo == "jornal" else PISTAS[codigo][1]


def visitar(estado):
    locais = EPISODIOS[estado.episodio - 1][1]
    for numero, local in enumerate(locais, 1):
        print(f"{numero}. {LOCAIS[local]}")
    print("0. Voltar")
    escolha = escolher("Local: ", {"0"} | {str(i) for i in range(1, len(locais) + 1)})
    if escolha == "0":
        return
    local = locais[int(escolha) - 1]
    estado.visitados.add((estado.episodio, local))
    print(f"\n--- {LOCAIS[local]} ---")
    encontrou = False
    for codigo, (inicio, _, titulo, texto) in PISTAS.items():
        if inicio <= estado.episodio and local_da_pista(codigo, estado) == local:
            encontrou = True
            print(f"\n{titulo}: {texto}")
            if codigo in ("flores", "jornal", "coroa"):
                print(f"Nesta partida, as flores relacionadas são {estado.flor}.")
            if codigo not in estado.pistas:
                estado.pistas.add(codigo)
                estado.pontos += 10
                print("Nova pista: +10 pontos.")
    if not encontrou:
        print("Você observa o ambiente. Não há um novo documento aqui neste episódio.")


def consultar(estado):
    print("\n--- Caderno de investigação ---")
    if not estado.pistas:
        print("Ainda não há pistas registradas.")
    for codigo in PISTAS:
        if codigo in estado.pistas:
            print(f"\n{PISTAS[codigo][2]}: {PISTAS[codigo][3]}")
    print(f"\nInterpretações corretas: {len(estado.acertos)}/{len(DESAFIOS)}")


def interpretar(estado):
    pendentes = [n for n in DESAFIOS if n <= estado.episodio and n not in estado.respondidos]
    if not pendentes:
        print("Nenhum novo desafio disponível.")
        return
    numero = pendentes[0]
    pergunta, opcoes, correta, explicacao = DESAFIOS[numero]
    print("\n" + pergunta)
    for i, texto in enumerate(opcoes, 1):
        print(f"{i}. {texto}")
    resposta = escolher("Resposta: ", {"1", "2"})
    # Cada desafio tem uma tentativa pontuada, evitando repetição para ganhar pontos.
    estado.respondidos.add(numero)
    if resposta == correta:
        estado.pontos += 15
        estado.acertos.add(numero)
        print("Correto: +15 pontos.")
    else:
        estado.pontos -= 5
        estado.erros += 1
        print("Inferência inadequada: −5 pontos.")
    print(explicacao)


def dica(estado):
    estado.pontos -= 10
    estado.dicas += 1
    for codigo, (inicio, _, titulo, _) in PISTAS.items():
        local = local_da_pista(codigo, estado)
        if inicio <= estado.episodio and codigo not in estado.pistas and local in EPISODIOS[estado.episodio - 1][1]:
            print(f"Procure '{titulo}' em {LOCAIS[local]}. Dica: −10 pontos.")
            return
    print("Compare relatos com observações e procure o padrão de isolamento. Dica: −10 pontos.")


def avancar(estado):
    if not any(ep == estado.episodio for ep, _ in estado.visitados):
        print("Visite pelo menos um local antes de avançar.")
        return
    # Avançar com pistas faltando é permitido: as escolhas têm consequências.
    if estado.episodio < 8:
        estado.episodio += 1


def estatisticas(estado):
    print(f"\nPerspectiva: {estado.perspectiva} | Pontos: {estado.pontos}")
    print(f"Pistas: {len(estado.pistas)}/{len(PISTAS)} | Acertos: {len(estado.acertos)}/{len(DESAFIOS)}")
    print(f"Erros: {estado.erros} | Dicas: {estado.dicas}")


def finalizar(estado):
    print("\n1. Relacionar o convite secreto ao padrão dos desaparecimentos")
    print("2. Encerrar atribuindo todos os relatos à imaginação de Cecília")
    print("0. Continuar examinando as pistas")
    escolha = escolher("Interpretação final: ", {"0", "1", "2"})
    if escolha == "0":
        return False
    necessarias = {"jornal", "convite", "coroa"}
    if escolha == "1" and not necessarias <= estado.pistas:
        print("Faltam pistas para apresentar essa relação. Volte a um episódio anterior para investigar.")
        return False
    if escolha == "1":
        estado.pontos += 50
        print("\nFINAL VERDADEIRO — A CLAREIRA")
        if estado.perspectiva == "Cecília":
            print("Você segue Circe acreditando na promessa de encontrar sua mãe. Na clareira, uma lembrança que ela desconhece rompe a imitação. A figura bloqueia sua saída. A cena escurece antes do ataque.")
        else:
            print("Você relaciona os registros tarde demais. Cecília já saiu. Na clareira, encontra uma coroa e objetos da filha. Você não vê Circe. O desfecho revela ao jogador o que ocorreu: a criatura atraiu e devorou Cecília, fora de cena.")
        print("A revelação narrativa confirma que Circe era um predador real. O final verdadeiro é trágico; identificar o padrão não altera o destino desta campanha.")
        print(f"\n[JORNAL] MENINA DE OITO ANOS DESAPARECE PRÓXIMO À FLORESTA\nAs buscas por Cecília concentram-se perto de uma clareira. Uma coroa de {estado.flor} foi encontrada. O caso apresenta semelhanças com desaparecimentos anteriores, cujas vítimas mencionavam uma companhia desconhecida. Seu paradeiro permanece desconhecido.")
    else:
        print("\nFINAL FALSO — O DIAGNÓSTICO")
        print("Os acontecimentos recebem uma explicação equivocada. Um epílogo informa que Cecília foi diagnosticada incorretamente e internada. A investigação foi encerrada; Circe continua escondida. No quarto vazio, Fluffy permanece sobre a cama. Uma nova coroa aparece junto à janela.")
        print("O diagnóstico faz parte do erro ficcional dos personagens; não é uma conclusão clínica demonstrada pelas pistas.")
    estatisticas(estado)
    return True


def selecionar_episodio(estado):
    print("Você pode revisitar episódios anteriores para recuperar pistas, sem alterar a cronologia.")
    escolha = escolher(f"Episódio (1 a {estado.episodio}, 0 para voltar): ", {str(i) for i in range(estado.episodio + 1)})
    if escolha != "0":
        atual = estado.episodio
        estado.episodio = int(escolha)
        visitar(estado)
        estado.episodio = atual


def jogar(perspectiva):
    estado = Partida(perspectiva)
    ultimo = None
    print("\nConteúdo: luto, desaparecimento e morte infantil sugerida. Ataque fora de cena.")
    print("Regras: pista +10; acerto +15; erro −5; dica −10; conclusão sustentada +50. Pontos podem ser negativos.")
    while True:
        if ultimo != estado.episodio:
            titulo, _, cecilia, pai = EPISODIOS[estado.episodio - 1]
            print(f"\nEPISÓDIO {estado.episodio}/8 — {titulo}")
            print(cecilia if perspectiva == "Cecília" else pai)
            ultimo = estado.episodio
        print(f"\nPontos: {estado.pontos}")
        print("1. Visitar local\n2. Consultar pistas\n3. Interpretar pistas\n4. Pedir dica\n5. Avançar episódio\n6. Revisitar episódio\n7. Apresentar conclusão (episódio 8)\n0. Sair da partida")
        escolha = escolher("Ação: ", {str(i) for i in range(8)})
        if escolha == "1": visitar(estado)
        elif escolha == "2": consultar(estado)
        elif escolha == "3": interpretar(estado)
        elif escolha == "4": dica(estado)
        elif escolha == "5":
            if estado.episodio == 8: print("Apresente sua conclusão pela opção 7.")
            else: avancar(estado)
        elif escolha == "6": selecionar_episodio(estado)
        elif escolha == "7":
            if estado.episodio < 8: print("A conclusão fica disponível no episódio 8.")
            elif finalizar(estado): return
        elif escolha == "0":
            print("Partida encerrada sem conclusão. O progresso não é salvo.")
            estatisticas(estado)
            return


def main():
    while True:
        print("\nTHE UNCANNY VALLEY\n1. Jogar como Cecília\n2. Jogar como o pai\n0. Sair")
        escolha = escolher("Perspectiva: ", {"0", "1", "2"})
        if escolha == "0": return
        jogar("Cecília" if escolha == "1" else "Pai")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nJogo encerrado.")
