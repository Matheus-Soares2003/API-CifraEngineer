from flask import Flask, request, jsonify
from ferramentas.file_reader import LeitorArquivo
from ferramentas.musica import transpoe_cifra, html_parser_cifra
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def arquivo_handler(arq, tom_origem, tom_destino):

    leitor_arq = LeitorArquivo(arq)

    extensao_arquivo = leitor_arq.extensao_arquivo
    conteudo_cifra = None
    cifra_html = None

    if extensao_arquivo == ".pdf":
        conteudo_cifra = leitor_arq.ler_pdf()
    elif extensao_arquivo == ".png" or extensao_arquivo == ".jpg":
        conteudo_cifra = leitor_arq.ler_img()
    elif extensao_arquivo == ".txt":
        conteudo_cifra = leitor_arq.ler_txt()
    elif extensao_arquivo == ".docx":
        conteudo_cifra = leitor_arq.ler_docx()
    else:
        print("EXTENSÃO DO ARQUIVO NÃO SUPORTADA PELA API!")
    
    if not conteudo_cifra:
        raise Exception("Erro ao ler o arquivo!")
    
    cifra_transposta = transpoe_cifra(conteudo_cifra, tom_origem, tom_destino)
    cifra_html = html_parser_cifra(cifra_transposta)
    return cifra_html


@app.route("/upload", methods=["POST"])
def upload():
    if "arquivo" not in request.files:
        return "<h1 class='erro'>Nenhum arquivo enviado</h1>", 400

    arquivo = request.files["arquivo"]
    tom_original = request.form.get("tom_original")
    tom_destino = request.form.get("tom_destino")

    if not tom_original:
        return "<h1 class='erro'>Informe o tom em que a música está</h1>", 400

    try:
        resposta = arquivo_handler(arquivo, tom_original, tom_destino)
        if resposta:
            return f"""<pre>\n{resposta}\n</pre>""", 200
        
        return "<h1 class='erro'>ERRO INESPERADO!</h1>", 500
    
    except Exception as e:
        print(e)
        return "<h1 class='erro'>ERRO AO LER ARQUIVO!</h1>", 500
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)