import requests
import smtplib
from email.message import EmailMessage
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

url = "https://api.weetrust.mx/documents?status=PENDING"

headers = {
    "accept": "application/json",
    "user-id": "kCTmosZegBbnHQBnZw8woqGTGN12",
    "token": token
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    
    for document in data.get("responseData", []):
        for signatory in document.get("signatory", []):
            email = signatory.get("emailID")
            name = signatory.get("name")
            signing_url = signatory.get("signing", {}).get("url")

            if email and signing_url:
                msg = EmailMessage()
                msg["Subject"] = "Firma pendiente de documento"
                msg["From"] = "57231900112@utrng.edu.mx"
                msg["To"] = email
                msg.set_content(f"¡Hola! {name},\n\n¡Hola!, Soy el asistente weetrust🤖,Tienes un documento pendiente de firma. Puedes firmarlo en el siguiente enlace:\n\n{signing_url}\n\nSaludos.")

                try:
                    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                        server.login("navar4077@gmail.com", "quzz wbpc zgrf qagu")
                        server.send_message(msg)
                    print(f"Correo enviado a {email}")
                except Exception as e:
                    print(f"Error al enviar correo a {email}: {e}")
else:
    print("Error al obtener los documentos:", response.text)
