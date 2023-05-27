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

## Uso

Una vez ejecutados los pasos de instalación, deberá ejecutar el siguiente comando:

```bash
python index.py
```
