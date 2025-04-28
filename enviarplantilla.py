import requests
import subprocess
from datetime import datetime
import os

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

url = "https://api.weetrust.mx/templates/createDocumentByTemplateV2"

payload = {
    "templateID": "67ed914cdcb3c5002b3943c5",
    "country": "México",
    "inputs": ["Nombre", "Empresa", "Direccion"],
    "signatories": [
        {
            "email": "57231900112@utrng.edu.mx",
            "name": "Roger"
        }
    ],
    "staticSignPositions": [
        {
            "imageSize": [
                {
                    "width": "974",
                    "height": "617"
                }
            ],
            "parentImageSize": {
                "width": "900",
                "height": "600"
            },
            "user": { "email": "57231900112@utrng.edu.mx" },
            "coordinates": {
                "x": "100",
                "y": "200"
            },
            "viewport": {
                "width": "80",
                "height": "90"
            },
            "page": 2,
            "pageY": 200,
            "color": "yellow"
        }
    ]
}
headers = {
    "accept": "application/json",
    "user-id": "kCTmosZegBbnHQBnZw8woqGTGN12",
    "token": token,
    "content-type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)