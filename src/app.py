from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def home():
   return "Servidor en linea"

@app.route("/webhook", methods=["GET","POST"])
def webhook():

    #Aqui decimos que si el request es un get guarda estos datos    
    if request.method == "GET":
        
     #guardo las parametros de verificacion 
        modo = request.args.get("hub.mode")
        challenge = request.args.get("hub.challenge")
        token = request.args.get("hub.verify_token")

    #Valida que modo y token sean correcto
        if modo == "subscribe" and token == "maria123":
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



    if messegaText.upper() == "Hola".upper():
        url = "https://graph.facebook.com/v25.0/971935982677896/messages"
        headers = {
    "Authorization": "Bearer EAAbPAueSpAUBQ6Vj2gHGT9JbYrWD8sZAjiyy8MZAtLL1ZB7ce4ECxb3uMMvFFH1w4kFtcqFRxIfJEqAZAJ7MKpX4aFHrsiDoSXQzCYcGQqzpfrTuNdLiJRg3A1YRZBLCmZAPfZB64YBXLMToUFHLptbTwATQhTxLAyxDUioKg4llWFjLoOr4ltbmMx8tuQ5ZAI0llWS9JcS3autpqfjCtncoPkGO9ZBmnkfeKuYYB",
    "Content-Type": "application/json",
   
    }

    data = {
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": f"{numberClient}",
  "type": "text",
  "text": {
    "body": f"Hola buenos dias, como estas {profileName}"
    }
   }
    response = requests.post(url, headers=headers, json=data , timeout=30)
    print("Estado de la verificacion",response.status_code)
 
    return jsonify({"status": "ok"}), 200



if __name__ == "__main__":
   app.run()
       

 



