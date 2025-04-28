import tkinter as tk
from tkinter import ttk, messagebox
import requests
from obtener_token import obtener_token

class PlantillasPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Colores y estilos modernos
        self.COLOR_PRIMARY = "#2c3e50"       # Azul oscuro para el fondo principal
        self.COLOR_SECONDARY = "#3498db"     # Azul claro para botones principales
        self.COLOR_ACCENT = "#2ecc71"        # Verde para acciones positivas
        self.COLOR_LIGHT = "#ecf0f1"         # Color claro para fondos
        self.COLOR_DARK = "#34495e"          # Color oscuro para textos
        
        self.configure(bg=self.COLOR_LIGHT, padx=20, pady=20)
        
        # Crear marco principal con efecto de elevación (sombra)
        main_frame = tk.Frame(self, bg=self.COLOR_LIGHT, padx=15, pady=15, 
                              highlightbackground=self.COLOR_DARK, highlightthickness=1)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título con estilo mejorado
        header_frame = tk.Frame(main_frame, bg=self.COLOR_PRIMARY)
        header_frame.pack(fill="x", pady=(0, 15))
        
        title_label = tk.Label(header_frame, text="PLANTILLAS DISPONIBLES", 
                          font=("Helvetica", 16, "bold"), bg=self.COLOR_PRIMARY, 
                          fg="white", pady=10)
        title_label.pack()
        
        # Panel de control con búsqueda y botones
        control_panel = tk.Frame(main_frame, bg=self.COLOR_LIGHT)
        control_panel.pack(fill="x", pady=10)
        
        # Marco para búsqueda con borde redondeado
        search_frame = tk.Frame(control_panel, bg=self.COLOR_LIGHT, pady=5)
        search_frame.pack(side="left", fill="x", expand=True)
        
        search_label = tk.Label(search_frame, text="Buscar:", 
                           font=("Helvetica", 10, "bold"), bg=self.COLOR_LIGHT, fg=self.COLOR_DARK)
        search_label.pack(side="left", padx=5)
        
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=30, 
                           font=("Helvetica", 10), bd=0, bg="white")
        search_entry.pack(side="left", ipady=5, padx=5)
        search_entry.configure(highlightthickness=1, highlightbackground="#bdc3c7")
        
        # Botón de búsqueda estilizado
        search_button = tk.Button(search_frame, text="Buscar", command=self.filtrar_plantillas,
                             bg=self.COLOR_SECONDARY, fg="white", relief="flat",
                             font=("Helvetica", 9, "bold"), padx=15, pady=5,
                             activebackground=self.COLOR_PRIMARY, cursor="hand2")
        search_button.pack(side="left", padx=5)
        
        # Botón para obtener plantillas en el lado derecho
        button_frame = tk.Frame(control_panel, bg=self.COLOR_LIGHT)
        button_frame.pack(side="right", padx=5)
        
        refresh_button = tk.Button(button_frame, text="Obtener Plantillas", command=self.obtener_plantillas,
                               bg=self.COLOR_ACCENT, fg="white", relief="flat",
                               font=("Helvetica", 9, "bold"), padx=15, pady=5,
                               activebackground="#27ae60", cursor="hand2")
        refresh_button.pack(side="right")
        
        # Crear estilo personalizado para la tabla
        style = ttk.Style()
        style.theme_use("clam")  # Tema base limpio
        
        # Configurar el estilo del Treeview
        style.configure("Treeview", 
                        background=self.COLOR_LIGHT,
                        foreground=self.COLOR_DARK,
                        rowheight=25,
                        fieldbackground=self.COLOR_LIGHT,
                        font=("Helvetica", 9))
        
        style.configure("Treeview.Heading", 
                        font=("Helvetica", 10, "bold"),
                        background=self.COLOR_PRIMARY,
                        foreground="white")
        
        style.map("Treeview", background=[("selected", self.COLOR_SECONDARY)])
        
        # Frame contenedor para la tabla y la barra de desplazamiento
        table_frame = tk.Frame(main_frame)
        table_frame.pack(fill="both", expand=True, pady=10)
        
        # Tabla para mostrar las plantillas
        self.tree = ttk.Treeview(
            table_frame,
            columns=("name", "status", "description", "templateID", "keyPDF"),
            show="headings",
            height=12
        )
        
        # Configuración de columnas
        self.tree.heading("name", text="Nombre")
        self.tree.heading("status", text="Estado")
        self.tree.heading("description", text="Descripción")
        self.tree.heading("templateID", text="Template ID")
        self.tree.heading("keyPDF", text="Key PDF")
        
        # Ajuste de tamaño de columnas
        self.tree.column("name", width=200, anchor="w")
        self.tree.column("status", width=80, anchor="center")
        self.tree.column("description", width=200, anchor="w")
        self.tree.column("templateID", width=250, anchor="w")
        self.tree.column("keyPDF", width=250, anchor="w")
        
        # Scrollbar vertical con estilo
        scrollbar_y = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)
        
        # Scrollbar horizontal
        scrollbar_x = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=scrollbar_x.set)
        
        # Colocar elementos con grid para mejor control
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")
        
        # Configurar expansión en el grid
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Barra de estado en la parte inferior
        status_frame = tk.Frame(main_frame, bg=self.COLOR_PRIMARY, height=25)
        status_frame.pack(fill="x", side="bottom", pady=(10, 0))
        
        status_label = tk.Label(status_frame, text="Doble clic en una plantilla para copiar su ID", 
                           bg=self.COLOR_PRIMARY, fg="white", font=("Helvetica", 9))
        status_label.pack(side="left", padx=10, pady=3)
        
        # Asociar evento doble clic
        self.tree.bind("<Double-1>", self.copiar_template_id)
        
        # Variable para almacenar las plantillas
        self.plantillas = []
        
        # Agregar efecto hover a los botones
        for button in [search_button, refresh_button]:
            button.bind("<Enter>", lambda e, b=button: self.on_hover(e, b))
            button.bind("<Leave>", lambda e, b=button: self.on_leave(e, b))
    
    def on_hover(self, event, button):
        """Efecto al pasar el cursor sobre el botón"""
        if button["text"] == "Buscar":
            button.config(bg="#2980b9")
        else:
            button.config(bg="#27ae60")
    
    def on_leave(self, event, button):
        """Efecto al quitar el cursor del botón"""
        if button["text"] == "Buscar":
            button.config(bg=self.COLOR_SECONDARY)
        else:
            button.config(bg=self.COLOR_ACCENT)
    
    def obtener_plantillas(self):
        try:
            token = obtener_token()
            headers = {
                "accept": "application/json",
                "user-id": "kCTmosZegBbnHQBnZw8woqGTGN12",
                "token": token
            }

            url = "https://api.weetrust.mx/templates/v2"
            response = requests.get(url, headers=headers)
            print(response.text)

            if response.status_code == 200:
                json_resp = response.json()
                self.plantillas = json_resp.get("responseData", {}).get("templates", [])
                
                if not self.plantillas:
                    messagebox.showinfo("Sin datos", "No se encontraron plantillas disponibles.")
                    return

                self.tree.delete(*self.tree.get_children())

                # Alternar colores de fondo para las filas
                for i, plantilla in enumerate(self.plantillas):
                    rowcolor = "#f9f9f9" if i % 2 == 0 else "white"
                    item_id = self.tree.insert(
                        "", "end",
                        values=(
                            plantilla["name"],
                            plantilla["status"],
                            plantilla.get("description", ""),
                            plantilla.get("templateID", ""),
                            plantilla.get("keyPDF", "")
                        )
                    )
                    # Aplicar color alternado a las filas
                    self.tree.item(item_id, tags=(f"row{i}",))
                    self.tree.tag_configure(f"row{i}", background=rowcolor)

                messagebox.showinfo("Éxito", "Plantillas obtenidas correctamente.")
            else:
                mensaje = response.json().get("message", "Error desconocido")
                messagebox.showerror("Error", f"No se pudo obtener las plantillas: {mensaje}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def filtrar_plantillas(self):
        query = self.search_var.get().lower()
        filtered = [p for p in self.plantillas if query in p["name"].lower()]

        self.tree.delete(*self.tree.get_children())

        if not filtered:
            messagebox.showinfo("Sin resultados", "No se encontraron plantillas con ese nombre.")
            return

        # Alternar colores de fondo para las filas
        for i, plantilla in enumerate(filtered):
            rowcolor = "#f9f9f9" if i % 2 == 0 else "white"
            item_id = self.tree.insert(
                "", "end",
                values=(
                    plantilla["name"],
                    plantilla["status"],
                    plantilla.get("description", ""),
                    plantilla.get("templateID", ""),
                    plantilla.get("keyPDF", "")
                )
            )
            # Aplicar color alternado a las filas
            self.tree.item(item_id, tags=(f"row{i}",))
            self.tree.tag_configure(f"row{i}", background=rowcolor)

    def copiar_template_id(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item[0], "values")
            template_id = values[3]  # templateID está en la columna 4
            self.clipboard_clear()
            self.clipboard_append(template_id)
            self.update()
            messagebox.showinfo("Copiado", f"Template ID copiado al portapapeles:\n{template_id}")

# Para probar el panel (descomentar para pruebas)
# if __name__ == "__main__":
#     root = tk.Tk()
#     root.title("Gestor de Plantillas")
#     root.geometry("1000x600")
#     app = PlantillasPanel(root)
#     app.pack(fill="both", expand=True)
#     root.mainloop()