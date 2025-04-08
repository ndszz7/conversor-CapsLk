from flask import Flask, request, jsonify
from flask_cors import CORS
from translatepy import Translator

app = Flask(__name__)
CORS(app)

translator = Translator()

@app.route("/traduzir", methods=["POST"])
def traduzir():
    data = request.get_json()
    texto = data.get("texto", "")
    idioma = data.get("idioma", "en")  # padrão: inglês

    if not texto.strip():
        return jsonify({"error": "Texto vazio."}), 400

    linhas = texto.split("\n")
    traducoes = []

    for linha in linhas:
        if linha.strip() == "":
            traducoes.append("")
            continue

        try:
            traducao = translator.translate(linha, idioma)
            traducoes.append(traducao.result)
        except Exception as e:
            traducoes.append(f"[Erro: {str(e)}]")

    return jsonify({
        "original": linhas,
        "traduzido": traducoes
    })

if __name__ == "__main__":
    app.run(debug=True)
