import os
import PyPDF2
import re
from .musica import transpoe_cifra

regex_cifra_linha = re.compile(
    r"^(\s*[A-G](#|b)?(m|M|maj|min|dim|aug|sus|add|º|°)?[0-9]*(?:/[A-G](#|b)?[0-9]*)?\s*)+$"
)

class LeitorArquivo():
    def __init__(self, arquivo):
        self.arquivo = arquivo
        self.nome_arquivo, self.extensao_arquivo = os.path.splitext(arquivo.filename)


    def ler_pdf(self, tom_origem=None, tom_destino=None):
        conteudo_pdf = PyPDF2.PdfReader(self.arquivo.stream)
        musica_completa = ""
        for page in conteudo_pdf.pages:
            musica_completa += page.extract_text() + "\n"
        
        cifra_transposta = transpoe_cifra(musica_completa, tom_origem=tom_origem, tom_destino=tom_destino)

        linhas_transpostas = cifra_transposta.split("\n")
        cifra_musica_formatada = ""
        inicio_musica = -1

        for idx, linha in enumerate(linhas_transpostas):
            if inicio_musica == -1 and regex_cifra_linha.match(linha.strip()):
                inicio_musica = idx
            
            if inicio_musica != -1:
                # Se a linha contiver apenas acordes, adicione a tag 'acorde'
                if regex_cifra_linha.match(linha.strip()):
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
