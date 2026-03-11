from flask import Flask, render_template, request, redirect, session
import csv
import os
from datetime import datetime
import webbrowser

app = Flask(__name__)

app.secret_key = "segredo_super_casamento"

ARQUIVO = "convidados.csv"

SENHA_ADMIN = "123456"


# ==============================
# CRIAR CSV
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
# LOGIN ADMIN
# ==============================

@app.route("/admin", methods=["GET","POST"])
def admin():

    if request.method == "POST":

        senha = request.form.get("senha")

        if senha == SENHA_ADMIN:

            session["logado"] = True
            return redirect("/lista")

        else:
            return "Senha incorreta"

    return render_template("login.html")


# ==============================
# LISTA PROTEGIDA
# ==============================

@app.route("/lista")
def lista():

    if not session.get("logado"):
        return redirect("/admin")

    convidados = []

    if os.path.exists(ARQUIVO):

        with open(ARQUIVO, newline="", encoding="utf-8") as f:

            reader = csv.reader(f)
            next(reader)

            for row in reader:
                convidados.append(row)

    return render_template("lista.html", convidados=convidados)


# ==============================
# LOGOUT
# ==============================

@app.route("/logout")
def logout():

    session.clear()
    return redirect("/admin")


# ==============================
# SERVIDOR
# ==============================

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        webbrowser.open(f"http://127.0.0.1:{port}")

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )
