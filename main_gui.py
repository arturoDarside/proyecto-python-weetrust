import tkinter as tk
from tkinter import ttk
import subprocess
import ui_token
import ui_documentos
from ui_firmar import FirmarPanel
from ui_plantillas import PlantillasPanel
from ui_enviarplantillas import FirmaPanel
from ui_recordatorios import NotificacionesPanel
from ui_lector import LectorPanel
from ui_verificar import VerificarPanel

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("RPA Weetrust")
        self.geometry("1000x600")
        self.minsize(800, 500)
        self.configure(bg='#f4f4f4')

        self.menu_frame = tk.Frame(self, bg='#2c3e50', width=200)
        self.menu_frame.pack(side='left', fill='y')

        self.content_frame = tk.Frame(self, bg='white')
        self.content_frame.pack(side='right', expand=True, fill='both')

        # Botones del menú
        self.botones = [
            ("Token", self.mostrar_token),
            ("Documentos", self.mostrar_documentos),
            ("Firmar", self.mostrar_firmar),
            ("Plantillas", self.mostrar_plantillas),
            ("Enviar Plantilla", self.mostrar_enviar_plantilla),
            ("Notificaciones", self.mostrar_notificaciones),
            ("Lector", self.mostrar_lector_correos),
            ("Verificar", self.mostrar_verificar)
        ]

        for texto, comando in self.botones:
            btn = tk.Button(self.menu_frame, text=texto, font=("Arial", 12), bg='#34495e', fg='white', relief='flat', command=comando)
            btn.pack(fill='x', padx=10, pady=5)

        # Frame de contenido inicial
        self.label_inicio = tk.Label(self.content_frame, text="Selecciona una opción del menú", font=("Arial", 14), bg='white')
        self.label_inicio.pack(pady=50)

    # Métodos de cambio de vista
    def limpiar_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def mostrar_token(self):
        self.limpiar_frame()
        token_panel = ui_token.TokenPanel(self.content_frame)
        token_panel.pack(expand=True, fill='both')
        
    def mostrar_documentos(self):
        self.limpiar_frame()
        panel = ui_documentos.DocumentosPanel(self.content_frame)
        panel.pack(expand=True, fill='both')

    def mostrar_firmar(self):
        self.limpiar_frame()
        tk.Label(self.content_frame, text="Sección: Firmar", font=("Arial", 14), bg='white').pack(pady=20)
        firmar_panel = FirmarPanel(self.content_frame)
        firmar_panel.pack(fill="both", expand=True)

    def mostrar_plantillas(self):
        self.limpiar_frame()
        tk.Label(self.content_frame, text="Sección: Plantillas", font=("Arial", 14), bg='white').pack(pady=20)
        plantillas_panel = PlantillasPanel(self.content_frame)
        plantillas_panel.pack(fill="both", expand=True)

    def mostrar_enviar_plantilla(self):
        self.limpiar_frame()
        panel = FirmaPanel(self.content_frame)
        panel.pack(fill="both", expand=True)

    def mostrar_notificaciones(self):
        self.limpiar_frame()
        notificaciones_panel = NotificacionesPanel(self.content_frame)
        notificaciones_panel.pack(fill="both", expand=True)

    def mostrar_lector_correos(self):
        self.limpiar_frame()
        lector_panel = LectorPanel(self.content_frame)
        lector_panel.pack(fill="both", expand=True)

    def mostrar_verificar(self):
        self.limpiar_frame()
        verificar_panel = VerificarPanel(self.content_frame)
        verificar_panel.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()