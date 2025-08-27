from flask import Flask, request, jsonify
from ferramentas.file_reader import LeitorArquivo

app = Flask(__name__)

def arquivo_handler(arq):

    leitor_arq = LeitorArquivo(arq)

    extensao_arquivo = leitor_arq.extensao_arquivo
    arquivo_tratado = None

    if extensao_arquivo == ".pdf":
        pass
    elif extensao_arquivo == ".png" or extensao_arquivo == ".jpg":
        pass
    elif extensao_arquivo == ".txt":
        pass
    elif extensao_arquivo == ".docx":
        pass
    else:
        print("EXTENSÃO DO ARQUIVO NÃO SUPORTADA PELA API!")
    
    return arquivo_tratado

@app.route("/upload", methods=["POST"])
def upload():
    if "arquivo" not in request.files:
        return jsonify({"message": "<h1 class='erro'>Nenhum arquivo enviado</h1>"}), 400

    arquivo = request.files["arquivo"]
    resposta = arquivo_handler(arquivo)

    if resposta:
        return jsonify({"message": resposta}), 200
    
    return jsonify({"message": "<h1 class='erro'>ERRO INESPERADO!</h1>"}), 500
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)