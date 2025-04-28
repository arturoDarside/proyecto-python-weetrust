import tkinter as tk
from tkinter import messagebox, ttk
import json
import requests
from obtener_token import obtener_token  # Función para obtener el token

class FirmarPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg="#f5f5f7")
        
        # Frame principal con bordes suaves
        main_frame = tk.Frame(self, bg="white", bd=1, relief=tk.SOLID)
        main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        # Cabecera con título
        header_frame = tk.Frame(main_frame, bg="#5d3b8c", pady=10)
        header_frame.pack(fill=tk.X)
        
        tk.Label(header_frame, text="Enviar Documento para Firma", 
                font=("Segoe UI", 16, "bold"), bg="#5d3b8c", fg="white").pack(pady=5)
        
        # Contenedor principal
        content_frame = tk.Frame(main_frame, bg="white", padx=25, pady=15)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Sección de configuración del documento
        doc_section = tk.LabelFrame(content_frame, text="Datos del Documento", 
                                   bg="white", fg="#333333", 
                                   font=("Segoe UI", 10, "bold"), padx=15, pady=15)
        doc_section.pack(fill=tk.X, pady=10)
        
        # Definición de campos principales
        self.campos = {
            "documentID": tk.StringVar(),
            "nickname": tk.StringVar(),
            "message": tk.StringVar(),
            "title": tk.StringVar(),
            "hasOrder": tk.StringVar(value="False"),
            "disableMailing": tk.StringVar(value="False")
        }
        
        # Crear layout de campos
        fields_frame = tk.Frame(doc_section, bg="white")
        fields_frame.pack(fill=tk.X)
        
        row = 0
        col = 0
        for campo, var in self.campos.items():
            field_frame = tk.Frame(fields_frame, bg="white", pady=5)
            field_frame.grid(row=row, column=col, padx=10, pady=3, sticky="w")
            
            label = tk.Label(field_frame, text=campo + ":", 
                           font=("Segoe UI", 9), 
                           bg="white", anchor="w", width=15)
            label.pack(side=tk.LEFT)
            
            if campo in ["hasOrder", "disableMailing"]:
                # Opciones Sí/No para campos booleanos
                options_frame = tk.Frame(field_frame, bg="white")
                options_frame.pack(side=tk.LEFT)
                
                tk.Radiobutton(options_frame, text="No", variable=var, value="False", 
                             bg="white", font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=5)
                tk.Radiobutton(options_frame, text="Sí", variable=var, value="True", 
                             bg="white", font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=5)
            else:
                entry = tk.Entry(field_frame, textvariable=var, 
                               font=("Segoe UI", 9), width=30, 
                               bd=1, relief=tk.SOLID)
                entry.pack(side=tk.LEFT, padx=5)
            
            col += 1
            if col > 1:  # Dos columnas
                col = 0
                row += 1
        
        # Sección de signatarios
        sign_section = tk.LabelFrame(content_frame, text="Signatarios", 
                                   bg="white", fg="#333333", 
                                   font=("Segoe UI", 10, "bold"), padx=15, pady=10)
        sign_section.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Estilo para la tabla
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", 
                      background="white",
                      fieldbackground="white", 
                      foreground="#333333",
                      rowheight=30,
                      font=("Segoe UI", 9))
        style.configure("Treeview.Heading", 
                      font=("Segoe UI", 9, "bold"), 
                      background="#e0e0e0",
                      foreground="#333333",
                      padding=5)
        style.map("Treeview", background=[("selected", "#e8f4fc")])
        
        # Tabla y scrollbar
        table_frame = tk.Frame(sign_section, bg="white")
        table_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.tree = ttk.Treeview(table_frame, 
                               columns=("emailID", "name", "phone", "identification"), 
                               show="headings", height=4)
        
        # Configurar columnas
        self.tree.heading("emailID", text="Correo Electrónico")
        self.tree.heading("name", text="Nombre")
        self.tree.heading("phone", text="Teléfono")
        self.tree.heading("identification", text="Identificación")
        
        self.tree.column("emailID", width=180)
        self.tree.column("name", width=150)
        self.tree.column("phone", width=120)
        self.tree.column("identification", width=120)
        
        # Scrollbars
        y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=y_scroll.set)
        
        self.tree.pack(side="left", fill=tk.BOTH, expand=True)
        y_scroll.pack(side="right", fill="y")
        
        # Botones de acción para signatarios
        btn_frame = tk.Frame(sign_section, bg="white", pady=5)
        btn_frame.pack(fill=tk.X)
        
        add_btn = tk.Button(btn_frame, text="Agregar Signatario", 
                          command=self.agregar_signatario, 
                          bg="#3498db", fg="white",
                          font=("Segoe UI", 9),
                          activebackground="#2980b9",
                          padx=10, pady=3, bd=0,
                          cursor="hand2")
        add_btn.pack(side=tk.LEFT, padx=5)
        
        remove_btn = tk.Button(btn_frame, text="Eliminar Seleccionado", 
                             command=self.eliminar_signatario, 
                             bg="#e74c3c", fg="white",
                             font=("Segoe UI", 9),
                             activebackground="#c0392b",
                             padx=10, pady=3, bd=0,
                             cursor="hand2")
        remove_btn.pack(side=tk.LEFT, padx=5)
        
        # Botón final para enviar
        submit_frame = tk.Frame(content_frame, bg="white", pady=10)
        submit_frame.pack(fill=tk.X)
        
        send_btn = tk.Button(submit_frame, text="Enviar para Firma", 
                           command=self.enviar_para_firma, 
                           bg="#2ecc71", fg="white",
                           font=("Segoe UI", 12, "bold"),
                           activebackground="#27ae60",
                           padx=20, pady=10, bd=0,
                           width=20,
                           cursor="hand2",
                           anchor="center")
        send_btn.pack(pady=3)
        
        self.signatarios = []  # Lista para almacenar los signatarios

    def agregar_signatario(self):
        # Ventana para agregar un nuevo signatario
        popup = tk.Toplevel(self)
        popup.title("Agregar Signatario")
        popup.geometry("450x400")
        popup.configure(bg="white")
        popup.resizable(False, False)
        
        # Título de la ventana popup
        title_frame = tk.Frame(popup, bg="#3498db")
        title_frame.pack(fill=tk.X)
        
        tk.Label(title_frame, text="Agregar Nuevo Signatario", 
               font=("Segoe UI", 12, "bold"), 
               bg="#3498db", fg="white",
               padx=15, pady=10).pack(anchor="w")
        
        # Contenido del popup
        content = tk.Frame(popup, bg="white", padx=20, pady=15)
        content.pack(fill=tk.BOTH, expand=True)
        
        # Campos del signatario
        campos_signatario = {
            "emailID": tk.StringVar(),
            "name": tk.StringVar(),
            "identification": tk.StringVar(value="FACE"),
            "check": tk.StringVar(value="False"),
            "phone": tk.StringVar(),
            "customerId": tk.StringVar()  # NUEVO
        }

        frames = {}
        
        # Crear entradas para los campos
        for i, (campo, var) in enumerate(campos_signatario.items()):
            if campo == "costomerId":
                continue
            frame = tk.Frame(content, bg="white", pady=8)
            frame.pack(fill=tk.X)
            frames[campo] = frame
            
            tk.Label(frame, text=campo + ":", 
                   width=15, anchor="w", 
                   bg="white", font=("Segoe UI", 10)).pack(side="left")
            
            if campo == "identification":
                # Menú desplegable para identificación
                combobox = ttk.Combobox(frame, textvariable=var, 
                                      state="readonly", width=25,
                                      font=("Segoe UI", 9))
                combobox["values"] = ["FACE", "FACE_LOGIN"]
                combobox.current(0)  # Seleccionar el primer valor
                combobox.pack(side="left", padx=5, fill=tk.X, expand=True)
            elif campo == "check":
                # Opciones Sí/No para check
                options_frame = tk.Frame(frame, bg="white")
                options_frame.pack(side="left", padx=5)
                
                tk.Radiobutton(options_frame, text="No", variable=var, value="False", 
                             bg="white", font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=5)
                tk.Radiobutton(options_frame, text="Sí", variable=var, value="True", 
                             bg="white", font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=5)
            else:
                # Entrada normal para otros campos
                entry = tk.Entry(frame, textvariable=var, 
                               width=25, font=("Segoe UI", 9),
                               bd=1, relief=tk.SOLID)
                entry.pack(side="left", padx=5, fill=tk.X, expand=True)

        # 👉 Campo dinámico: customerId
            customer_id_frame = tk.Frame(content, bg="white", pady=8)
            tk.Label(customer_id_frame, text="customerId:",
             width=15, anchor="w",
             bg="white", font=("Segoe UI", 10)).pack(side="left")
            tk.Entry(customer_id_frame, textvariable=campos_signatario["customerId"],
             width=25, font=("Segoe UI", 9), bd=1, relief=tk.SOLID).pack(side="left", padx=5)

        # Mostrar/Ocultar customerId según identificación
        def toggle_customer_id(*args):
         if campos_signatario["identification"].get() == "FACE_LOGIN":
            customer_id_frame.pack(fill=tk.X)
         else:
            customer_id_frame.pack_forget()

        campos_signatario["identification"].trace("w", toggle_customer_id)
        toggle_customer_id()  # Ejecutar una vez al inicio   
        
        
        # Botones de acción
        button_frame = tk.Frame(content, bg="white", pady=10)
        button_frame.pack(fill=tk.X)
        
        tk.Button(button_frame, text="Cancelar", 
                command=popup.destroy, 
                bg="#95a5a6", fg="white",
                font=("Segoe UI", 10),
                activebackground="#7f8c8d",
                padx=15, pady=5, bd=0).pack(side="right", padx=5)
        
        tk.Button(button_frame, text="Guardar", 
                command=lambda: self.guardar_signatario(campos_signatario, popup), 
                bg="#2ecc71", fg="white",
                font=("Segoe UI", 10, "bold"),
                activebackground="#27ae60",
                padx=15, pady=5, bd=0).pack(side="right", padx=5)

    def guardar_signatario(self, campos_signatario, popup):
        # Validar datos (ejemplo básico)
        email = campos_signatario["emailID"].get()
        name = campos_signatario["name"].get()
        
        if not email or not name:
            messagebox.showwarning("Datos incompletos", "El correo y nombre son obligatorios.")
            return
        
        # Agregar los datos del signatario a la lista y tabla
        signatario = {campo: var.get() for campo, var in campos_signatario.items()}
        self.signatarios.append(signatario)
        
        self.tree.insert("", "end", values=(
            signatario["emailID"], 
            signatario["name"], 
            signatario["phone"], 
            signatario["identification"]
        ))
        
        popup.destroy()
    
    def eliminar_signatario(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selección", "Por favor selecciona un signatario para eliminar.")
            return
            
        # Obtener el índice del elemento seleccionado
        index = self.tree.index(selected_item[0])
        
        # Eliminar de la lista y de la tabla
        if 0 <= index < len(self.signatarios):
            del self.signatarios[index]
            self.tree.delete(selected_item)
            messagebox.showinfo("Eliminado", "Signatario eliminado correctamente.")

    def enviar_para_firma(self):
        # Validaciones básicas
        if not self.campos["documentID"].get():
            messagebox.showwarning("Datos incompletos", "El ID del documento es obligatorio.")
            return
            
        if not self.signatarios:
            messagebox.showwarning("Sin signatarios", "Debe agregar al menos un signatario.")
            return
        
        # Construir el payload desde los campos
        payload = {clave: var.get() for clave, var in self.campos.items()}
        payload["hasOrder"] = payload["hasOrder"] == "True"  # Convertir a booleano
        payload["disableMailing"] = payload["disableMailing"] == "True"  # Convertir a booleano
        payload["signatory"] = self.signatarios
        
        try:
            token = obtener_token()
            headers = {
                "accept": "application/json",
                "user-id": "kCTmosZegBbnHQBnZw8woqGTGN12",
                "token": token,
                "content-type": "application/json"
            }
            
            # Mostrar indicador de progreso
            progress_popup = tk.Toplevel(self)
            progress_popup.title("Enviando...")
            progress_popup.geometry("300x100")
            progress_popup.configure(bg="white")
            progress_popup.resizable(False, False)
            
            tk.Label(progress_popup, text="Enviando documento para firma...", 
                   font=("Segoe UI", 10), bg="white").pack(pady=15)
            
            progress = ttk.Progressbar(progress_popup, mode="indeterminate")
            progress.pack(fill=tk.X, padx=20)
            progress.start()
            
            # Actualizar la interfaz
            self.update()
            
            # Realizar la solicitud
            response = requests.put("https://api.weetrust.mx/documents/signatory", json=payload, headers=headers)
            
            # Cerrar el indicador de progreso
            progress_popup.destroy()
            
            if response.status_code == 200:
                messagebox.showinfo("Éxito", "Documento enviado para firma correctamente.")
                # Limpiar campos después de éxito
                for var in self.campos.values():
                    var.set("")
                self.tree.delete(*self.tree.get_children())
                self.signatarios.clear()
            else:
                mensaje = response.json().get("message", "Error desconocido")
                messagebox.showerror("Error", f"Error en la solicitud: {mensaje}")
        except Exception as e:
            messagebox.showerror("Error", str(e))