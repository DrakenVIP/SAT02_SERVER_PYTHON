import re
class Resource:
      #Variables de texto de los diferentes menu
      welcomenToUser = '''

✨✨ ¡Bienvenido/a a Tono Barbershop! ✨✨

Nuestro sistema digital está diseñado para ayudarte a gestionar tus turnos de manera rápida y sencilla.
'''

      userDontRegistre = ("📋 *Registro necesario*\n\n👋 ¡Hola! Antes de continuar con el agendado de tu turno necesitamos que completes tu registro, ya que aún no estás registrado en nuestro sistema.\n\n📝 Tranquilo, este paso se hace solo una vez y es muy rápido. Nos permitirá brindarte un mejor servicio en tus próximas reservas.\n\n👉 Por favor llena el formulario y, una vez finalizado, podrás seguir con tu turno sin inconvenientes.\n\n🙌 ¡Gracias por tu confianza!")



      

      

      #Variables de los recursos multimedia

      logoPrincipalMenu = "961877869681925"


      #ID buttons 
      idButtonAgendar = "agendar-button"
      idButtonVerTurno = "turno-button"
      idButtonInformacion = "informacion-button"

      #Formulario
      colocarNombre = "✍️ Por favor escribe tu nombre completo y pulsa el botón \"Enviar\" "
      mensaje_ingreso_cedula = "🪪 Por favor, digita tu cédula sin guiones ➖🚫"
      mensaje_error_nombre = "⚠️ Nombre no válido. 🚫 Vuelve a escribirlo, por favor ✍️"
      mensaje_error_cedula = "⚠️ Cédula no válida. 🚫 Recuerda escribirla sin guiones ✍️"


      #funcion para validar texto del usuario
      def validar_text(self,nombre):
            patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s'-]+$"
            return bool(re.match(patron, nombre))
      
      #funcion para validar texto del usuario
      def validar_text_cedula(self,cedula):
            if len(cedula) == 11:
                  patron = r"^[0987654321]+$"
                  return bool(re.match(patron, cedula))
            else:
                  return False
            


      #Maquina  de estados 
      state_machine = {
            "state":"idle",

            "transition":{
                  "idle":{True: "iniciar"},
                  "iniciar":{ False: "waiting_name"},
                  "waiting_name":{True: "waiting_cedula"},
                  "waiting_cedula":{True: "registro_completado"}
            }
      }

      def change_state(self,event):
            estado_actual = Resource.state_machine["state"]
            transition = Resource.state_machine["transition"].get(estado_actual)
            nextState = transition.get(event)

            if (nextState):
                  Resource.state_machine["state"] = nextState
                  return True
            else:
                  return False


      #Horas disponibles
      timeAvilable ="""
1.  09:00 AM
2.  09:50 AM
3.  10:40 AM
4.  11:30 AM
5.  12:20 PM
6.  01:10 PM
7.  02:00 PM
8.  02:50 PM
9.  03:40 PM
10. 04:30 PM
11. 05:20 PM
12. 06:10 PM
13. 07:00 PM
14. 07:50 PM
15. 08:40 PM
"""
