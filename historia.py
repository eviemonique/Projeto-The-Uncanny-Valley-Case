#Historia Completa
#Cenas - separadas por capitulos

#Cenas definidas em listas: "personagem", "fala"#
# Nome vazio ("") representa a narração.

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
    ],
    
    "visitar_casa": [
        ("", "Cecília observa novamente os cômodos da casa."),
        ("Cecília", "Ainda tem muitas caixas para abrir.")
    ],

    "visitar_jardim": [
        ("", "Cecília caminha pelo jardim e observa a floresta."),
        ("Cecília", "Será que vou encontrar Circe de novo?")
    ],
    
    "inicio_episodio_2": [
        ("", "Episódio 2 — cena de teste."),
        ("", "A história continuará aqui.")
    ],
    
    "decisao_final": [
        ("", "É hora de reunir as informações e apresentar uma conclusão."),
        ("", "Como você interpreta o que aconteceu com Cecília?")
    ],

    "final_verdadeiro": [
        ("", "Cecília segue Circe até a clareira."),
        ("", "Longe da casa, a verdadeira aparência da criatura se revela."),
        ("", "Dias depois, o jornal noticia o desaparecimento da menina."),
        ("", "FINAL VERDADEIRO — A CLAREIRA")
    ],

    "final_falso": [
        ("", "A investigação atribui os relatos de Cecília à imaginação."),
        ("", "A menina recebe atendimento, enquanto as demais pistas "
             "ficam sem uma explicação conclusiva."),
        ("", "FINAL FALSO — UMA CONCLUSÃO PRECIPITADA")
    ],
}

#Cenarios
cenario_por_cena = {
    "inicio": "casa",
    "casa": "casa",
    "janela": "casa",
    "circe": "jardim",
    "fim": "escuro",
    "visitar_casa": "casa",
    "visitar_jardim": "jardim",
    "inicio_episodio_2": "casa",
    "decisao_final": "casa",
    "final_verdadeiro": "jardim",
    "final_falso": "escuro",
}

# Termino das cenas:
#"escolha" abre a tela de opções;
#"encerrado" termina a demonstração.

proximas_cenas = {
    "inicio": "escolha",
    "casa": "circe",
    "janela": "circe",
    "circe": "locais",
    "fim": "encerrado",
    "visitar_casa": "locais",
    "visitar_jardim": "locais",
    "inicio_episodio_2": "desafio_modus_ponens",
    "decisao_final": "escolha",
    "final_verdadeiro": "encerrado",
    "final_falso": "encerrado"
}


#Opções depois da cena "inicio"
escolhas = {
    "inicio": {
        "pergunta": "O que deseja fazer?",

        "opcoes": [
            {
                "texto": "Explorar a casa",
                "destino": "casa"
            },
            {
                "texto": "Olhar pela janela",
                "destino": "janela"
            }
        ]
    },
    
    "decisao_final": {
        "pergunta": "Qual conclusão você apresenta?",

        "opcoes": [
            {
                "texto": "Investigar a ameaça da floresta",
                "destino": "final_verdadeiro"
            },
            {
                "texto": "Atribuir os relatos à imaginação",
                "destino": "final_falso"
            }
        ]
    },
}

# Posição das falas na lista:
# 0 = primeira fala
# 1 = segunda fala
# 2 = terceira fala

pistas_por_fala = {
    ("casa", 1): "Bula do remédio",
    ("janela", 1): "Movimento entre as árvores"
}

# Informações gerais de cada episódio
episodios = {
    1: {
        "titulo": "Uma casa diferente",
        "locais": ["Casa", "Jardim"]
    },

    2: {
        "titulo": "A fada do jardim",
        "locais": ["Casa", "Jardim"]
    },

    3: {
        "titulo": "Duas companhias",
        "locais": ["Casa", "Escola"]
    }
}


# Indica o episódio e o local de cada cena já existente.
# Estes dados são provisórios para testar a estrutura.
informacoes_cenas = {
    "inicio": {"episodio": 1, "local": "Casa"},
    "casa": {"episodio": 1, "local": "Casa"},
    "janela": {"episodio": 1, "local": "Casa"},
    "circe": {"episodio": 1, "local": "Jardim"},
    "fim": {"episodio": 1, "local": "Jardim"},
    "visitar_casa": {"episodio": 1, "local": "Casa"},
    "visitar_jardim": {"episodio": 1, "local": "Jardim"},
    "inicio_episodio_2": {"episodio": 2, "local": "Casa"},
    "decisao_final": {"episodio": 2, "local": "Casa"},
    "final_verdadeiro": {"episodio": 2, "local": "Clareira"},
    "final_falso": {"episodio": 2, "local": "Casa"},
}

#Locais disponiveis por episodio
locais_por_episodio = {
    1: [
        {"nome": "Casa", "destino": "visitar_casa"},
        {"nome": "Jardim", "destino": "visitar_jardim"}
    ]
}

#Cena inicial de cada episodio
inicio_dos_episodios = {
    2: "inicio_episodio_2"
}

# Música de cada cena:
# None significa que a cena ficará sem música.
musica_por_cena = {
    "inicio": "casa.mp3",
    "casa": "casa.mp3",
    "janela": "casa.mp3",
    "circe": "jardim.mp3",
    "visitar_casa": "casa.mp3",
    "visitar_jardim": "jardim.mp3",
    "inicio_episodio_2": "casa.mp3",
    "decisao_final": "casa.mp3",
    "final_verdadeiro": "jardim.mp3",
    "final_falso": None,
    "fim": None
}