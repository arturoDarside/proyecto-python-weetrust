import requests
import subprocess
import os
from datetime import datetime

# Función para verificar si el token ha expirado
def token_ha_expirado(expiration_time):
    return datetime.now() > expiration_time

# Función para obtener el token desde el archivo token.txt
def obtener_token():
    # Verificar si el archivo token.txt existe
    if os.path.exists("token.txt"):
        with open("token.txt", "r") as f:
            token = f.readline().strip()  # Primer línea: token
            expiration_time_str = f.readline().strip()  # Segunda línea: fecha de expiración
            expiration_time = datetime.strptime(expiration_time_str, "%Y-%m-%d %H:%M:%S")
            
            # Si el token no ha expirado, devolverlo
            if not token_ha_expirado(expiration_time):
                return token

    # Si el token ha expirado o el archivo no existe, generar uno nuevo ejecutando pruebatoken.py
    print("Token caducado o no encontrado. Generando uno nuevo...")
    subprocess.run(["python", "pruebatoken.py"])  # Ejecutar el script que genera el token

    # Ahora que se ha generado el nuevo token, leerlo desde el archivo
    with open("token.txt", "r") as f:
        token = f.readline().strip()  # Leer el nuevo token
    return token

# Obtener el token
token = obtener_token()

# URL de la API
url = "https://api.weetrust.mx/documents/signatory"

# Datos del documento
payload = {
    "documentID": "67f02961032f7c001e9c8fd6",
    "nickname": "APP Android",
    "message": "hola te envio el doc",
    "title": "firmar",
    "hasOrder": False,
    "disableMailing": False,
    "signatory": [
        {
            "emailID": "57231900112@utrng.edu.mx",
            "name": "Roger",
            "identification": "id",
            "check": False,
            "phone": "7561179220"
        }
    ]
}

# Encabezados con el token obtenido
headers = {
    "accept": "application/json",
    "user-id": "kCTmosZegBbnHQBnZw8woqGTGN12",
    "token": token,  # Usamos el token obtenido
    "content-type": "application/json"
}

# Realizar la solicitud PUT para firmar el documento
response = requests.put(url, json=payload, headers=headers)

# Imprimir la respuesta
print(response.text)
