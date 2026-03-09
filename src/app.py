from flask import Flask, request, jsonify
from src.messageMenu import Menu
<<<<<<< HEAD
from src.resourceMenu import Resource
from src.connexion import ConnexionSql
=======
>>>>>>> a59a68bae5967ea16eb9e9d62fce5b44d3df1cf1
from src.config import verify_token,mySqlDb,mySqlHost,mySqlPassword,mySqlUser,whatsappToken
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
        print("Datos del json", data)

        profileName = data["entry"][0]["changes"][0]["value"]["contacts"][0]["profile"]["name"]
        idMessage = data["entry"][0]["changes"][0]["value"]["messages"][0]["id"]
        numberClient = data["entry"][0]["changes"][0]["value"]["messages"][0]["from"]
        messegaText = data["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
        timestamp = data["entry"][0]["changes"][0]["value"]["messages"][0]["id"]
        idButton = data["entry"][0]["changes"][0]["value"]["messages"][0]["interactive"]["button_reply"]["id"]

   


    if messegaText.upper() == "Tono".upper():
       sendMessage.welcomeMessage(numberClient,)
       if idButton == resouceMenu.idButtonAgendar:
            if connexion.lookForUser(numberClient) == False:
                sendMessage.simpleMessage(numberClient,resouceMenu.userDontRegistre)
            elif connexion.lookForUser(numberClient) == True:
                sendMessage.simpleMessage(numberClient,resouceMenu.timeAvilable)

                return jsonify({"status": "ok"}), 200



if __name__ == "__main__":
   app.run()
       

 



