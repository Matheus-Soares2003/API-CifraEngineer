from flask import Flask, request, jsonify
from ferramentas.file_reader import LeitorArquivo
from ferramentas.musica import Musica

app = Flask(__name__)

def arquivo_handler(arq, musica):

    leitor_arq = LeitorArquivo(arq, musica_info=musica)

    extensao_arquivo = leitor_arq.extensao_arquivo
    arquivo_tratado = None

    if extensao_arquivo == ".pdf":
        arquivo_tratado = leitor_arq.ler_pdf()
    elif extensao_arquivo == ".png" or extensao_arquivo == ".jpg":
        arquivo_tratado = leitor_arq.ler_img()
    elif extensao_arquivo == ".txt":
        arquivo_tratado = leitor_arq.ler_txt()
    elif extensao_arquivo == ".docx":
        arquivo_tratado = leitor_arq.ler_docx()
    else:
        print("EXTENSÃO DO ARQUIVO NÃO SUPORTADA PELA API!")
    
    return arquivo_tratado

@app.route("/upload", methods=["POST"])
def upload():
    if "arquivo" not in request.files:
        return jsonify({"message": "<h1 class='erro'>Nenhum arquivo enviado</h1>"}), 400

    arquivo = request.files["arquivo"]
    tom_original = request.form.get("tom_original")
    nome_musica = request.form.get("nome_musica")
    compositor = request.form.get("compositor")

    if not tom_original:
        return jsonify({"message": "<h1 class='erro'>Informe o tom em que a música está</h1>"}), 400

    musica = Musica(tom_original, nome_musica, compositor)
    resposta = arquivo_handler(arquivo, musica)

    if resposta:
        return jsonify({"message": resposta}), 200
    
    return jsonify({"message": "<h1 class='erro'>ERRO INESPERADO!</h1>"}), 500
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)