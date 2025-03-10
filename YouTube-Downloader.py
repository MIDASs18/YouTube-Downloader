import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import threading
import time
import subprocess
import sys
import platform

def verificar_dependencias(lista_descargas):
    """Verifica e instala las dependencias necesarias (yt-dlp y FFmpeg) si está activado en la configuración"""
    # Cargar configuración
    config = cargar_configuracion()
    
    # Verificar si está activada la verificación de dependencias
    if config["VERIFICAR_DEPENDENCIAS"].lower() != "true":
        lista_descargas.insert(tk.END, "Verificación de dependencias desactivada en configuración.")
        return True
    
    lista_descargas.insert(tk.END, "Verificando dependencias...")
    if not verificar_ytdlp(lista_descargas):
        return False
    
    # Verificar FFmpeg
    if not verificar_ffmpeg(lista_descargas):
        return False
    
    lista_descargas.insert(tk.END, "✅ Todas las dependencias están instaladas.")
    return True

def verificar_ytdlp(lista_descargas):
    """Verifica si yt-dlp está instalado y lo instala si no lo está"""
    try:
        lista_descargas.insert(tk.END, "Verificando yt-dlp...")
        lista_descargas.see(tk.END)
        
        # Usar importación directa para verificar si yt-dlp está instalado
        try:
            import yt_dlp
            lista_descargas.insert(tk.END, "✅ yt-dlp ya está instalado.")
            lista_descargas.see(tk.END)
            return True
        except ImportError:
            # No está instalado, intentar instalarlo
            mensaje = "La herramienta yt-dlp no está instalada. Se instalará automáticamente."
            lista_descargas.insert(tk.END, mensaje)
            lista_descargas.see(tk.END)
            messagebox.showinfo("Instalación necesaria", mensaje)
            
            lista_descargas.insert(tk.END, "Instalando yt-dlp... (puede tardar un momento)")
            lista_descargas.see(tk.END)
            
            startupinfo = None
            if platform.system() == "Windows":
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = 0  # SW_HIDE
            
            cmd = [sys.executable, '-m', 'pip', 'install', 'yt-dlp', '--quiet']
            
            if platform.system() == "Windows":
                process = subprocess.Popen(
                    " ".join(cmd),
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    startupinfo=startupinfo
                )
            else:
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                error = stderr.decode('utf-8', errors='replace')
                lista_descargas.insert(tk.END, f"❌ Error al instalar yt-dlp: {error}")
                lista_descargas.see(tk.END)
                messagebox.showerror("Error", "No se pudo instalar yt-dlp. Por favor instálalo manualmente con 'pip install yt-dlp'.")
                return False
            else:
                lista_descargas.insert(tk.END, "✅ yt-dlp instalado correctamente.")
                lista_descargas.see(tk.END)
                # Intentar importar de nuevo para asegurarse de que está disponible
                try:
                    import importlib
                    importlib.invalidate_caches()  # Limpiar caché de importación
                    import yt_dlp
                    return True
                except ImportError:
                    lista_descargas.insert(tk.END, "⚠️ Se instaló yt-dlp pero es posible que necesites reiniciar la aplicación para usarlo.")
                    lista_descargas.see(tk.END)
                    return True
    except Exception as e:
        lista_descargas.insert(tk.END, f"❌ Error al verificar yt-dlp: {str(e)}")
        lista_descargas.see(tk.END)
        messagebox.showerror("Error", f"Error al verificar yt-dlp: {str(e)}")
        return False

def verificar_ffmpeg(lista_descargas):
    """Verifica si FFmpeg está instalado y lo instala si es posible"""
    try:
        lista_descargas.insert(tk.END, "Verificando FFmpeg...")
        lista_descargas.see(tk.END)
        
        startupinfo = None
        if platform.system() == "Windows":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = 0  # SW_HIDE
        
        # Verificar si FFmpeg ya está en el PATH
        try:
            if platform.system() == "Windows":
                process = subprocess.Popen(
                    "ffmpeg -version",
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    startupinfo=startupinfo
                )
            else:
                process = subprocess.Popen(
                    ["ffmpeg", "-version"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                
            stdout, stderr = process.communicate()
            
            if process.returncode == 0:
                lista_descargas.insert(tk.END, "✅ FFmpeg ya está instalado.")
                lista_descargas.see(tk.END)
                return True
        except:
            pass  # FFmpeg no está en el PATH, intentaremos instalarlo
        
        # El resto de la función permanece igual
        sistema = platform.system().lower()
        
        # Diferente método de instalación según el sistema operativo
        if sistema == "windows":
            mensaje = ("FFmpeg no está instalado. Para continuar la descarga, por favor:\n\n"
                      "1. Descarga FFmpeg desde https://www.gyan.dev/ffmpeg/builds/ (versión 'release')\n"
                      "2. Extrae el archivo y mueve la carpeta a C:\\\n"
                      "3. Añade la carpeta 'bin' a la variable PATH del sistema\n"
                      "4. Reinicia este programa\n\n"
                      "Sin FFmpeg, los archivos se descargarán en formato WebM y no MP3.")
            lista_descargas.insert(tk.END, "❌ FFmpeg no está instalado.")
            lista_descargas.insert(tk.END, "Los archivos se descargarán en formato WebM en lugar de MP3.")
            lista_descargas.see(tk.END)
            messagebox.showwarning("FFmpeg requerido", mensaje)
            return False
            
        elif sistema == "darwin":  # macOS
            # En macOS intentamos instalar con brew si está disponible
            try:
                lista_descargas.insert(tk.END, "Intentando instalar FFmpeg con Homebrew...")
                lista_descargas.see(tk.END)
                messagebox.showinfo("Instalación", "Se intentará instalar FFmpeg con Homebrew. Esto puede tardar unos minutos.")
                
                # Popen para la instalación
                process = subprocess.Popen(
                    ["brew", "install", "ffmpeg"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                
                stdout, stderr = process.communicate()
                
                if process.returncode == 0:
                    lista_descargas.insert(tk.END, "✅ FFmpeg instalado correctamente con Homebrew.")
                    lista_descargas.see(tk.END)
                    return True
                else:
                    raise Exception("Error instalando con Homebrew")
            except:
                mensaje = ("No se pudo instalar FFmpeg automáticamente. Para continuar la descarga, por favor:\n\n"
                          "1. Instala Homebrew desde https://brew.sh\n"
                          "2. Abre Terminal y ejecuta: brew install ffmpeg\n"
                          "3. Reinicia este programa\n\n"
                          "Sin FFmpeg, los archivos se descargarán en formato WebM y no MP3.")
                lista_descargas.insert(tk.END, "❌ Error al instalar FFmpeg.")
                lista_descargas.insert(tk.END, "Los archivos se descargarán en formato WebM en lugar de MP3.")
                lista_descargas.see(tk.END)
                messagebox.showwarning("FFmpeg requerido", mensaje)
                return False
                
        elif sistema == "linux":
            # En Linux intentamos instalar con apt (Ubuntu, Debian) o pacman (Arch)
            try:
                # Primero intentamos con apt (Ubuntu, Debian, etc.)
                lista_descargas.insert(tk.END, "Intentando instalar FFmpeg con apt...")
                messagebox.showinfo("Instalación", "Se intentará instalar FFmpeg. Esto puede requerir permisos de administrador y tardar unos minutos.")
                resultado = subprocess.run(
                    ["sudo", "apt", "install", "-y", "ffmpeg"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                if resultado.returncode == 0:
                    lista_descargas.insert(tk.END, "✅ FFmpeg instalado correctamente con apt.")
                    return True
                    
                # Si falla apt, intentamos con pacman (Arch Linux)
                lista_descargas.insert(tk.END, "Intentando instalar FFmpeg con pacman...")
                resultado = subprocess.run(
                    ["sudo", "pacman", "-S", "--noconfirm", "ffmpeg"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                if resultado.returncode == 0:
                    lista_descargas.insert(tk.END, "✅ FFmpeg instalado correctamente con pacman.")
                    return True
                    
                raise Exception("No se pudo instalar automáticamente")
            except:
                mensaje = ("No se pudo instalar FFmpeg automáticamente. Para continuar la descarga, por favor:\n\n"
                          "1. Abre Terminal y ejecuta uno de estos comandos según tu distribución:\n"
                          "   - Ubuntu/Debian: sudo apt install ffmpeg\n"
                          "   - Arch Linux: sudo pacman -S ffmpeg\n"
                          "   - Fedora: sudo dnf install ffmpeg\n"
                          "2. Reinicia este programa\n\n"
                          "Sin FFmpeg, los archivos se descargarán en formato WebM y no MP3.")
                lista_descargas.insert(tk.END, "❌ Error al instalar FFmpeg.")
                lista_descargas.insert(tk.END, "Los archivos se descargarán en formato WebM en lugar de MP3.")
                messagebox.showwarning("FFmpeg requerido", mensaje)
                return False
        
        # Sistema no reconocido o no se pudo instalar
        mensaje = ("No se pudo instalar FFmpeg automáticamente. Por favor, instálalo manualmente según tu sistema operativo.\n\n"
                  "Sin FFmpeg, los archivos se descargarán en formato WebM y no MP3.")
        lista_descargas.insert(tk.END, "⚠️ No se pudo verificar o instalar FFmpeg.")
        lista_descargas.insert(tk.END, "Los archivos se descargarán en su formato original.")
        lista_descargas.see(tk.END)
        messagebox.showwarning("FFmpeg requerido", mensaje)
        return False
        
    except Exception as e:
        lista_descargas.insert(tk.END, f"❌ Error al verificar FFmpeg: {str(e)}")
        lista_descargas.insert(tk.END, "Los archivos se descargarán en su formato original.")
        lista_descargas.see(tk.END)
        return False

def mostrar_en_registro(mensaje, tipo="info"):
    config = cargar_configuracion()
    
    if tipo == "detalles" and config.get("MOSTRAR_DETALLES") != "true":
        return False
    if tipo == "exito" and config.get("MOSTRAR_EXITOS") != "true":
        return False
    if tipo == "error" and config.get("MOSTRAR_ERRORES") != "true":
        return False
    if tipo == "resumen" and config.get("MOSTRAR_RESUMEN") != "true":
        return False
    
    return True

def descargar_mp3(url, output_path, lista_descargas, ffmpeg_disponible):
    """Descarga un video de YouTube"""
    try:
        """if getattr(threading.current_thread, '_thread_killer', False):
            lista_descargas.insert(tk.END, "Descarga interrumpida.")
            return False"""
        
        # Cargar configuración para verificar formato seleccionado
        config = cargar_configuracion()
        formato_seleccionado = config.get("FORMATO_DESCARGA", "mp3")
        
        # Preparar comando base
        comando = ["yt-dlp"]
        
        if formato_seleccionado == "mp3" and ffmpeg_disponible:
            # Si FFmpeg está disponible y se quiere MP3, extraer audio y convertir a MP3
            comando.extend([
                "-x", 
                "--audio-format", "mp3",
                "--audio-quality", "0",  # Mejor calidad
            ])
        else:
            # Si FFmpeg no está disponible o se eligió formato original, solo descargar el mejor audio
            comando.extend([
                "-f", "bestaudio",
            ])
        
        # Completar comando con destino y URL
        comando.extend([
            "-o", os.path.join(output_path, "%(title)s.%(ext)s"),
            url
        ])
        
        if platform.system() == "Windows":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = 0  # SW_HIDE
            
            proceso = subprocess.Popen(
                comando,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                universal_newlines=True,
                startupinfo=startupinfo,
                creationflags=subprocess.CREATE_NO_WINDOW,
                shell=False 
            )
        else:
            # Para Linux/Mac
            proceso = subprocess.Popen(
                comando,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                universal_newlines=True,
                shell=False 
            )
        
        # Variables para seguimiento del progreso
        progreso_actual = None
        nombre_archivo = None
        
        # Leer salida en tiempo real
        if mostrar_en_registro("detalles_descarga", "detalles"):
            for linea in proceso.stdout:
                if "[download]" in linea and "%" in linea and "ETA" in linea:
                    nuevo_progreso = linea.strip()
                    if nuevo_progreso != progreso_actual:
                        progreso_actual = nuevo_progreso
                        try:
                            lista_descargas.delete(tk.END)
                        except:
                            pass
                        lista_descargas.insert(tk.END, progreso_actual)
                        lista_descargas.see(tk.END)
                        
                        # Actualizar barra de progreso
                        try:
                            porcentaje = float(linea.split("%")[0].split()[-1])
                            barra_progreso["value"] = porcentaje
                            ventana.update_idletasks()
                        except:
                            pass
                elif "[download]" in linea and "Destination:" in linea:
                    # Capturar el nombre del archivo
                    nombre_archivo = linea.split("Destination:")[1].strip()
                    lista_descargas.insert(tk.END, f"Archivo: {os.path.basename(nombre_archivo)}")
                    lista_descargas.see(tk.END)
                elif "ERROR:" in linea:
                    lista_descargas.insert(tk.END, f"⚠️ {linea.strip()}")
                    lista_descargas.see(tk.END)
        
        proceso.wait()
        
        if proceso.returncode == 0:
            extension = "mp3" if formato_seleccionado == "mp3" and ffmpeg_disponible else "webm/m4a/opus"
            nombre_final = nombre_archivo if nombre_archivo else "Archivo desconocido"
            nombre_final = os.path.basename(nombre_final)
            
            if mostrar_en_registro("descarga_exitosa", "exito"):
                lista_descargas.insert(tk.END, f"✅ Descargado: {nombre_final} (formato: {extension})")
                lista_descargas.see(tk.END)
            
            # Restablecer barra de progreso
            barra_progreso["value"] = 0
            ventana.update_idletasks()
            
            return True
        else:
            error = proceso.stderr.read() if proceso.stderr else "Error desconocido"
            
            if mostrar_en_registro("error_descarga", "error"):
                lista_descargas.insert(tk.END, f"❌ Error al descargar: {error}")
                lista_descargas.see(tk.END)
            
            # Restablecer barra de progreso
            barra_progreso["value"] = 0
            ventana.update_idletasks()
            
            return False
            
    except Exception as e:
        lista_descargas.insert(tk.END, f"❌ Error al descargar {url}: {str(e)}")
        lista_descargas.see(tk.END)
        return False

def iniciar_descarga(archivo_urls, directorio_destino, lista_descargas, btn_descargar, btn_seleccionar_archivo, btn_seleccionar_carpeta):
    """Inicia la descarga de videos de YouTube"""

    if not archivo_urls or not os.path.exists(archivo_urls):
        messagebox.showerror("Error", "Por favor selecciona un archivo de texto válido con URLs.")
        return
        
    if not directorio_destino:
        messagebox.showerror("Error", "Por favor selecciona una carpeta de destino válida.")
        return
    
    # Deshabilitar botones durante la descarga
    btn_descargar.config(state=tk.DISABLED)
    btn_seleccionar_archivo.config(state=tk.DISABLED)
    btn_seleccionar_carpeta.config(state=tk.DISABLED)
    
    # Habilitar botones
    def habilitar_botones():
        btn_descargar.config(state=tk.NORMAL)
        btn_seleccionar_archivo.config(state=tk.NORMAL)
        btn_seleccionar_carpeta.config(state=tk.NORMAL)
    
    # Función para manejar las descargas en un hilo separado
    def proceso_descarga():

        global cancelar_descarga
        #global proceso_actual
        cancelar_descarga = False
        #proceso_actual = threading.current_thread()

        # Verificar dependencias
        if not verificar_dependencias(lista_descargas):
            lista_descargas.insert(tk.END, "⚠️ Algunas dependencias no están disponibles. Las descargas pueden ser limitadas.")
            ffmpeg_disponible = False
        else:
            ffmpeg_disponible = True
        
        # Leer URLs del archivo
        try:
            with open(archivo_urls, 'r', encoding='utf-8') as file:
                urls = [line.strip() for line in file if line.strip()]
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el archivo: {str(e)}")
            habilitar_botones()
            return
        
        # Verificar que hay URLs para descargar
        if not urls:
            messagebox.showinfo("Información", "No se encontraron URLs en el archivo.")
            habilitar_botones()
            return
        
        # Crear directorio de destino si no existe
        if not os.path.exists(directorio_destino):
            try:
                os.makedirs(directorio_destino)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo crear la carpeta de destino: {str(e)}")
                habilitar_botones()
                return
        
        total = len(urls)
        completados = 0
        fallidos = 0
        
        lista_descargas.insert(tk.END, f"")
        lista_descargas.insert(tk.END, f"Iniciando descarga de {total} archivos...")

        barra_progreso_archivos = ttk.Progressbar(marco_lista, orient="horizontal", mode="determinate")
        barra_progreso_archivos.pack(fill=tk.X, padx=5, pady=(0, 5))

        btn_cancelar_descarga = ttk.Button(marco_lista, text="Cancelar descarga", command=lambda: cancelar_descargas())
        btn_cancelar_descarga.pack(side=tk.TOP, anchor=tk.E, padx=5, pady=2)

        for i, url in enumerate(urls):

            if cancelar_descarga:
                lista_descargas.insert(tk.END, "❌ Descarga cancelada por el usuario.")
                break
            
            resultado = descargar_mp3(url, directorio_destino, lista_descargas, ffmpeg_disponible)
            barra_progreso_archivos["value"] = ((i + 1) / total) * 100
            ventana.update_idletasks()
            if resultado:
                completados += 1
            else:
                fallidos += 1
            # Pequeña pausa entre descargas para evitar sobrecargar la conexión
            time.sleep(0.2)
        
        if mostrar_en_registro("resumen", "resumen"):  # or True  --> Forzar mostrar el resumen
            lista_descargas.insert(tk.END, f"")
            lista_descargas.insert(tk.END, f"=== RESUMEN ===")
            lista_descargas.insert(tk.END, f"Total de archivos: {total}")
            lista_descargas.insert(tk.END, f"Descargados con éxito: {completados}")
            lista_descargas.insert(tk.END, f"Fallidos: {fallidos}")
            lista_descargas.see(tk.END)

            if not ffmpeg_disponible and completados > 0:
                lista_descargas.insert(tk.END, f"Nota: Los archivos se descargaron en su formato original, no en MP3.")
                lista_descargas.insert(tk.END, f"Para convertir a MP3, instala FFmpeg y vuelve a ejecutar el programa.")
        
        messagebox.showinfo("Descarga Completada", f"Se descargaron {completados} de {total} archivos.")
        barra_progreso_archivos.destroy()
        btn_cancelar_descarga.destroy()
        habilitar_botones()
    
    # Iniciar descarga en un hilo separado para no bloquear la interfaz
    threading.Thread(target=proceso_descarga, daemon=True).start()

def iniciar_descarga_individual(url, directorio_destino, lista_descargas, btn_descargar, btn_seleccionar_carpeta_individual, entrada_url):

    # Validar entradas
    if not url or not url.strip():
        messagebox.showerror("Error", "Por favor introduce una URL válida de YouTube.")
        return
        
    if not directorio_destino:
        messagebox.showerror("Error", "Por favor selecciona una carpeta de destino válida.")
        return
    
    # Deshabilitar botones durante la descarga
    btn_descargar.config(state=tk.DISABLED)
    btn_seleccionar_carpeta_individual.config(state=tk.DISABLED)
    entrada_url.config(state=tk.DISABLED)
    
    # Habilitar botones
    def habilitar_botones():
        btn_descargar.config(state=tk.NORMAL)
        btn_seleccionar_carpeta_individual.config(state=tk.NORMAL)
        entrada_url.config(state=tk.NORMAL)
    
    # Función para manejar las descargas en un hilo separado
    def proceso_descarga():
        # Verificar dependencias
        if not verificar_dependencias(lista_descargas):
            lista_descargas.insert(tk.END, "⚠️ Algunas dependencias no están disponibles. Las descargas pueden ser limitadas.")
            ffmpeg_disponible = False
        else:
            ffmpeg_disponible = True
        
        # Crear directorio de destino si no existe
        if not os.path.exists(directorio_destino):
            try:
                os.makedirs(directorio_destino)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo crear la carpeta de destino: {str(e)}")
                habilitar_botones()
                return
        
        lista_descargas.insert(tk.END, f"")
        lista_descargas.insert(tk.END, f"Iniciando descarga individual...")
        
        resultado = descargar_mp3(url, directorio_destino, lista_descargas, ffmpeg_disponible)

        if resultado:
            mensaje = "La descarga se ha completado con éxito."
        else:
            mensaje = "La descarga ha fallado. Revisa el registro para más detalles."
        
        if mostrar_en_registro("resumen", "resumen"):  # or True  --> Forzar mostrar el resumen
            # Actualizar con resumen final
            lista_descargas.insert(tk.END, f"")
            lista_descargas.insert(tk.END, f"=== RESUMEN ===")
            if resultado:
                lista_descargas.insert(tk.END, f"✅ Descarga completada con éxito")
            else:
                lista_descargas.insert(tk.END, f"❌ La descarga ha fallado")
            lista_descargas.see(tk.END)
        
        if not ffmpeg_disponible and resultado:
            lista_descargas.insert(tk.END, f"Nota: El archivo se descargó en su formato original, no en MP3.")
            lista_descargas.insert(tk.END, f"Para convertir a MP3, instala FFmpeg y vuelve a ejecutar el programa.")
            mensaje += "\nEl archivo se descargó en su formato original, no en MP3."
        
        messagebox.showinfo("Descarga Completada", mensaje)
        habilitar_botones()
    
    # Iniciar descarga en un hilo separado para no bloquear la interfaz
    threading.Thread(target=proceso_descarga, daemon=True).start()

def cancelar_descargas():
    global cancelar_descarga
    cancelar_descarga = True
    lista_descargas.insert(tk.END, "⚠️ Cancelando descargas... Espere un momento.")
    lista_descargas.see(tk.END)

"""def cancelar_descargas():
    global cancelar_descarga, proceso_actual
    if proceso_actual and proceso_actual.is_alive():
        cancelar_descarga = True
        try:
            # Attempt to forcefully terminate the thread
            proceso_actual._thread_killer = True
        except:
            pass
        lista_descargas.insert(tk.END, "⚠️ Cancelando descargas... Espere un momento.")
        lista_descargas.see(tk.END)"""

def seleccionar_archivo():
    archivo = filedialog.askopenfilename(
        title="Selecciona el archivo con las URLs",
        filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
    )
    if archivo:
        entrada_archivo.delete(0, tk.END)
        entrada_archivo.insert(0, archivo)

def seleccionar_carpeta():
    carpeta = filedialog.askdirectory(title="Selecciona la carpeta de destino")
    if carpeta:
        entrada_carpeta.delete(0, tk.END)
        entrada_carpeta.insert(0, carpeta)

def seleccionar_carpeta_individual():
    carpeta = filedialog.askdirectory(title="Selecciona la carpeta de destino")
    if carpeta:
        entrada_carpeta_individual.delete(0, tk.END)
        entrada_carpeta_individual.insert(0, carpeta)

def limpiar_listado():
    """Limpia el listado de progreso"""
    lista_descargas.delete(0, tk.END)
    lista_instrucciones = [
        "Instrucciones: Selecciona un archivo de texto con URLs de YouTube (una por línea)",
        "Al iniciar la descarga, se verificarán las dependencias necesarias.",
        "Se necesita yt-dlp para descargar videos y FFmpeg para convertir a MP3."
    ]
    for instruccion in lista_instrucciones:
        lista_descargas.insert(tk.END, instruccion)
    # Reiniciar barra de progreso
    barra_progreso["value"] = 0
    ventana.update_idletasks()

def pegar_url(event=None):
    """Pega el contenido del portapapeles en el campo de URL"""
    try:
        entrada_url.delete(0, tk.END)
        entrada_url.insert(0, ventana.clipboard_get())
    except:
        pass

def abrir_configuracion():
    """Abre la ventana de configuración de la aplicación"""
    # Crear ventana de configuración
    ventana_config = tk.Toplevel(ventana)
    ventana_config.title("Configuración")
    ventana_config.geometry("500x550")
    ventana_config.resizable(False, False)
    ventana_config.transient(ventana)  # Hacer que sea modal
    ventana_config.grab_set()  # Forzar que sea modal
    
    # Marco principal
    marco_config = ttk.Frame(ventana_config, padding=15)
    marco_config.pack(fill=tk.BOTH, expand=True)
    
    # Título
    ttk.Label(marco_config, text="Configuración de la aplicación", font=("", 12, "bold")).pack(pady=(0, 15))
    
    # Carpeta de descarga predeterminada
    marco_carpeta_default = ttk.Frame(marco_config)
    marco_carpeta_default.pack(fill=tk.X, pady=5)
    
    ttk.Label(marco_carpeta_default, text="Carpeta de descarga predeterminada:").pack(anchor=tk.W)
    
    # Frame para entrada y botón
    marco_entrada_carpeta = ttk.Frame(marco_config)
    marco_entrada_carpeta.pack(fill=tk.X, pady=(0, 10))
    
    entrada_carpeta_default = ttk.Entry(marco_entrada_carpeta)
    entrada_carpeta_default.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
    
    # Obtener la ruta actual desde el archivo de configuración o usar valor predeterminado
    try:
        with open("config.ini", "r") as f:
            for linea in f:
                if linea.startswith("CARPETA_DESCARGA="):
                    ruta = linea.split("=")[1].strip()
                    entrada_carpeta_default.insert(0, ruta)
                    break
    except:
        # Si no existe, usar la carpeta de descargas predeterminada
        carpeta_descargas = os.path.join(os.path.expanduser("~"), "Downloads")
        entrada_carpeta_default.insert(0, carpeta_descargas)
    
    def seleccionar_carpeta_default():
        carpeta = filedialog.askdirectory(title="Selecciona la carpeta de destino predeterminada")
        if carpeta:
            entrada_carpeta_default.delete(0, tk.END)
            entrada_carpeta_default.insert(0, carpeta)
    
    btn_seleccionar_carpeta_default = ttk.Button(
        marco_entrada_carpeta, 
        text="Seleccionar", 
        command=seleccionar_carpeta_default
    )
    btn_seleccionar_carpeta_default.pack(side=tk.LEFT)
    
    ttk.Separator(marco_config, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
    
    # Verificación de dependencias
    marco_dependencias = ttk.Frame(marco_config)
    marco_dependencias.pack(fill=tk.X, pady=5)
    
    ttk.Label(marco_dependencias, text="Verificación de dependencias:").pack(anchor=tk.W)
    
    # Variable para el estado del checkbox
    verificar_deps = tk.BooleanVar()
    verificar_deps.set(True)  # Por defecto activado
    
    # Intentar cargar valor desde archivo de configuración
    try:
        with open("config.ini", "r") as f:
            for linea in f:
                if linea.startswith("VERIFICAR_DEPENDENCIAS="):
                    valor = linea.split("=")[1].strip().lower()
                    verificar_deps.set(valor == "true")
                    break
    except:
        pass
    
    check_dependencias = ttk.Checkbutton(
        marco_config, 
        text="Verificar dependencias al iniciar la descarga", 
        variable=verificar_deps
    )
    check_dependencias.pack(anchor=tk.W, pady=(0, 10))
    
    ttk.Separator(marco_config, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
    
    # Formato predeterminado
    marco_formato = ttk.Frame(marco_config)
    marco_formato.pack(fill=tk.X, pady=5)
    
    ttk.Label(marco_formato, text="Formato de descarga:").pack(anchor=tk.W)
    
    # Variable para el formato
    formato_var = tk.StringVar()
    formato_var.set("mp3")  # Por defecto MP3
    
    # Intentar cargar valor desde archivo de configuración
    try:
        with open("config.ini", "r") as f:
            for linea in f:
                if linea.startswith("FORMATO_DESCARGA="):
                    valor = linea.split("=")[1].strip().lower()
                    formato_var.set(valor)
                    break
    except:
        pass
    
    radio_mp3 = ttk.Radiobutton(
        marco_config, 
        text="MP3 (requiere FFmpeg)", 
        variable=formato_var, 
        value="mp3"
    )
    radio_mp3.pack(anchor=tk.W)
    
    radio_original = ttk.Radiobutton(
        marco_config, 
        text="Formato original (webm/m4a)", 
        variable=formato_var, 
        value="original"
    )
    radio_original.pack(anchor=tk.W, pady=(0, 10))

    ttk.Separator(marco_config, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

    # Nivel de detalle del registro
    marco_registro = ttk.Frame(marco_config)
    marco_registro.pack(fill=tk.X, pady=5)

    # Variables para cada tipo de registro
    detalles_var = tk.BooleanVar(value=True)
    exitos_var = tk.BooleanVar(value=True)
    errores_var = tk.BooleanVar(value=True)
    resumen_var = tk.BooleanVar(value=True)

    try:
        with open("config.ini", "r") as f:
            for linea in f:
                if linea.startswith("MOSTRAR_DETALLES="):
                    detalles_var.set(linea.split("=")[1].strip().lower() == "true")
                elif linea.startswith("MOSTRAR_EXITOS="):
                    exitos_var.set(linea.split("=")[1].strip().lower() == "true")
                elif linea.startswith("MOSTRAR_ERRORES="):
                    errores_var.set(linea.split("=")[1].strip().lower() == "true")
                elif linea.startswith("MOSTRAR_RESUMEN="):
                    resumen_var.set(linea.split("=")[1].strip().lower() == "true")
    except:
        pass

    marco_registro = ttk.Frame(marco_config)
    marco_registro.pack(fill=tk.X, pady=5)

    ttk.Label(marco_registro, text="Niveles de registro:").pack(anchor=tk.W)

    check_detalles = ttk.Checkbutton(marco_config, text="Detalles de descarga", variable=detalles_var)
    check_detalles.pack(anchor=tk.W)

    check_exitos = ttk.Checkbutton(marco_config, text="Descargas exitosas", variable=exitos_var)
    check_exitos.pack(anchor=tk.W)

    check_errores = ttk.Checkbutton(marco_config, text="Errores", variable=errores_var)
    check_errores.pack(anchor=tk.W)

    check_resumen = ttk.Checkbutton(marco_config, text="Resumen", variable=resumen_var)
    check_resumen.pack(anchor=tk.W)
    
    # Botones de acción
    marco_botones = ttk.Frame(marco_config)
    marco_botones.pack(fill=tk.X, pady=15)
    
    def guardar_configuracion():
        # Guardar configuración en archivo
        try:
            with open("config.ini", "w") as f:
                f.write(f"CARPETA_DESCARGA={entrada_carpeta_default.get()}\n")
                f.write(f"VERIFICAR_DEPENDENCIAS={'true' if verificar_deps.get() else 'false'}\n")
                f.write(f"FORMATO_DESCARGA={formato_var.get()}\n")
                f.write(f"MOSTRAR_DETALLES={'true' if detalles_var.get() else 'false'}\n")
                f.write(f"MOSTRAR_EXITOS={'true' if exitos_var.get() else 'false'}\n")
                f.write(f"MOSTRAR_ERRORES={'true' if errores_var.get() else 'false'}\n")
                f.write(f"MOSTRAR_RESUMEN={'true' if resumen_var.get() else 'false'}\n")
            
            # Actualizar las entradas de carpeta en la interfaz principal
            carpeta_nueva = entrada_carpeta_default.get()
            entrada_carpeta.delete(0, tk.END)
            entrada_carpeta.insert(0, carpeta_nueva)
            entrada_carpeta_individual.delete(0, tk.END)
            entrada_carpeta_individual.insert(0, carpeta_nueva)
            
            messagebox.showinfo("Éxito", "Configuración guardada correctamente")
            ventana_config.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la configuración: {str(e)}")
    
    def restaurar_valores():
        entrada_carpeta_default.delete(0, tk.END)
        entrada_carpeta_default.insert(0, os.path.join(os.path.expanduser("~"), "Downloads"))
        verificar_deps.set(True)
        formato_var.set("mp3")

    
    btn_cancelar = ttk.Button(marco_botones, text="Cancelar", command=ventana_config.destroy)
    btn_cancelar.pack(side=tk.RIGHT, padx=(5, 0))
    
    btn_guardar = ttk.Button(marco_botones, text="Guardar", command=guardar_configuracion)
    btn_guardar.pack(side=tk.RIGHT, padx=(5, 0))
    
    btn_restaurar = ttk.Button(marco_botones, text="Valores predeterminados", command=restaurar_valores)
    btn_restaurar.pack(side=tk.LEFT)

# Función para cargar la configuración al inicio
def cargar_configuracion():
    """Carga la configuración desde el archivo config.ini"""
    try:
        # Valores predeterminados
        config = {
            "CARPETA_DESCARGA": os.path.join(os.path.expanduser("~"), "Downloads"),
            "VERIFICAR_DEPENDENCIAS": "true",
            "FORMATO_DESCARGA": "mp3",
            "MOSTRAR_DETALLES": "true",
            "MOSTRAR_EXITOS": "true",
            "MOSTRAR_ERRORES": "true",
            "MOSTRAR_RESUMEN": "true"
        }
        
        # Intentar leer desde archivo
        try:
            with open("config.ini", "r") as f:
                for linea in f:
                    if "=" in linea:
                        clave, valor = linea.strip().split("=", 1)
                        config[clave] = valor
        except FileNotFoundError:
            # Crear archivo de configuración si no existe
            with open("config.ini", "w") as f:
                f.write(f"CARPETA_DESCARGA={config['CARPETA_DESCARGA']}\n")
                f.write(f"VERIFICAR_DEPENDENCIAS={config['VERIFICAR_DEPENDENCIAS']}\n")
                f.write(f"FORMATO_DESCARGA={config['FORMATO_DESCARGA']}\n")
                f.write(f"NIVEL_REGISTRO={config['NIVEL_REGISTRO']}\n")
        
        # Aplicar configuración
        carpeta_descargas = config["CARPETA_DESCARGA"]
        if os.path.exists(carpeta_descargas):
            entrada_carpeta.delete(0, tk.END)
            entrada_carpeta.insert(0, carpeta_descargas)
            entrada_carpeta_individual.delete(0, tk.END)
            entrada_carpeta_individual.insert(0, carpeta_descargas)
            
        return config
    except Exception as e:
        print(f"Error al cargar configuración: {str(e)}")
        return {
            "CARPETA_DESCARGA": os.path.join(os.path.expanduser("~"), "Downloads"),
            "VERIFICAR_DEPENDENCIAS": "true",
            "FORMATO_DESCARGA": "mp3"
        }


# Crear la interfaz gráfica
ventana = tk.Tk()
ventana.title("YouTube a MP3 - Descargador")
ventana.geometry("700x550")
ventana.resizable(True, True)

# Añadir botón de configuración en la esquina superior derecha
marco_superior = ttk.Frame(ventana)
marco_superior.pack(fill=tk.X, padx=10, pady=(10, 0))

# Botón de configuración con texto de rueda
btn_configuracion = ttk.Button(marco_superior, text="⚙", width=3, command=abrir_configuracion)
btn_configuracion.pack(side=tk.RIGHT)

# Crear un notebook (pestañas)
notebook = ttk.Notebook(ventana)
notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Pestaña 1: Descarga desde archivo
tab_archivo = ttk.Frame(notebook)
notebook.add(tab_archivo, text="Descarga Múltiple")

# Pestaña 2: Descarga individual
tab_individual = ttk.Frame(notebook)
notebook.add(tab_individual, text="Descarga Individual")

# ---- Configuración de la pestaña de descarga desde archivo ----
marco_principal = ttk.Frame(tab_archivo, padding=10)
marco_principal.pack(fill=tk.BOTH, expand=True)

# Selección de archivo
marco_archivo = ttk.Frame(marco_principal)
marco_archivo.pack(fill=tk.X, pady=5)

ttk.Label(marco_archivo, text="Archivo de URLs:").pack(side=tk.LEFT)
entrada_archivo = ttk.Entry(marco_archivo)
entrada_archivo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))
btn_seleccionar_archivo = ttk.Button(marco_archivo, text="Seleccionar", command=seleccionar_archivo)
btn_seleccionar_archivo.pack(side=tk.LEFT)

# Selección de carpeta de destino
marco_carpeta = ttk.Frame(marco_principal)
marco_carpeta.pack(fill=tk.X, pady=5)

ttk.Label(marco_carpeta, text="Carpeta destino:").pack(side=tk.LEFT)
entrada_carpeta = ttk.Entry(marco_carpeta)
entrada_carpeta.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))
btn_seleccionar_carpeta = ttk.Button(marco_carpeta, text="Seleccionar", command=seleccionar_carpeta)
btn_seleccionar_carpeta.pack(side=tk.LEFT)

# Botón de descarga
btn_descargar = ttk.Button(
    marco_principal, 
    text="Iniciar Descarga", 
    command=lambda: iniciar_descarga(
        entrada_archivo.get(), 
        entrada_carpeta.get(), 
        lista_descargas,
        btn_descargar,
        btn_seleccionar_archivo,
        btn_seleccionar_carpeta
    )
)
btn_descargar.pack(pady=10)

# ---- Configuración de la pestaña de descarga individual ----
marco_individual = ttk.Frame(tab_individual, padding=10)
marco_individual.pack(fill=tk.BOTH, expand=True)

# Entrada de URL individual
marco_url = ttk.Frame(marco_individual)
marco_url.pack(fill=tk.X, pady=5)

ttk.Label(marco_url, text="URL de YouTube:").pack(side=tk.LEFT)
entrada_url = ttk.Entry(marco_url)
entrada_url.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))
btn_pegar = ttk.Button(marco_url, text="Pegar", command=pegar_url)
btn_pegar.pack(side=tk.LEFT)

# Tecla rápida para pegar (Ctrl+V)
entrada_url.bind('<Control-v>', pegar_url)

# Selección de carpeta de destino individual
marco_carpeta_individual = ttk.Frame(marco_individual)
marco_carpeta_individual.pack(fill=tk.X, pady=5)

ttk.Label(marco_carpeta_individual, text="Carpeta destino:").pack(side=tk.LEFT)
entrada_carpeta_individual = ttk.Entry(marco_carpeta_individual)
entrada_carpeta_individual.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))
btn_seleccionar_carpeta_individual = ttk.Button(marco_carpeta_individual, text="Seleccionar", command=seleccionar_carpeta_individual)
btn_seleccionar_carpeta_individual.pack(side=tk.LEFT)

# Botón de descarga individual
btn_descargar_individual = ttk.Button(
    marco_individual, 
    text="Descargar", 
    command=lambda: iniciar_descarga_individual(
        entrada_url.get(), 
        entrada_carpeta_individual.get(), 
        lista_descargas,
        btn_descargar_individual,
        btn_seleccionar_carpeta_individual,
        entrada_url
    )
)
btn_descargar_individual.pack(pady=10)

# Compartir la lista de descargas entre ambas pestañas
# Crear un frame para la lista en la ventana principal
marco_lista = ttk.LabelFrame(ventana, text="Progreso de descargas:")
marco_lista.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

# Agregar botón para limpiar el registro
btn_limpiar = ttk.Button(marco_lista, text="Limpiar registro", command=limpiar_listado)
btn_limpiar.pack(side=tk.TOP, anchor=tk.E, padx=5, pady=2)

# Crear scrollbar y lista
scrollbar = ttk.Scrollbar(marco_lista)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

lista_descargas = tk.Listbox(marco_lista, yscrollcommand=scrollbar.set)
lista_descargas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
scrollbar.config(command=lista_descargas.yview)

barra_progreso = ttk.Progressbar(marco_lista, orient="horizontal", mode="determinate")
barra_progreso.pack(fill=tk.X, padx=5, pady=(0, 5))

# Instrucciones y mensajes iniciales
limpiar_listado()

# Cargar configuración al iniciar
config = cargar_configuracion()

ventana.mainloop()