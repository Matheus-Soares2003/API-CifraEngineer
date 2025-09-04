import os
import PyPDF2
import re
from .musica import transpoe_cifra

# Regex aprimorada para encontrar um acorde individualmente, com grupo para o baixo
regex_acorde_individual = re.compile(
    r'(?<!\w)([A-G][b#]?)((?:m|M|maj|min|dim|aug|sus|add|º|°)?[0-9]*\+?(?:\([0-9]+\))?)(?:\/([A-G][b#]?))?(?!\w)'
)

regex_cifra = re.compile(r"^(\s*[A-G](#|b)?(m|M|maj|min|dim|aug|sus|add|º|°)?[0-9]*(/[A-G](#|b)?[0-9]*)?\s*)+$")

class LeitorArquivo():
    def __init__(self, arquivo):
        self.arquivo = arquivo
        self.nome_arquivo, self.extensao_arquivo = os.path.splitext(arquivo.filename)

    def ler_pdf(self, tom_origem=None, tom_destino=None):
        conteudo_pdf = PyPDF2.PdfReader(self.arquivo.stream)
        musica_completa = ""
        inicio_musica = -1
        for page in conteudo_pdf.pages:
            cifra_lista = page.extract_text().split("\n")
            for idx, linha in enumerate(cifra_lista):
                linha_sem_acordes = regex_acorde_individual.sub('', linha).strip()
                if not linha_sem_acordes and inicio_musica == -1 and linha.strip() != "":
                    inicio_musica = idx
                if inicio_musica != -1:
                    musica_completa += "\n".join(cifra_lista[idx:])
                    break

            #print(musica_completa)
        
        cifra_transposta = transpoe_cifra(musica_completa, tom_origem=tom_origem, tom_destino=tom_destino)

        linhas_transpostas = cifra_transposta.split("\n")
        cifra_musica_formatada = ""
        
        for linha in linhas_transpostas:
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

    def ler_img(self):
        return None

    def ler_txt(self):
        return None

    def ler_docx(self):
        return None
