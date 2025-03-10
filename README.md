# 🎵 YouTube to MP3 Downloader 🎵  

Este es un programa de escritorio en Python que permite descargar audio de videos de YouTube en formato MP3. Es una alternativa ligera y funcional después del cierre de muchas aplicaciones piratas de Spotify.  

## ✨ Características  
✅ Descarga individual o en lote desde un archivo de texto con URLs.  
✅ Conversión automática a MP3 (requiere FFmpeg).  
✅ Interfaz gráfica amigable y fácil de usar con `tkinter`.  
✅ Descargas rápidas y eficientes utilizando `yt-dlp`.  
✅ Verificación automática de dependencias e instalación si es necesario.  
✅ Configuración personalizable para la carpeta de destino, formato de descarga y nivel de detalle en los registros.  

## 📥 Instalación  

### 1️⃣ Requisitos Previos  
Antes de ejecutar la aplicación, asegúrate de tener instalado lo siguiente:  
- **Python 3.7 o superior**  
- **yt-dlp** (se instala automáticamente si no está presente)  
- **FFmpeg** (opcional, pero necesario para la conversión a MP3)  

### 2️⃣ Instalación de dependencias  
Ejecuta el siguiente comando en la terminal o en el CMD:  
```bash
pip install yt-dlp
```
> ⚠️ Si `yt-dlp` no está instalado, la aplicación intentará instalarlo automáticamente.  

### 3️⃣ Instalación de FFmpeg (Opcional pero Recomendado)  
Si quieres convertir los audios descargados a MP3, necesitas instalar **FFmpeg**.  

#### 🔹 En Windows  
1. Descarga FFmpeg desde: [Gyan.dev FFmpeg Builds](https://www.gyan.dev/ffmpeg/builds/)  
2. Extrae el contenido en `C:\ffmpeg`.  
3. Agrega `C:\ffmpeg\bin` a la variable de entorno **PATH**:
   - Abre el **Panel de Control** → **Sistema** → **Configuración avanzada del sistema**  
   - Ve a **Variables de entorno** → Busca la variable `Path` → Haz clic en **Editar**  
   - Añade `C:\ffmpeg\bin` y guarda los cambios.  
4. Cierra y vuelve a abrir la terminal/CMD y ejecuta:  
   ```bash
   ffmpeg -version
   ```
   Si ves información de FFmpeg, significa que está correctamente instalado.  

#### 🔹 En Linux  
Ejecuta:  
```bash
sudo apt update && sudo apt install ffmpeg -y
```
Para verificar la instalación:  
```bash
ffmpeg -version
```

#### 🔹 En macOS  
Si tienes Homebrew instalado:  
```bash
brew install ffmpeg
```

## 🚀 Uso  
1. Ejecuta el script en Python:  
   ```bash
   python "YouTube-Downloader.py"
   ```
2. **Modo descarga individual**:  
   - Introduce una URL de YouTube y selecciona la carpeta de destino.  
   - Pulsa "Descargar".  

3. **Modo descarga masiva**:  
   - Prepara un archivo `.txt` con una URL de YouTube por línea.  
   - Carga el archivo en la aplicación y elige la carpeta de destino.  
   - Pulsa "Iniciar Descarga".  

## 🛠 Configuración  
Puedes personalizar la configuración en el archivo `config.ini` para definir:  
- Carpeta predeterminada de descargas.  
- Formato de descarga (`mp3` o `webm/m4a`).  
- Nivel de detalle de los registros.  
- Verificación automática de dependencias.  

## 📝 Notas  
- Sin FFmpeg, los archivos se descargarán en formato **WebM** en lugar de MP3.  
- No necesitas una cuenta de YouTube ni claves API.  
- yt-dlp se encarga de manejar cualquier restricción de acceso a videos.  

## 📜 Licencia  
Este proyecto es de uso personal y educativo. No está destinado para uso comercial o distribución masiva.  
