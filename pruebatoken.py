import requests
from datetime import datetime

# URL del endpoint para obtener el token
url = "https://api.weetrust.mx/access/token"

# Encabezados de la solicitud
headers = {
    "accept": "application/json",
    "user-id": "".strip(),
    "api-key": "".strip()
}

# Realizar la solicitud POST
response = requests.post(url, headers=headers)

# Verificar si la solicitud fue exitosa
if response.status_code == 200:
    try:
        data = response.json()  # Convertir la respuesta a JSON
        token = data.get("responseData", {}).get("accessToken", "")

        if token:
            print("Token generado:", token)

            # Guardar token y hora de creación
            with open("token.txt", "w") as f:
                f.write(token + "\n")
                f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        else:
            print("No se encontró el token en la respuesta.")
    except ValueError:
        print("Error: La respuesta no es un JSON válido.")
else:
    print(f"Error en la solicitud: {response.status_code}")
    print(response.text)  # Mostrar respuesta completa en caso de error
