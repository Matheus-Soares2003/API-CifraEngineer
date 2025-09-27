import os
import PyPDF2
from .musica import achar_inicio_musica

class LeitorArquivo():
    def __init__(self, arquivo):
        self.arquivo = arquivo
        self.nome_arquivo, self.extensao_arquivo = os.path.splitext(arquivo.filename)


    def ler_pdf(self):
        conteudo_pdf = PyPDF2.PdfReader(self.arquivo.stream)
        musica_completa = ""
        for page in conteudo_pdf.pages:
            cifra = page.extract_text()
            musica_completa += achar_inicio_musica(cifra)
        
        return musica_completa 


    def ler_img(self):
        return None


    def ler_txt(self):
        cifra_txt = self.arquivo.read().decode("utf-8")        
        musica_completa = achar_inicio_musica(cifra_txt)
        return musica_completa
        

    def ler_docx(self):
        return None
