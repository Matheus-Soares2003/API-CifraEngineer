import re

regex_cifra_linha = re.compile(
    r"^(\s*[A-G][b#]?(?:m|M|maj|min|dim|aug|sus|add|º|°)?[0-9]*(?:/[A-G][b#]?\d*)?\s*)+$"
)

regex_acorde_individual = re.compile(
    r'\b([A-G][b#]?)((?:m|M|maj|min|dim|aug|sus|add|º|°)?[0-9]*(?:/[A-G][b#]?\d*)?)\b'
)

# Escalas cromáticas
escalas = {
    "C":  ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "Bb", "B"],
    "C#": ["C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "Bb", "B", "C"],
    "D":  ["D", "D#", "E", "F", "F#", "G", "G#", "A", "Bb", "B", "C", "C#"],
    "D#": ["D#", "E", "F", "F#", "G", "G#", "A", "Bb", "B", "C", "C#", "D"],
    "E":  ["E", "F", "F#", "G", "G#", "A", "Bb", "B", "C", "C#", "D", "D#"],
    "F":  ["F", "F#", "G", "G#", "A", "Bb", "B", "C", "C#", "D", "D#", "E"],
    "F#": ["F#", "G", "G#", "A", "Bb", "B", "C", "C#", "D", "D#", "E", "F"],
    "G":  ["G", "G#", "A", "Bb", "B", "C", "C#", "D", "D#", "E", "F", "F#"],
    "G#": ["G#", "A", "Bb", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G"],
    "A":  ["A", "Bb", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"],
    "Bb": ["Bb", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A"],
    "B":  ["B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "Bb"]
}

# Relativo menor → maior
escala_menor = {
    "Am": "C",
    "Bbm": "C#",
    "Bm": "D",
    "Cm": "Eb",
    "C#m": "E",
    "Dm": "F",
    "D#m": "F#",
    "Em": "G",
    "Fm": "G#",
    "F#m": "A",
    "Gm": "Bb",
    "G#m": "B"
}


def transpoe_cifra(cifra, tom_origem, tom_destino):
    if tom_origem in escala_menor.keys():
        tom_origem = escala_menor[tom_origem]

    if tom_destino in escala_menor.keys():
        tom_destino = escala_menor[tom_destino]

    linhas_originais = cifra.split("\n")
    nova_cifra_linhas = []

    for linha in linhas_originais:
        if regex_cifra_linha.match(linha.strip()):
            def substitui_acorde(match):
                base_acorde = match.group(1)
                modificador = match.group(2)
                
                # Encontra a posição do acorde base na escala original
                try:
                    posicao_acorde_original = escalas[tom_origem].index(base_acorde)
                except ValueError:
                    # Se o acorde não for encontrado, retorna-o como está
                    return match.group(0)
                
                # Encontra o novo acorde base na escala de destino
                novo_acorde_base = escalas[tom_destino][posicao_acorde_original]

                return novo_acorde_base + modificador

            # Substitui os acordes na linha, preservando o espaçamento
            nova_linha = regex_acorde_individual.sub(substitui_acorde, linha)
            nova_cifra_linhas.append(nova_linha)
        else:
            # Se a linha não for de acordes, a adiciona como está
            nova_cifra_linhas.append(linha)
    
    return "\n".join(nova_cifra_linhas)


def subir_um_tom():
    pass


def diminuir_um_tom():
    pass


def subir_meio_tom():
    pass


def diminuir_meio_tom():
    pass


def adicionar_capotraste(casaCapo):
    pass

