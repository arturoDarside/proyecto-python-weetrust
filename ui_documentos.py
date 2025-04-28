import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import requests
import json
from obtener_token import obtener_token

class DocumentosPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg="#f5f5f7")
        
        # Frame principal con bordes suaves
        main_frame = tk.Frame(self, bg="white", bd=1, relief=tk.SOLID)
        main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        # Cabecera con título
        header_frame = tk.Frame(main_frame, bg="#4a6fa5", pady=10)
        header_frame.pack(fill=tk.X)
        
        tk.Label(header_frame, text="Subir Documento a WeeTrust", 
                font=("Segoe UI", 16, "bold"), bg="#4a6fa5", fg="white").pack(pady=5)
        
        # Contenedor principal
        content_frame = tk.Frame(main_frame, bg="white", padx=25, pady=15)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Sección de selección de archivo
        file_section = tk.LabelFrame(content_frame, text="Archivo PDF", bg="white", fg="#333333", 
                                   font=("Segoe UI", 10, "bold"), padx=10, pady=10)
        file_section.pack(fill=tk.X, pady=10)
        
        self.file_path = tk.StringVar()
        file_frame = tk.Frame(file_section, bg="white")
        file_frame.pack(fill=tk.X)
        
        entry = tk.Entry(file_frame, textvariable=self.file_path, width=60, 
                       font=("Segoe UI", 10), bd=1, relief=tk.SOLID)
        entry.pack(side="left", padx=5, fill=tk.X, expand=True)
        
        select_button = tk.Button(file_frame, text="Seleccionar Archivo", 
                                command=self.seleccionar_archivo, 
                                bg="#3498db", fg="white",
                                font=("Segoe UI", 9),
                                activebackground="#2980b9",
                                padx=10, pady=4, bd=0,
                                cursor="hand2")
        select_button.pack(side="left", padx=5)
        
        # Sección de parámetros
        params_section = tk.LabelFrame(content_frame, text="Parámetros del Documento", 
                                     bg="white", fg="#333333", 
                                     font=("Segoe UI", 10, "bold"), 
                                     padx=10, pady=10)
        params_section.pack(fill=tk.X, pady=10)
        
        # Definición de campos con valores por defecto
        self.campos = {
            "documentSignType": tk.StringVar(value="ELECTRONIC_SIGNATURE"),
            "country": tk.StringVar(value="Mexico"),
            "language": tk.StringVar(value="es"),
            "position": tk.StringVar(value="geolocation"),
            "splitPage": tk.StringVar(value="1,2,3,4,5,6,7,8,9")
        }
        
        # Crear un grid para los campos
        grid_frame = tk.Frame(params_section, bg="white")
        grid_frame.pack(fill=tk.X)
        
        row = 0
        col = 0
        for campo, var in self.campos.items():
            label = tk.Label(grid_frame, text=campo + ":", 
                           width=18, anchor="w", bg="white", 
                           font=("Segoe UI", 9))
            label.grid(row=row, column=col*2, sticky="w", padx=5, pady=6)

            if campo == "documentSignType":
                dropdown = ttk.Combobox(
                grid_frame,
                textvariable=var,
                state="readonly",
                values=["ELECTRONIC_SIGNATURE", "E_FIRMA"],
                width=26,
                font=("Segoe UI", 9)
                )
                dropdown.grid(row=row, column=col*2+1, sticky="w", padx=5, pady=6)

            else:
            
            
             entry = tk.Entry(grid_frame, textvariable=var, width=28, 
                           font=("Segoe UI", 9), bd=1, relief=tk.SOLID)
             entry.grid(row=row, column=col*2+1, sticky="w", padx=5, pady=6)
            
            col += 1
            if col > 1:  # Dos campos por fila
                col = 0
                row += 1
        
        # Sección de acción
        action_frame = tk.Frame(content_frame, bg="white", pady=10)
        action_frame.pack(fill=tk.X)
        
        upload_button = tk.Button(action_frame, text="Subir Documento", 
                                command=self.subir_documento, 
                                bg="#2ecc71", fg="white", 
                                font=("Segoe UI", 11, "bold"),
                                activebackground="#27ae60",
                                padx=15, pady=8, bd=0,
                                cursor="hand2")
        upload_button.pack(pady=5)
        
        # Sección de ID del documento 
        self.id_section = tk.LabelFrame(content_frame, text="ID del Documento", 
                                      bg="white", fg="#333333", 
                                      font=("Segoe UI", 10, "bold"), 
                                      padx=10, pady=10)
        self.id_section.pack(fill=tk.X, pady=10)
        
        self.doc_id_var = tk.StringVar()
        
        id_frame = tk.Frame(self.id_section, bg="white")
        id_frame.pack(fill=tk.X)
        
        self.id_entry = tk.Entry(id_frame, textvariable=self.doc_id_var, 
                               width=60, font=("Segoe UI", 10, "bold"), 
                               bd=1, relief=tk.SOLID, state="readonly", 
                               readonlybackground="#f9f9f9")
        self.id_entry.pack(side="left", padx=5, fill=tk.X, expand=True)
        
        copy_id_button = tk.Button(id_frame, text="Copiar ID", 
                                 command=self.copiar_id_directo, 
                                 bg="#f39c12", fg="white",
                                 font=("Segoe UI", 9, "bold"),
                                 activebackground="#e67e22",
                                 padx=10, pady=4, bd=0,
                                 cursor="hand2")
        copy_id_button.pack(side="left", padx=5)
        
        # Tabla de resultados con mejor estilo
        results_frame = tk.LabelFrame(content_frame, text="Historial de Documentos", 
                                    bg="white", fg="#333333", 
                                    font=("Segoe UI", 10, "bold"), 
                                    padx=10, pady=10)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Estilo para la tabla
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", 
                      background="white",
                      fieldbackground="white", 
                      foreground="#333333",
                      rowheight=30,
                      font=("Segoe UI", 10))
        style.configure("Treeview.Heading", 
                      font=("Segoe UI", 10, "bold"), 
                      background="#e0e0e0",
                      foreground="#333333",
                      padding=5)
        style.map("Treeview", background=[("selected", "#e1f5fe")])
        
        # Tabla y scrollbar
        table_frame = tk.Frame(results_frame, bg="white")
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        self.tree = ttk.Treeview(table_frame, columns=("file_name", "documentID"), show="headings", height=5)
        self.tree.heading("file_name", text="Nombre del Archivo")
        self.tree.heading("documentID", text="ID del Documento")
        self.tree.column("file_name", width=250)
        self.tree.column("documentID", width=350)
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill=tk.BOTH, expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Botón para usar ID seleccionado de la tabla
        table_actions_frame = tk.Frame(results_frame, bg="white", pady=5)
        table_actions_frame.pack(fill=tk.X)
        
        select_button = tk.Button(table_actions_frame, text="Usar ID Seleccionado", 
                                command=self.usar_id_seleccionado, 
                                bg="#3498db", fg="white",
                                font=("Segoe UI", 9),
                                activebackground="#2980b9",
                                padx=10, pady=4, bd=0,
                                cursor="hand2")
        select_button.pack(side="left", padx=5)
        
        # Evento al seleccionar una fila en la tabla
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    def seleccionar_archivo(self):
        archivo = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")])
        if archivo:
            self.file_path.set(archivo)

    def subir_documento(self):
        ruta = self.file_path.get()

        if not os.path.exists(ruta):
            messagebox.showerror("Error", f"El archivo '{ruta}' no existe.")
            return

        # Construir el JSON desde los campos
        data = {clave: var.get() for clave, var in self.campos.items()}

        try:
            token = obtener_token()

            headers = {
                "accept": "application/json",
                "user-id": "kCTmosZegBbnHQBnZw8woqGTGN12",
                "token": token
            }

            with open(ruta, "rb") as file:
                files = {
                    "document": (os.path.basename(ruta), file, "application/pdf"),
                    "data": (None, json.dumps(data), "application/json")
                }

                response = requests.post("https://api.weetrust.mx/documents", headers=headers, files=files)

            if response.status_code == 200:
                json_resp = response.json()
                doc_id = json_resp.get("responseData", {}).get("documentID", "No ID")
                file_name = os.path.basename(ruta)
                
                # Actualizar ID actual
                self.doc_id_var.set(doc_id)
                self.id_entry.config(state="readonly")
                
                # Agregar a la tabla
                self.tree.insert("", "end", values=(file_name, doc_id))
                
                messagebox.showinfo("Éxito", "Documento subido correctamente.")
            else:
                mensaje = response.json().get("message", "Error desconocido")
                messagebox.showerror("Error", f"Error en la solicitud: {mensaje}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def copiar_id_directo(self):
        doc_id = self.doc_id_var.get()
        if doc_id:
            self.clipboard_clear()
            self.clipboard_append(doc_id)
            self.update()  # Actualiza el portapapeles
            messagebox.showinfo("Copiado", f"ID del documento copiado: {doc_id}")
        else:
            messagebox.showwarning("Advertencia", "No hay ID de documento para copiar.")

    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            doc_id = self.tree.item(selected_item, "values")[1]
            self.doc_id_var.set(doc_id)

    def usar_id_seleccionado(self):
        selected_item = self.tree.selection()
        if selected_item:
            doc_id = self.tree.item(selected_item, "values")[1]
            self.doc_id_var.set(doc_id)
            messagebox.showinfo("Seleccionado", f"ID seleccionado: {doc_id}")
        else:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un documento de la tabla.")