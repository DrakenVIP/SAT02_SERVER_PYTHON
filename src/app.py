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

@app.route("/webhook", methods=["GET","POST"])
def webhook():
    # Se crea una instancia de la clase Menu que contiene los metodos para enviar mensajes
    sendMessage = Menu()
    # Se crea una instancia de la clase Resource que contiene los recursos de la app
    resouceMenu = Resource()
    # Se crea una instancia de la clase ConnexionSql que contiene los metodos para hacer consulta y insert en la base de datos
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
        idMessage = data["entry"][0]["changes"][0]["value"]["messages"][0]["id"]
        messageText = message.get("text", {}).get("body", "").strip()
        timestamp = data["entry"][0]["changes"][0]["value"]["messages"][0]["id"]
        idButton = (message.get("interactive", {}).get("button_reply", {}).get("id") or "").strip()
        idMessage = message.get("id")

        # Evitar duplicados
        if not connexion.already_processed(idMessage):
            return jsonify({"status": "ok"}), 200
        else:
            connexion.mark_processed(idMessage)
            print("Datos del json", data)

        # --- TU LÓGICA AQUÍ DENTRO --- 



        # Cuando el usuario manda una palabra clave
        if messageText and messageText.upper() == "TONO":
            messageText = ""
            sendMessage.welcomeMessage(message["from"])
            return jsonify({"status": "ok"}), 200

        # Cuando el usuario presiona agendar cita y no está registrado
        if idButton == resouceMenu.idButtonAgendar:
            idButton = ""
            if connexion.lookForUser(message["from"]) is False:
                sendMessage.simpleMessage(message["from"], resouceMenu.userDontRegistre)
                sendMessage.simpleMessage(message["from"], resouceMenu.colocarNombre)
                saveName = message.get("text", {}).get("body", "").strip()
                while resouceMenu.validar_text(saveName) == False:
                    sendMessage.simpleMessage(message["from"], resouceMenu.mensaje_error_nombre)
                    saveName = message.get("text", {}).get("body", "").strip()
                if resouceMenu.validar_text(saveName):
                    sendMessage.simpleMessage(message["from"], resouceMenu.mensaje_ingreso_cedula)
                    saveCedula = message.get("text", {}).get("body", "").strip()
                    while resouceMenu.validar_text_cedula(saveCedula) == False:
                        sendMessage.simpleMessage(message["from"], resouceMenu.mensaje_error_cedula)
                        saveCedula= message.get("text", {}).get("body", "").strip()
                    if resouceMenu.validar_text_cedula(saveCedula):
                        sendMessage.simpleMessage(message["from"], f"Te has gegsitrado con exicto {saveName}")
                    return jsonify({"status": "ok"}), 200
            elif connexion.lookForUser(message["from"]) is True:
                sendMessage.simpleMessage(message["from"], resouceMenu.timeAvilable)
                return jsonify({"status": "ok"}), 200
        else:
            return jsonify({"status": "ok"}), 200
        
        
        
     # Respuesta final
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
       

 



