import os
import PyPDF2
import re
from .musica import Musica


class LeitorArquivo():
    def __init__(self, arquivo, musica_info: Musica):
        self.arquivo = arquivo
        self.nome_arquivo, self.extensao_arquivo = os.path.splitext(arquivo.filename)
        self.musica_info = musica_info
        self.regex_cifra = re.compile(r"^(\s*[A-G](#|b)?(m|M|maj|min|dim|aug|sus|add|º|°)?[0-9]*(/[A-G](#|b)?[0-9]*)?\s*)+$")


    def ler_pdf(self):
        conteudo_pdf = PyPDF2.PdfReader(self.arquivo.stream)
        cifra_musica = ""
        inicio_musica = -1

        for page in conteudo_pdf.pages:
            linhas = page.extract_text().split("\n")
            for idx, linha in enumerate(linhas):
                if self.regex_cifra.match(linha.strip()):
                    inicio_musica = idx if inicio_musica == -1 else inicio_musica
                    linhas[idx] = "<span class='acorde'>" + linha + "</span>"
                else:
                    linhas[idx] = "<span class='letra'>" + linha + "</span>"

            cifra_musica += "\n".join(linhas[inicio_musica:len(linhas)])
        
        return cifra_musica


    def ler_img(self):
        return None


    def ler_txt(self):
        return None


    def ler_docx(self):
        return None 