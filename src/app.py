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
    #Se crea una instancia de la clase Menu que contiene los metodos para enviar mensajes
    sendMessage = Menu()
    #Se crea una instancia de la clase Resource que contiene los recursos de la app
    resouceMenu = Resource()
    #Se crea una instancia de la clase ConnexionSql que contiene los metodos para hacer consulta y insert en la base de datos
    connexion = ConnexionSql()
    #Aqui decimos que si el request es un get guarda estos datos    
    if request.method == "GET":
        
     #guardo las parametros de verificacion 
        modo = request.args.get("hub.mode")
        challenge = request.args.get("hub.challenge")
        token = request.args.get("hub.verify_token")

    #Valida que modo y token sean correcto
        if modo == "subscribe" and token == verify_token:
            return challenge, 200
        else:
         return "Error de autenticacion", 403

    if request.method == "POST":
        data = request.get_json()
      

        message = data["entry"][0]["changes"][0]["value"]["messages"][0]
        profileName = data["entry"][0]["changes"][0]["value"]["contacts"][0]["profile"]["name"]
        idMessage = data["entry"][0]["changes"][0]["value"]["messages"][0]["id"]
        messageText = message.get("text", {}).get("body", "")
        timestamp = data["entry"][0]["changes"][0]["value"]["messages"][0]["id"]
        idButton = message.get("interactive", {}).get("button_reply", {}).get("id")
        print("Datos del json", data)
   

        
    if messageText.upper() == "Tono".upper():
       sendMessage.welcomeMessage(message["from"])
       if idButton == resouceMenu.idButtonAgendar:
            if connexion.lookForUser(message["from"]) is False:
                sendMessage.simpleMessage(message["from"],resouceMenu.userDontRegistre)
                return jsonify({"status": "ok"}), 200
            elif connexion.lookForUser(message["from"]) is True:
                sendMessage.simpleMessage(message["from"],resouceMenu.timeAvilable)
                return jsonify({"status": "ok"}), 200

    return jsonify({"status": "ok"}), 200
       


if __name__ == "__main__":
   port = int(os.environ.get("PORT", 5000))
   app.run(host="0.0.0.0", port=port)
       

 



