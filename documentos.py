import requests
import json
import os
from datetime import datetime
import subprocess

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


# URL de la API
url = "https://api.weetrust.mx/documents"

# Datos del documento
data = {
    "documentSignType": "ELECTRONIC_SIGNATURE",
    "country": "Mexico",
    "language": "es",
    "position": "geolocation",
    "splitPage": "1,2,3,4,5,6,7,8,9"
}

# Ruta del archivo
file_path = r"C:\Users\Hector\OneDrive\Documentos\APPALUMNO.PDF"

# Verificar si el archivo existe
if not os.path.exists(file_path):
    print(f"❌ Error: El archivo '{file_path}' no existe.")
    exit()

# Obtener el token (automáticamente o generando uno nuevo)
token = obtener_token()

# Encabezados
headers = {
    "accept": "application/json",
    "user-id": "kCTmosZegBbnHQBnZw8woqGTGN12",
    "token": token  # Usar el token obtenido automáticamente
}

# Enviar el archivo
with open(file_path, "rb") as file:
    files = {
        "document": (os.path.basename(file_path), file, "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
        "data": (None, json.dumps(data), "application/json")
    }

    print("\n📤 Enviando documento a WeeTrust...")
    response = requests.post(url, headers=headers, files=files)

# Imprimir respuesta
print("\n📊 Respuesta del servidor:")
print(f"HTTP Status: {response.status_code}")

try:
    json_response = response.json()
    print(json.dumps(json_response, indent=2))

    if response.status_code == 200:
        print("\n✅ Documento subido exitosamente!")
    else:
        print("\n❌ Error en la solicitud:")
        print(f"Mensaje: {json_response.get('message', 'Sin mensaje de error')}")
except ValueError:
    print("⚠ La respuesta no es JSON válido:")
    print(response.text)
