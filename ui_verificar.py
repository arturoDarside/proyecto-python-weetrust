import tkinter as tk
from tkinter import ttk, messagebox
import os
import webbrowser
import requests
from flask import Flask, request
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading
import time
import json
from obtener_token import obtener_token

# =====================
# Configuración Global
# =====================
URL_WEBHOOK = "https://0b55-143-255-41-62.ngrok-free.app/webhook"
USER_ID = "kCTmosZegBbnHQBnZw8woqGTGN12"
WEBHOOK_REFRESH_INTERVAL = 300  # 5 minutos en segundos

# Configuración del servidor Flask para webhooks
app = Flask(__name__)

# =====================
# Funciones del Webhook
# =====================
def registrar_webhook(token):
    """Registra el webhook con el token actual"""
    url = f"https://api.weetrust.mx/webhooks?url={URL_WEBHOOK}&type=signDocument"
    headers = {
        "accept": "application/json",
        "user-id": USER_ID,
        "token": token,
        "content-type": "application/json"
    }
    
    try:
        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            print("Webhook registrado exitosamente")
            return True
        else:
            print(f"Error al registrar webhook: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"Error de conexión al registrar webhook: {e}")
        return False

def mantener_webhook_activo():
    """Hilo que mantiene actualizado el webhook cada 5 minutos"""
    while True:
        try:
            token = obtener_token()
            if token:
                if registrar_webhook(token):
                    print("Webhook actualizado correctamente")
                else:
                    print("Error al actualizar webhook")
            else:
                print("No se pudo obtener el token para actualizar webhook")
        except Exception as e:
            print(f"Error en el hilo de actualización de webhook: {e}")
        
        time.sleep(WEBHOOK_REFRESH_INTERVAL)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("Datos recibidos del webhook:", data)

    if data.get("type") == "signDocument":
        signer_email = data.get("data", {}).get("email") 
        if signer_email:
            guardar_firmante(signer_email)
            send_email_notification(signer_email)
            # Actualizar la interfaz si está abierta
            if hasattr(VerificarPanel, 'instance'):
                VerificarPanel.instance.after(0, VerificarPanel.instance.actualizar_lista)

    return "OK", 200

def guardar_firmante(correo):
    """Guarda el correo del firmante en el archivo"""
    with open("firmantes.txt", "a") as f:
        f.write(correo + "\n")
    print(f"Correo guardado: {correo}")

def send_email_notification(correo):
    """Envía notificación por email cuando alguien firma"""
    sender_email = "picejmv@gmail.com"
    receiver_email = "57211000079@utrng.edu.mx"
    password = "ymyb ifff gtae bnjr"

    subject = "Contrato firmado"
    body = f"El siguiente correo ha firmado el contrato: {correo}"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        print("Correo enviado con éxito 📧")
    except Exception as e:
        print(f"Error al enviar correo: {e}")

def run_flask():
    """Inicia el servidor Flask para recibir webhooks"""
    app.run(host='0.0.0.0', port=5000)

# =====================
# Interfaz Gráfica
# =====================
class VerificarPanel(tk.Frame):
    instance = None
    
    def __init__(self, parent):
        super().__init__(parent, bg='white')
        self.parent = parent
        VerificarPanel.instance = self
        
        # Diccionario con los nombres específicos
        self.nombres = {
            "clatempa921@gmail.com": "Carlos Tlatempa",
            "navar4077@gmail.com": "Rogelio Nava",
            "picejmv@gmail.com": "Jonathan Murphy",
            "57231900112@utmg.edu.mx": "Arturo Gutierrez",
            "carlosarturo756z106@gmail.com": "Carlos Arturo"
        }
        
        self.setup_ui()
        self.mostrar_mensaje_inicial()
        
        # Iniciar el hilo para mantener el webhook activo
        self.iniciar_webhook_automatico()

    def iniciar_webhook_automatico(self):
        """Inicia el hilo que mantiene el webhook actualizado"""
        webhook_thread = threading.Thread(target=mantener_webhook_activo, daemon=True)
        webhook_thread.start()

    def setup_ui(self):
        # Configuración de la interfaz
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Frame contenedor
        self.main_frame = tk.Frame(self, bg='white')
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        # Título
        tk.Label(self.main_frame, 
                text="Firmantes Registrados", 
                font=("Arial", 16, "bold"), 
                bg='white').pack(pady=(0, 20))
        
        # Frame para la lista
        self.list_frame = tk.Frame(self.main_frame, bg='white')
        self.list_frame.pack(fill='both', expand=True)
        
        # Lista de firmantes con scrollbar
        self.tree = ttk.Treeview(self.list_frame, 
                               columns=('Correo', 'Nombre', 'Veces Firmado'), 
                               show='headings')
        
        # Configurar columnas
        self.tree.heading('Correo', text='Correo Electrónico')
        self.tree.heading('Nombre', text='Nombre')
        self.tree.heading('Veces Firmado', text='Veces Firmado')
        self.tree.column('Correo', width=250, anchor='w')
        self.tree.column('Nombre', width=200, anchor='w')
        self.tree.column('Veces Firmado', width=100, anchor='center')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.list_frame, orient='vertical', command=self.tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side='left', fill='both', expand=True)
        
        # Barra de progreso
        self.progress = ttk.Progressbar(self.main_frame, orient='horizontal', 
                                      length=300, mode='determinate')
        self.progress.pack(pady=(10, 0))
        self.progress.pack_forget()  # Ocultar inicialmente
        
        # Botón para actualizar
        self.btn_actualizar = tk.Button(self.main_frame, 
                                      text="Actualizar Lista", 
                                      command=self.iniciar_actualizacion,
                                      bg='#3498db', 
                                      fg='white',
                                      font=("Arial", 10),
                                      relief='flat')
        self.btn_actualizar.pack(pady=(20, 0))
        
        # Frame para mensajes
        self.message_frame = tk.Frame(self.main_frame, bg='white')
        self.message_frame.pack(fill='x', pady=(10, 0))
        
        # Mensaje de estado
        self.lbl_mensaje = tk.Label(self.message_frame, 
                                  text="", 
                                  fg='black',
                                  bg='white',
                                  font=("Arial", 10))
        self.lbl_mensaje.pack(side='left')
        
        # Botón para abrir enlace (oculto inicialmente)
        self.btn_enlace = tk.Button(self.message_frame, 
                                  text="Ir a WeeTrust", 
                                  command=self.abrir_enlace,
                                  bg='#e74c3c', 
                                  fg='white',
                                  font=("Arial", 8),
                                  relief='flat')
        self.btn_enlace.pack(side='left', padx=10)
        self.btn_enlace.pack_forget()

    def mostrar_mensaje_inicial(self):
        """Muestra un mensaje inicial en la lista"""
        self.limpiar_lista()
        self.actualizar_mensaje("Presione 'Actualizar Lista' para verificar firmantes", "black")
        self.tree.insert('', 'end', values=("Presione el botón para verificar", "", ""))

    def limpiar_lista(self):
        """Limpia todos los elementos de la lista"""
        for item in self.tree.get_children():
            self.tree.delete(item)

    def actualizar_mensaje(self, texto, color="black"):
        """Actualiza el mensaje de estado"""
        self.lbl_mensaje.config(text=texto, fg=color)
        if "error" in texto.lower() or "no hay firmantes" in texto.lower():
            self.btn_enlace.pack(side='left', padx=10)
        else:
            self.btn_enlace.pack_forget()

    def abrir_enlace(self):
        """Abre el enlace a WeeTrust en el navegador"""
        webbrowser.open("https://app.weetrust.mx/dashboard/document")

    def iniciar_actualizacion(self):
        """Inicia el proceso de actualización con barra de progreso"""
        self.btn_actualizar.config(state='disabled')
        self.progress.pack(pady=(10, 0))
        self.progress['value'] = 0
        self.actualizar_mensaje("Verificando firmantes...", "blue")
        
        # Simular carga
        self.after(100, lambda: self.progress.step(20))
        self.after(200, lambda: self.progress.step(40))
        self.after(300, lambda: self.progress.step(60))
        self.after(400, lambda: self.progress.step(80))
        self.after(500, self.finalizar_actualizacion)

    def finalizar_actualizacion(self):
        """Finaliza el proceso de actualización"""
        self.progress['value'] = 100
        
        try:
            firmantes_encontrados = self.actualizar_lista()
            
            if not firmantes_encontrados:
                self.actualizar_mensaje("No hay firmantes registrados. Favor de revisar en WeeTrust", "red")
            else:
                self.actualizar_mensaje(f"Se encontraron {firmantes_encontrados} firmante(s)", "green")
                
        except Exception as e:
            self.actualizar_mensaje(f"Advertencia: {str(e)}. Favor de compilar datos", "red")
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")
        finally:
            self.progress.pack_forget()
            self.btn_actualizar.config(state='normal')

    def actualizar_lista(self):
        """Carga los firmantes desde el archivo"""
        self.limpiar_lista()
        firmantes_encontrados = 0
        
        try:
            if not os.path.exists("firmantes.txt"):
                self.tree.insert('', 'end', values=("No se encontró el archivo de firmantes", "", ""))
                return 0
                
            with open("firmantes.txt", "r") as f:
                correos = [line.strip() for line in f.readlines() if line.strip()]
                
            if not correos:
                self.tree.insert('', 'end', values=("No hay firmantes registrados", "", ""))
                return 0
            else:
                conteo = {}
                for correo in correos:
                    conteo[correo] = conteo.get(correo, 0) + 1
                
                for correo, veces in conteo.items():
                    nombre = self.nombres.get(correo, "Nombre no registrado")
                    self.tree.insert('', 'end', values=(correo, nombre, veces))
                    firmantes_encontrados += 1
                    
                return firmantes_encontrados
                    
        except FileNotFoundError:
            self.tree.insert('', 'end', values=("Archivo de firmantes no encontrado", "", ""))
            return 0
        except Exception as e:
            self.tree.insert('', 'end', values=(f"Error: {str(e)}", "", ""))
            return 0

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Verificación de Firmas")
        self.geometry("900x600")
        self.configure(bg='#f4f4f4')
        
        # Crear y mostrar el panel de verificación
        self.verificar_panel = VerificarPanel(self)
        self.verificar_panel.pack(fill='both', expand=True)

# =====================
# Iniciar Aplicación
# =====================
if __name__ == "__main__":
    # Crear archivo de ejemplo si no existe
    if not os.path.exists("firmantes.txt"):
        with open("firmantes.txt", "w") as f:
            f.write("clatempa921@gmail.com\n")
            f.write("navar4077@gmail.com\n")
            f.write("picejmv@gmail.com\n")
            f.write("picejmv@gmail.com\n")
            f.write("picejmv@gmail.com\n")
            f.write("57231900112@utmg.edu.mx\n")
            f.write("carlosarturo756z106@gmail.com\n")
            f.write("navar4077@gmail.com\n")
            f.write("carlosarturo756z106@gmail.com\n")
    
    # Iniciar servidor Flask en segundo plano
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Iniciar la aplicación Tkinter
    app = MainApp()
    app.mainloop()