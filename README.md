# App-Veterinaria-IS2-Backend

## Descripción

Este repositorio contiene el código del backend de una página web desarrollada en Python utilizando el framework Flask y la biblioteca SQLAlchemy en el ámbito de de un proyecto de Ingenieria en Software como parte de un trabajo para la facultad de Informática de la UNLP. El backend es responsable de manejar las solicitudes y respuestas entre el cliente y el servidor, así como de interactuar con la base de datos.

## Requerimientos

- Python3
- MySQL

## Instalación

1. Clona este repositorio en tu máquina local.

2. Navega hasta el directorio del proyecto.

3. Ejecuta el siguiente comando para instalar las dependencias:

```bash
pip install -r requirements.txt
```

Tener en cuenta que antes de correr la aplicación, primero tendrás que crear las siguientes variables de entorno dentro de un archivo .env:

- MYSQL_USER=
- MYSQL_PASSWORD=
- MYSQL_DATABASE=
- MYSQL_HOST=

con sus valores correspondientes.

Además, también deberás configurar las variables de entorno para que la aplicación pueda enviar emails.

- SECRET_KEY = Aca poner un password cualquiera
- MAIL_SERVER = Acá poner el servidor que vas a utilizar. Por ejemplo si vas a usar SMTP, sería "smtp.gmail.com"
- MAIL_PORT = Puerto del email. Puede ser 25, 465 o 587 si usas SMTP
- MAIL_USERNAME = Acá iria tu direccion de email desde donde vas a enviar los correos
- MAIL_PASSWORD = Acá iria el password para la aplicación que vas a utilizar
- MAIL_USE_TLS = True

## Uso

Una vez ejecutados los pasos de instalación, deberá ejecutar el siguiente comando:

```bash
python index.py
```
