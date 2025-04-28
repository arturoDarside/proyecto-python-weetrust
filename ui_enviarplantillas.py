import tkinter as tk
from tkinter import messagebox
import requests
from obtener_token import obtener_token

class FirmaPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.COLOR_PRIMARY = "#2c3e50"
        self.COLOR_ACCENT = "#2ecc71"
        self.COLOR_LIGHT = "#ecf0f1"
        self.COLOR_DARK = "#34495e"

        self.configure(bg=self.COLOR_LIGHT, padx=20, pady=20)

        main_frame = tk.Frame(self, bg=self.COLOR_LIGHT, padx=15, pady=15, 
                              highlightbackground=self.COLOR_DARK, highlightthickness=1)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        header_frame = tk.Frame(main_frame, bg=self.COLOR_PRIMARY)
        header_frame.pack(fill="x", pady=(0, 15))

        title_label = tk.Label(header_frame, text="ENVIAR DOCUMENTO A FIRMA", 
                          font=("Helvetica", 16, "bold"), bg=self.COLOR_PRIMARY, 
                          fg="white", pady=10)
        title_label.pack()

        form_frame = tk.Frame(main_frame, bg=self.COLOR_LIGHT)
        form_frame.pack(pady=10)

        # Campos del formulario
        self.template_id_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.email_var = tk.StringVar()

        self.create_input(form_frame, "Template ID:", self.template_id_var)
        self.create_input(form_frame, "Nombre del firmante:", self.name_var)
        self.create_input(form_frame, "Email del firmante:", self.email_var)

        # Botón estilizado
        send_btn = tk.Button(
            form_frame, text="Mandar a firmar", 
            command=self.enviar_a_firma,
            bg=self.COLOR_ACCENT, fg="white", relief="flat",
            font=("Helvetica", 10, "bold"), padx=20, pady=10,
            activebackground="#27ae60", cursor="hand2"
        )
        send_btn.pack(pady=20)

        # Hover efecto
        send_btn.bind("<Enter>", lambda e: send_btn.config(bg="#27ae60"))
        send_btn.bind("<Leave>", lambda e: send_btn.config(bg=self.COLOR_ACCENT))

    def create_input(self, parent, label_text, variable):
        frame = tk.Frame(parent, bg=self.COLOR_LIGHT)
        frame.pack(fill="x", pady=5)
        label = tk.Label(frame, text=label_text, bg=self.COLOR_LIGHT, fg=self.COLOR_DARK, 
                         font=("Helvetica", 10, "bold"))
        label.pack(anchor="w")
        entry = tk.Entry(frame, textvariable=variable, font=("Helvetica", 10), bg="white",
                         highlightthickness=1, highlightbackground="#bdc3c7", relief="flat")
        entry.pack(fill="x", ipady=5)

    def enviar_a_firma(self):
        token = obtener_token()
        template_id = self.template_id_var.get()
        nombre = self.name_var.get()
        email = self.email_var.get()

        if not all([template_id, nombre, email]):
            messagebox.showerror("Error", "Por favor completa todos los campos.")
            return

        payload = {
            "templateID": template_id,
            "country": "México",
            "inputs": ["Nombre", "Empresa", "Direccion"],
            "signatories": [
                {
                    "email": email,
                    "name": nombre
                }
            ],
            "staticSignPositions": [
                {
                    "imageSize": [{"width": "974", "height": "617"}],
                    "parentImageSize": {"width": "900", "height": "600"},
                    "user": {"email": email},
                    "coordinates": {"x": "100", "y": "200"},
                    "viewport": {"width": "80", "height": "90"},
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

        try:
            url = "https://api.weetrust.mx/templates/createDocumentByTemplateV2"
            response = requests.post(url, json=payload, headers=headers)
            data = response.json()

            if response.status_code == 200 and data.get("success"):
                messagebox.showinfo("Éxito", "Documento enviado a firmar correctamente.")
            else:
                msg = data.get("message", "Error al enviar a firmar.")
                messagebox.showerror("Error", msg)

        except Exception as e:
            messagebox.showerror("Error", str(e))
