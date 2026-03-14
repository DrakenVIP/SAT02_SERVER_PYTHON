from flask import Flask, request, jsonify
from src.messageMenu import Menu
from src.resourceMenu import Resource
from src.connexion import ConnexionSql
from src.config import verify_token
import os
import json
import requests

app = Flask(__name__)


@app.route("/")
def home():
    return "Servidor en linea"


@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    # Instancias de las clases
    sendMessage = Menu()
    resouceMenu = Resource()
    connexion = ConnexionSql()

    # --------------------
    # GET (verificación)
    # --------------------
    if request.method == "GET":
        modo = request.args.get("hub.mode")
        challenge = request.args.get("hub.challenge")
        token = request.args.get("hub.verify_token")

        if modo == "subscribe" and token == verify_token:
            return challenge, 200
        else:
            return "Error de autenticacion", 403

    # --------------------
    # POST (webhook data)
    # --------------------
    if request.method == "POST":
        data = request.get_json()

        message = data["entry"][0]["changes"][0]["value"]["messages"][0]
        profileName = data["entry"][0]["changes"][0]["value"]["contacts"][0]["profile"]["name"]
        idMessage = message.get("id")
        messageText = message.get("text", {}).get("body", "").strip()
        idButton = (message.get("interactive", {}).get("button_reply", {}).get("id") or "").strip()

        print(f"Mensaje del usuario: {idMessage}")
        print(f"Texto del usuario: {messageText}")

        # Evitar duplicados
        if connexion.already_processed(idMessage):
            # Ya lo procesaste antes, no hagas nada
            return jsonify({"status": "ok"}), 200

        # Es nuevo, márcalo y procesa
        connexion.mark_processed(idMessage)
        print("Datos del json", data)

        # --- LÓGICA DEL BOT ---

        # Cuando el usuario manda una palabra clave
        if messageText and messageText.upper() == "TONO":
            sendMessage.welcomeMessage(message["from"])
            return jsonify({"status": "ok"}), 200

        # Cuando el usuario presiona agendar cita
        if idButton == resouceMenu.idButtonAgendar:
            print("Estado antes del cambio:", resouceMenu.state_machine["state"] )
            resouceMenu.change_state(True)
            sendMessage.simpleMessage(message["from"], "iniciando app")
            print("Estado despues del cambio:", resouceMenu.state_machine["state"] )
            print("es que estado esta lookfor:", connexion.lookForUser(message["from"]))

            return jsonify({"status": "ok"}), 200
            
        # Flujo de registro
        if resouceMenu.state_machine["state"]== "iniciar" and not connexion.lookForUser(message["from"]):
            resouceMenu.change_state(False)
            sendMessage.simpleMessage(message["from"], resouceMenu.userDontRegistre)
            sendMessage.simpleMessage(message["from"], resouceMenu.colocarNombre)
            return jsonify({"status": "ok"}), 200

        # Capturar y validar nombre
        if resouceMenu.state_machine["state"] == "waiting_name":
            saveName = message.get("text", {}).get("body", "").strip()
            if resouceMenu.change_state(resouceMenu.validar_text(saveName)):
                sendMessage.simpleMessage(message["from"], "Nombre registrado correctamente")
                resouceMenu.change_state(True)
                return jsonify({"status": "ok"}), 200
            else:
                sendMessage.simpleMessage(message["from"], resouceMenu.mensaje_error_nombre)
                return jsonify({"status": "ok"}), 200

        # Capturar y validar cédula
        if resouceMenu.state_machine["state"] == "waiting_cedula":
            saveCedula = message.get("text", {}).get("body", "").strip()
            if resouceMenu.change_state(resouceMenu.validar_text_cedula(saveCedula)):
                sendMessage.simpleMessage(message["from"], "registro completado")
                resouceMenu.change_state(True)
                return jsonify({"status": "ok"}), 200
            else:
                sendMessage.simpleMessage(message["from"], resouceMenu.mensaje_error_cedula)
                return jsonify({"status": "ok"}), 200

        # Respuesta final si no cayó en ningún caso
        return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
