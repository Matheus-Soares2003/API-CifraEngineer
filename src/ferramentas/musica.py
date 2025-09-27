import re

# Dicionários com as escalas e tons menores
escalas = {
    "C": ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "Bb", "B"],
    "C#": ["C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "Bb", "B", "C"],
    "D": ["D", "D#", "E", "F", "F#", "G", "G#", "A", "Bb", "B", "C", "C#"],
    "D#": ["D#", "E", "F", "F#", "G", "G#", "A", "Bb", "B", "C", "C#", "D"],
    "Eb": ["Eb", "E", "F", "F#", "G", "G#", "A", "Bb", "B", "C", "C#", "D"],
    "E": ["E", "F", "F#", "G", "G#", "A", "Bb", "B", "C", "C#", "D", "D#"],
    "F": ["F", "F#", "G", "G#", "A", "Bb", "B", "C", "C#", "D", "D#", "E"],
    "F#": ["F#", "G", "G#", "A", "Bb", "B", "C", "C#", "D", "D#", "E", "F"],
    "G": ["G", "G#", "A", "Bb", "B", "C", "C#", "D", "D#", "E", "F", "F#"],
    "G#": ["G#", "A", "Bb", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G"],
    "A": ["A", "Bb", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"],
    "A#": ["A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A"],
    "Bb": ["Bb", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A"],
    "B": ["B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "Bb"]
}

escala_menor = {
    "Am": "C", "Bbm": "C#", "Bm": "D", "Cm": "Eb", "C#m": "E", "Dm": "F",
    "D#m": "F#", "Em": "G", "Fm": "G#", "F#m": "A", "Gm": "Bb", "G#m": "B"
}

normalizacao = {
    "B#": "C",
    "Db": "C#",
    #"Eb": "D#",
    "Gb": "F#",
    "Ab": "G#",
    #"A#": "Bb",
    "Cb": "B",
    "E#": "F",
    "Fb": "E"
}

# Regex para identificar uma linha que CONTÉM APENAS acordes
regex_cifra_linha = re.compile(
    r"^\s*(\([A-G][b#]?(?:m|M|maj|min|dim|aug|sus|add|º|°)?\d*(?:\+)?(?:\([0-9]+\))?\s*[A-G][b#]?(?:m|M|maj|min|dim|aug|sus|add|º|°)?\d*(?:\+)?(?:\([0-9]+\))?\)\s*)*[A-G][b#]?(?:m|M|maj|min|dim|aug|sus|add|º|°)?\d*(?:\+)?(?:\([0-9]+\))?(?:\/[A-G][b#]?)?\s*$"
)

# Regex aprimorada para encontrar um acorde individualmente, com grupo para o baixo
regex_acorde_individual = re.compile(
    r'(?<!\w)([A-G][b#]?)((?:m|M|maj|min|dim|aug|sus|add|º|°)?[0-9]*\+?(?:\([0-9]+\))?)(?:\/([A-G][b#]?))?(?!\w)'
)


def transpoe_cifra(cifra_completa, tom_origem, tom_destino):
    """
    Transpõe uma cifra musical de um tom para outro, incluindo acordes com inversão do baixo.
    
    Args:
        cifra_completa (str): A cifra musical completa em formato de texto.
        tom_origem (str): O tom original da música.
        tom_destino (str): O tom para o qual a música será transposta.
        
    Returns:
        str: A cifra transposta.
    """
    
    # Normaliza os tons de origem e destino
    tom_origem_maior, tom_destino_maior = normaliza_tom(tom_origem, tom_destino)

    # Verifica se os tons existem nas escalas
    if tom_origem_maior not in escalas or tom_destino_maior not in escalas:
        print("Erro: Tom de origem ou destino não encontrado nas escalas.")
        return cifra_completa

    linhas_originais = cifra_completa.split("\n")
    nova_cifra_linhas = []

    for linha in linhas_originais:
        nova_linha = linha
        def substitui_acorde(match):
            base_acorde = match.group(1)
            modificador = match.group(2) if match.group(2) else ""
            baixo = match.group(3)
            
            # Normaliza a nota base e a nota do baixo antes de transpor
            base_acorde_normalizada = normalizacao.get(base_acorde, base_acorde)
            baixo_normalizado = normalizacao.get(baixo, baixo) if baixo else None

            # Transpõe a nota base
            try:
                posicao_acorde_original = escalas[tom_origem_maior].index(base_acorde_normalizada)
                novo_acorde_base = escalas[tom_destino_maior][posicao_acorde_original]
            except ValueError:
                novo_acorde_base = base_acorde

            # Transpõe a nota de baixo, se existir
            novo_baixo = ""
            if baixo_normalizado:
                try:
                    posicao_baixo_original = escalas[tom_origem_maior].index(baixo_normalizado)
                    novo_baixo = escalas[tom_destino_maior][posicao_baixo_original]
                    novo_baixo = "/" + novo_baixo
                except ValueError:
                    novo_baixo = "/" + baixo

            return novo_acorde_base + modificador + novo_baixo

        # Substitui os acordes na linha, preservando o espaçamento
        linha_sem_acordes = regex_acorde_individual.sub('', linha).strip()

        if not linha_sem_acordes:
            nova_linha = regex_acorde_individual.sub(substitui_acorde, linha)
        
        nova_cifra_linhas.append(nova_linha)
    
    return "\n".join(nova_cifra_linhas)


def normaliza_tom(tom_origem, tom_destino):
    # Normaliza os tons de origem e destino
    tom_origem_normalizado = normalizacao.get(tom_origem, tom_origem)
    tom_destino_normalizado = normalizacao.get(tom_destino, tom_destino)

    # Converte os tons menores para seus relativos maiores para o cálculo
    tom_origem_maior = escala_menor.get(tom_origem_normalizado, tom_origem_normalizado)
    tom_destino_maior = escala_menor.get(tom_destino_normalizado, tom_destino_normalizado)

    return tom_origem_maior, tom_destino_maior


def achar_inicio_musica(cifra: str):
    cifra_lista = cifra.split("\n")
    musica_completa = ""

    for idx, linha in enumerate(cifra_lista):
        linha_sem_acordes = regex_acorde_individual.sub('', linha).strip()
        if not linha_sem_acordes and linha.strip() != "":
            musica_completa = "\n".join(cifra_lista[idx:])
            break

    return musica_completa


def html_parser_cifra(cifra: str):
    linhas_cifra = cifra.split("\n")
    cifra_musica_formatada = ""
    
    for linha in linhas_cifra:
        # Substitui todos os acordes e espaços por uma string vazia.
        # Se o resultado for uma string vazia, a linha original continha apenas acordes.
        linha_sem_acordes = regex_acorde_individual.sub('', linha).strip()

        if not linha_sem_acordes:
            # Se a linha contiver apenas acordes e espaços, adicione a tag 'acorde'
            cifra_musica_formatada += f"<span class='acorde'>{linha}</span>\n"
        else:
            # Caso contrário, adicione a tag 'letra'
            cifra_musica_formatada += f"<span class='letra'>{linha}</span>\n"
    
    return cifra_musica_formatada.strip()