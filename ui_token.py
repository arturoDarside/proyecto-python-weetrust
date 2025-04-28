import tkinter as tk
from tkinter import messagebox, ttk
import subprocess
import os
from datetime import datetime

class TokenPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg="#f5f5f7")  # Fondo gris claro más moderno
        
        # Frame principal con sombra simulada
        main_frame = tk.Frame(self, bg="white", bd=1, relief=tk.SOLID)
        main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        # Título con mejor diseño
        title_frame = tk.Frame(main_frame, bg="#3498db")
        title_frame.pack(fill=tk.X)
        
        self.label = tk.Label(title_frame, text="Generar Token de Acceso", 
                             font=("Segoe UI", 16, "bold"), bg="#3498db", fg="white", 
                             padx=15, pady=12)
        self.label.pack(anchor="w")
        
        # Contenido
        content_frame = tk.Frame(main_frame, bg="white", padx=20, pady=15)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Botón moderno con efecto hover
        self.btn_generar = tk.Button(content_frame, text="Generar Token", 
                                   command=self.generar_token, 
                                   bg="#2ecc71", fg="white", 
                                   font=("Segoe UI", 12),
                                   activebackground="#27ae60", 
                                   activeforeground="white",
                                   bd=0, padx=15, pady=8,
                                   cursor="hand2")
        self.btn_generar.pack(pady=15)
        
        # Etiqueta de estado con mejor visualización
        self.status_frame = tk.Frame(content_frame, bg="white")
        self.status_frame.pack(fill=tk.X, pady=5)
        
        self.status_label = tk.Label(self.status_frame, text="", 
                                   font=("Segoe UI", 11), 
                                   bg="white", fg="green")
        self.status_label.pack(pady=5)
        
        # Estilo para la tabla
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", 
                      background="white",
                      fieldbackground="white", 
                      foreground="black",
                      rowheight=30,
                      font=("Segoe UI", 10))
        style.configure("Treeview.Heading", 
                      font=("Segoe UI", 10, "bold"), 
                      background="#e0e0e0",
                      foreground="black",
                      padding=5)
        style.map("Treeview", background=[("selected", "#e1f5fe")])
        
        # Tabla con token y hora
        table_frame = tk.Frame(content_frame, bg="white", bd=1, relief=tk.SOLID)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.tree = ttk.Treeview(table_frame, columns=("token", "fecha"), show="headings", height=2)
        self.tree.heading("token", text="Token")
        self.tree.heading("fecha", text="Fecha de Generación")
        self.tree.column("token", width=400)
        self.tree.column("fecha", width=180)
        self.tree.pack(fill=tk.BOTH, expand=True, pady=5, padx=5)

    def generar_token(self):
        try:
            subprocess.run(["python", "pruebatoken.py"], check=True)

            if os.path.exists("token.txt"):
                with open("token.txt", "r") as f:
                    token = f.readline().strip()
                    fecha = f.readline().strip()

                self.tree.delete(*self.tree.get_children())  # limpiar
                self.tree.insert("", "end", values=(token, fecha))
                self.status_label.config(text="✅ Token generado correctamente", fg="#27ae60")

            else:
                self.status_label.config(text="⚠️ No se encontró el archivo token.txt", fg="#e74c3c")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el token:\n{e}")