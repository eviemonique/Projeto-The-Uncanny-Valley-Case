#Historia Completa


#Cenas - separadas por capitulos

#Cenas definidas em listas: "personagem", "fala"#
# Falas de cada cena:
# ("nome do personagem", "fala")
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
    ]
}

# Cenário usado em cada cena
cenario_por_cena = {
    "inicio": "casa",
    "casa": "casa",
    "janela": "casa",
    "circe": "jardim",
    "fim": "escuro"
}
