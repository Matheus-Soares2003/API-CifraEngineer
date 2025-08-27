import os

class LeitorArquivo():
    def __init__(self, arquivo):
        self.arquivo = arquivo
        self.nome_arquivo, self.extensao_arquivo = os.path.splitext(arquivo.filename)


    def ler_pdf(self):
        pass


    def ler_img(self):
        pass


    def ler_txt(self):
        pass


    def ler_docx(self):
        pass 