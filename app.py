from flask import Flask, render_template, request
import csv
import os
from datetime import datetime
import webbrowser

app = Flask(__name__)

ARQUIVO = "convidados.csv"


# ==============================
# CRIAR ARQUIVO CSV SE NÃO EXISTIR
# ==============================

def iniciar_csv():
    if not os.path.exists(ARQUIVO):
        with open(ARQUIVO, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Nome", "Data Confirmacao"])


iniciar_csv()


# ==============================
# PAGINA PRINCIPAL
# ==============================

@app.route("/")
def convite():
    return render_template("index.html")


# ==============================
# CONFIRMAR PRESENÇA
# ==============================

@app.route("/confirmar", methods=["POST"])
def confirmar():

    nome = request.form.get("nome")

    if not nome:
        return "Nome não informado"

    with open(ARQUIVO, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            nome,
            datetime.now().strftime("%d/%m/%Y %H:%M")
        ])

    return render_template("confirmado.html", nome=nome)


# ==============================
# INICIAR SERVIDOR
# ==============================

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    # abre navegador apenas uma vez
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        webbrowser.open(f"http://127.0.0.1:{port}")

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )
