from flask import Flask, request, jsonify
from ferramentas.file_reader import LeitorArquivo

app = Flask(__name__)

def arquivo_handler(arq, tom_origem, tom_destino):

    leitor_arq = LeitorArquivo(arq)

    extensao_arquivo = leitor_arq.extensao_arquivo
    arquivo_tratado = None

    if extensao_arquivo == ".pdf":
        arquivo_tratado = leitor_arq.ler_pdf(tom_origem, tom_destino)
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
    tom_destino = request.form.get("tom_destino")

    if not tom_original:
        return jsonify({"message": "<h1 class='erro'>Informe o tom em que a música está</h1>"}), 400

    resposta = arquivo_handler(arquivo, tom_original, tom_destino)
    print(resposta)

    if resposta:
        return jsonify({"message": f"""<pre>\n{resposta}\n</pre>"""}), 200
    
    return jsonify({"message": "<h1 class='erro'>ERRO INESPERADO!</h1>"}), 500
    

if __name__ == "__main__":
    app.run(debug=True)