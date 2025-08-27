import os

class LeitorArquivo():
    def __init__(self, arquivo):
        self.arquivo = arquivo
        self.nome_arquivo, self.extensao_arquivo = os.path.splitext(arquivo.filename)

    #Só aceitar PDF, TXT ou DOCX
    def ler_arquivo(self):
        pass 