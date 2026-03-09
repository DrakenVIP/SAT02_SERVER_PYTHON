from config import whatsappToken
from src.resourceMenu import Resource
import requests
class Menu:
    global resourceMenu
    resourceMenu = Resource()
      #Mensaje menu principal
    def welcomeMessage(self,numberClient):
     
     url = "https://graph.facebook.com/v25.0/971935982677896/messages"
     headers = {
    "Authorization": f"Bearer {whatsappToken}",
    "Content-Type": "application/json",
   
    }

     data = {
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": f"{numberClient}",
  "type": "interactive",
  "interactive": {
    "type": "button",
    "header": {
       "type": "image",
       "image":{
          "id": f"{resourceMenu.logoPrincipalMenu}"
       }
    },
    "body": {
       "text":f"{resourceMenu.welcomenToUser}"
    },
    "footer": {
      "text": "Usa los botones para responder"
      },
    "action": {
       "buttons": [
          {
             "type": "reply",
             "reply": {
                "id": f"{resourceMenu.idButtonAgendar}",
                "title": "📅 Agendar Turno"
             }
          },
          {
             "type": "reply",
             "reply": {
                "id": f"{resourceMenu.idButtonVerTurno}",
                "title": "⏳ Ver Turnos"
             }
          },
          {
             "type": "reply",
             "reply": {
                "id": f"{resourceMenu.idButtonInformacion}",
                "title": "ℹ️ Información"
             }
          }
       ]
     }
    }
   }

     response = requests.post(url, headers=headers, json=data , timeout=30)
     return response
