# Configuración de correos
EMAIL_CONFIG = {
    "gmail": {"server": "imap.gmail.com", "port": 993},
    "outlook": {"server": "outlook.office365.com", "port": 993},
    "hotmail": {"server": "outlook.office365.com", "port": 993}
}

# Credenciales
EMAIL_USER = ""  # Cambia según tu proveedor
EMAIL_PASS = ""  # contraseña de aplicación si es necesario
EMAIL_PROVIDER = "gmail"  # Cambia entre 'gmail', 'outlook' o 'hotmail'

# Definir el servidor IMAP en base al proveedor seleccionado
if EMAIL_PROVIDER in EMAIL_CONFIG:
    IMAP_SERVER = EMAIL_CONFIG[EMAIL_PROVIDER]["server"]
    IMAP_PORT = EMAIL_CONFIG[EMAIL_PROVIDER]["port"]
else:
    raise ValueError(f"⚠ Error: Proveedor de correo '{EMAIL_PROVIDER}' no válido.")
