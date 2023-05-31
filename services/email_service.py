from flask import jsonify
from flask_mail import Mail, Message
import os

mail = Mail()

def enviar_email(email, titulo, cuerpo):
    msje_titulo = titulo
    emisor = os.environ['MAIL_USERNAME']
    msje = Message(msje_titulo, sender=emisor, recipients=[email])
    msje.body = cuerpo
    try:
        mail.send(msje)
        return "Mensaje enviado!"
    except Exception as e:
        return  "El email no se ha enviado. Lo sentimos."
