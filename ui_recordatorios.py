import tkinter as tk
from tkinter import ttk, messagebox
import requests
import smtplib
from email.message import EmailMessage
from obtener_token import obtener_token

class NotificacionesPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg="white")

        tk.Label(self, text="Notificaciones de Firma", font=("Arial", 16, "bold"), bg="white").pack(pady=10)

        tk.Button(self, text="Buscar Documentos Pendientes", command=self.buscar_y_notificar, bg="#e67e22", fg="white").pack(pady=10)

        # Tabla para mostrar correos notificados
        self.tree = ttk.Treeview(self, columns=("email", "status"), show="headings", height=10)
        self.tree.heading("email", text="Correo Notificado")
        self.tree.heading("status", text="Estado")
        self.tree.pack(pady=10, fill="both", expand=True)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

    def buscar_y_notificar(self):
        self.tree.delete(*self.tree.get_children())

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
            enviados = []

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
                        msg.set_content(f"¡Hola! {name},\n\nSoy el asistente Weetrust🤖. Tienes un documento pendiente de firma. Puedes firmarlo en el siguiente enlace:\n\n{signing_url}\n\nSaludos.")

                        try:
                            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                                server.login("navar4077@gmail.com", "quzz wbpc zgrf qagu")
                                server.send_message(msg)
                            enviados.append(email)
                            self.tree.insert("", "end", values=(email, "Pendiente de firma"))
                        except Exception as e:
                            print(f"Error al enviar correo a {email}: {e}")
                            self.tree.insert("", "end", values=(email, f"Error: {str(e)}"))

            if enviados:
                messagebox.showinfo("Éxito", f"Correos enviados a {len(enviados)} destinatarios.")
            else:
                messagebox.showinfo("Sin documentos", "No hay documentos pendientes de firma.")
        else:
            messagebox.showerror("Error", f"No se pudo obtener los documentos: {response.text}")
