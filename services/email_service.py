from flask_mail import Mail, Message

mail = Mail()


def enviar_email(email, titulo, cuerpo):
    msje_titulo = titulo
    emisor = "francokumichel1996@gmail.com"
    msje = Message(msje_titulo, sender=emisor, recipients=[email])
    msje_cuerpo = cuerpo
    msje.body = ""
    data = {
        'app_name': "Oh My Dog",
        'titulo': msje_titulo,
        'cuerpo': msje_cuerpo
    }

    try:
        mail.send(msje)
        return "Mensaje enviado!"
    except Exception as e:
        return f'El email no se ha enviado {e}'
