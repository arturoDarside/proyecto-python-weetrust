import tkinter as tk
from tkinter import ttk, messagebox
import os
import time
from datetime import datetime
import webbrowser

class VerificarPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg='white')
        self.parent = parent
        
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
        
        # Simular carga (en una aplicación real, aquí iría tu lógica de actualización)
        self.after(100, lambda: self.progress.step(20))
        self.after(200, lambda: self.progress.step(40))
        self.after(300, lambda: self.progress.step(60))
        self.after(400, lambda: self.progress.step(80))
        self.after(500, self.finalizar_actualizacion)

    def finalizar_actualizacion(self):
        """Finaliza el proceso de actualización"""
        self.progress['value'] = 100
        
        try:
            # Aquí va tu lógica de actualización real
            firmantes_encontrados = self.actualizar_lista()
            
            if not firmantes_encontrados:
                self.actualizar_mensaje("No hay firmantes registrados. Favor de revisar en WeeTrust", "red")
            else:
                self.actualizar_mensaje(f"Se encontraron {firmantes_encontrados} firmante(s)", "green")
                
            # Simular un error aleatorio (para demostración)
            import random
            if random.random() < 0.2:  # 20% de probabilidad de error
                raise Exception("Error de conexión con WeeTrust")
                
        except Exception as e:
            self.actualizar_mensaje(f"Advertencia: {str(e)}. Favor de compilar datos", "red")
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")
        finally:
            self.progress.pack_forget()
            self.btn_actualizar.config(state='normal')

    def actualizar_lista(self):
        """Carga los firmantes desde el archivo con los nombres específicos"""
        self.limpiar_lista()
        firmantes_encontrados = 0
        
        try:
            # Leer el archivo de firmantes
            if not os.path.exists("firmantes.txt"):
                self.tree.insert('', 'end', values=("No se encontró el archivo de firmantes", "", ""))
                return 0
                
            with open("firmantes.txt", "r") as f:
                correos = [line.strip() for line in f.readlines() if line.strip()]
                
            if not correos:
                self.tree.insert('', 'end', values=("No hay firmantes registrados", "", ""))
                return 0
            else:
                # Contar cuántas veces ha firmado cada persona
                conteo = {}
                for correo in correos:
                    conteo[correo] = conteo.get(correo, 0) + 1
                
                # Agregar firmantes a la lista con los nombres específicos
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

if __name__ == "__main__":
    # Crear archivo de ejemplo con los correos que proporcionaste
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
    
    # Iniciar la aplicación
    app = MainApp()
    app.mainloop()