from flask import Flask, request, jsonify

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
 
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
   app.run()
       

 



