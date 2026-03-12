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
        else:
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
                if not connexion.lookForUser(message["from"]):
                    sendMessage.simpleMessage(message["from"], resouceMenu.userDontRegistre)
                    sendMessage.simpleMessage(message["from"], resouceMenu.colocarNombre)

                    saveName = message.get("text", {}).get("body", "").strip()
                    while not resouceMenu.validar_text(saveName):
                        sendMessage.simpleMessage(message["from"], resouceMenu.mensaje_error_nombre)
                        saveName = message.get("text", {}).get("body", "").strip()

                    if resouceMenu.validar_text(saveName):
                        sendMessage.simpleMessage(message["from"], resouceMenu.mensaje_ingreso_cedula)
                        saveCedula = message.get("text", {}).get("body", "").strip()
                        while not resouceMenu.validar_text_cedula(saveCedula):
                            sendMessage.simpleMessage(message["from"], resouceMenu.mensaje_error_cedula)
                            saveCedula = message.get("text", {}).get("body", "").strip()

                        if resouceMenu.validar_text_cedula(saveCedula):
                            sendMessage.simpleMessage(message["from"], f"Te has registrado con éxito {saveName}")
                        return jsonify({"status": "ok"}), 200
                else:
                    sendMessage.simpleMessage(message["from"], resouceMenu.timeAvilable)
                    return jsonify({"status": "ok"}), 200

            # Respuesta final si no cayó en ningún caso
            return jsonify({"status": "ok"}), 200
