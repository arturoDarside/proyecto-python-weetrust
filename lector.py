import imaplib
import email
from email.header import decode_header
import unicodedata
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import pandas as pd
from openpyxl import load_workbook
from scripts import config
import os
import re
import chardet
from pathlib import Path
from datetime import datetime


detener_busqueda = False  # Flag global para detener la lectura

def normalizar_texto(texto):
    if not texto:
        return ""
    if isinstance(texto, bytes):
        try:
            detected = chardet.detect(texto)
            texto = texto.decode(detected['encoding'] or 'utf-8', errors='ignore')
        except:
            texto = texto.decode('utf-8', errors='ignore')
    else:
        texto = str(texto)
    texto = unicodedata.normalize('NFD', texto)
    texto = texto.encode('ascii', 'ignore').decode('utf-8')
    return texto.strip()

def extraer_cuerpo(mensaje):
    cuerpo = ""
    if mensaje.is_multipart():
        for parte in mensaje.walk():
            content_type = parte.get_content_type()
            content_disposition = str(parte.get("Content-Disposition"))
            if "attachment" not in content_disposition and content_type == "text/plain":
                cuerpo = parte.get_payload(decode=True)
                if cuerpo:
                    detected = chardet.detect(cuerpo)
                    cuerpo = cuerpo.decode(detected['encoding'] or 'utf-8', errors='ignore')
                    break
    else:
        cuerpo = mensaje.get_payload(decode=True)
        if cuerpo:
            detected = chardet.detect(cuerpo)
            cuerpo = cuerpo.decode(detected['encoding'] or 'utf-8', errors='ignore')
    return cuerpo.strip()

def extraer_datos_estudiante(cuerpo):
    nombre = re.search(r'nombre[:\-]?\s*(.+)', cuerpo, re.IGNORECASE)
    carrera = re.search(r'carrera[:\-]?\s*(.+)', cuerpo, re.IGNORECASE)
    universidad = re.search(r'universidad[:\-]?\s*(.+)', cuerpo, re.IGNORECASE)
    return {
        "nombre": nombre.group(1).strip() if nombre else "",
        "carrera": carrera.group(1).strip() if carrera else "",
        "universidad": universidad.group(1).strip() if universidad else ""
    }

def guardar_cv_adjuntos(mensaje, nombre_estudiante):
    # Usar carpeta Descargas/CVs del usuario
    carpeta_descargas = Path.home() / "F:/Descargas/" / "CVs"
    carpeta_descargas.mkdir(parents=True, exist_ok=True)

    archivos_guardados = []

    def limpiar_nombre(nombre):
        nombre = unicodedata.normalize("NFD", nombre)
        nombre = nombre.encode("ascii", "ignore").decode("utf-8")
        nombre = re.sub(r'[^\w\-_. ]', '', nombre)
        return nombre.replace(" ", "_").lower()

    nombre_estudiante = limpiar_nombre(nombre_estudiante)

    for parte in mensaje.walk():
        if parte.get_content_maintype() == 'multipart':
            continue
        if parte.get('Content-Disposition') is None:
            continue

        filename = parte.get_filename()
        if filename:
            filename = decode_header(filename)[0][0]
            if isinstance(filename, bytes):
                filename = normalizar_texto(filename)
            filename = limpiar_nombre(filename)

            # Extraer extensión (o usar .pdf por defecto)
            extension = os.path.splitext(filename)[1] or ".pdf"
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_final = f"{nombre_estudiante}_{timestamp}{extension}"

            ruta_completa = carpeta_descargas / nombre_final

            try:
                with open(ruta_completa, "wb") as f:
                    f.write(parte.get_payload(decode=True))
                archivos_guardados.append(str(ruta_completa))
                print(f"📎 CV guardado: {ruta_completa}")
            except Exception as e:
                print(f"⚠ Error al guardar adjunto: {e}")

    return archivos_guardados

def guardar_en_excel(nombre, carrera, universidad, remitente):
    try:
        archivo = "solicitudes_estadia.xlsx"
        nombre = normalizar_texto(nombre)
        carrera = normalizar_texto(carrera)
        universidad = normalizar_texto(universidad)
        remitente = normalizar_texto(remitente)
        df = pd.DataFrame([[nombre, carrera, universidad, remitente]], columns=['Nombre', 'Carrera', 'Universidad', 'Remitente'])

        if not os.path.exists(archivo):
            df.to_excel(archivo, index=False)
        else:
            with pd.ExcelWriter(archivo, engine="openpyxl", mode="a", if_sheet_exists="overlay") as writer:
                df.to_excel(writer, index=False, header=False)
        print("✅ Guardado en Excel correctamente")
    except Exception as e:
        print(f"⚠ Error guardando en Excel: {e}")

def decodificar_asunto(subject_raw):
    decoded_parts = decode_header(subject_raw)
    subject = ''
    for part, encoding in decoded_parts:
        if isinstance(part, bytes):
            try:
                subject += part.decode(encoding or 'utf-8', errors='ignore')
            except:
                subject += part.decode('utf-8', errors='ignore')
        else:
            subject += part
    return subject

def obtener_emails():
    try:
        status_label.config(text="🔍 Conectando al servidor IMAP...")
        root.update()
        print("⏳ Conectando...")
        mail = imaplib.IMAP4_SSL(config.EMAIL_CONFIG[config.EMAIL_PROVIDER]["server"])
        mail.login(config.EMAIL_USER, config.EMAIL_PASS)
        print("✅ Login exitoso")
        mail.select("inbox")

        _, mensajes = mail.search(None, "ALL")  # Leemos todos los correos
        correos_filtrados = []
        total_mensajes = len(mensajes[0].split())
        print(f"🔢 Total de correos encontrados: {total_mensajes}")

        if mensajes and mensajes[0]:
            for num in reversed(mensajes[0].split()):
                if detener_busqueda:
                    print("⛔ Proceso detenido por el usuario.")
                    break
                _, data = mail.fetch(num, "(RFC822)")
                for respuesta in data:
                    if isinstance(respuesta, tuple):
                        mensaje = email.message_from_bytes(respuesta[1])

                        # Decodificar y normalizar el asunto
                        asunto_raw = mensaje["Subject"]
                        asunto_decodificado = decodificar_asunto(asunto_raw)
                        asunto_normalizado = normalizar_texto(asunto_decodificado).lower()

                        print(f"📬 Asunto detectado: {asunto_normalizado}")

                        # Coincidencias que aceptamos
                        if not any(keyword in asunto_normalizado for keyword in [
                            "solicitud de estadia", "practicas", "estadia profesional"
                        ]):
                            print("⛔ Correo ignorado, no contiene keywords.")
                            continue

                        remitente = mensaje["From"]
                        remitente = normalizar_texto(remitente)
                        cuerpo = extraer_cuerpo(mensaje)
                        datos = extraer_datos_estudiante(cuerpo)
                        print(f"🧾 Datos extraídos: {datos}")
                        datos["remitente"] = remitente

                        guardar_en_excel(datos["nombre"], datos["carrera"], datos["universidad"], remitente)
                        guardar_cv_adjuntos(mensaje, datos["nombre"])
                        correos_filtrados.append(datos)
                        tabla.insert("", "end", values=(
                            datos["nombre"], datos["carrera"], datos["universidad"], remitente
                        ))
                        root.update()

        status_label.config(text=f"✅ {len(correos_filtrados)} correos procesados.")
        mail.close()
        mail.logout()

    except Exception as e:
        messagebox.showerror("Error", f"⚠ Error al leer correos: {e}")
        print(f"❌ Excepción: {e}")


def iniciar_proceso():
    global detener_busqueda
    detener_busqueda = False
    threading.Thread(target=obtener_emails, daemon=True).start()

def detener_proceso():
    global detener_busqueda
    detener_busqueda = True
    status_label.config(text="⛔ Búsqueda detenida por el usuario.")

def finalizar_proceso():
    root.quit()
    root.destroy()

# INTERFAZ
root = tk.Tk()
root.title("Lector de Solicitudes de Estadia/Practicas")
root.geometry("700x450")

frame = tk.Frame(root)
frame.pack(pady=10)

status_label = tk.Label(frame, text="🔍 Esperando accion...", font=("Arial", 10))
status_label.pack()

btn_iniciar = tk.Button(frame, text="Leer Correos", command=iniciar_proceso, bg="lightblue", font=("Arial", 12))
btn_iniciar.pack(pady=5)

btn_detener = tk.Button(frame, text="Detener Búsqueda", command=detener_proceso, bg="orange", font=("Arial", 12))
btn_detener.pack(pady=5)


btn_finalizar = tk.Button(frame, text="Finalizar Ejecucion", command=finalizar_proceso, bg="red", font=("Arial", 12))
btn_finalizar.pack(pady=5)

cols = ('Nombre', 'Carrera', 'Universidad', 'Remitente')
tabla = ttk.Treeview(root, columns=cols, show='headings')
for col in cols:
    tabla.heading(col, text=col)
    tabla.column(col, width=160)
tabla.pack(pady=10, fill='x', expand=True)

root.mainloop()
