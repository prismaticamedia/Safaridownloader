# S4f4riDownload (Con Interfaz Gráfica y Soporte PDF)

¡Bienvenido a **S4f4riDownload**! Este proyecto proporciona una interfaz gráfica de usuario (GUI) fácil de usar, construida con PyQt6, para descargar libros de la biblioteca de Safari Books Online (O'Reilly Learning) y, opcionalmente, convertirlos en hermosos archivos PDF.

## Características Principales
- **Interfaz de Escritorio Intuitiva:** Ingresa el ID de tu libro y pega tus cookies rápidamente.
- **Salida en EPUB y PDF Formateado:** Genera automáticamente un EPUB con el contenido del libro y ofrece la conversión a un PDF limpio con números de página precisos (utilizando PyPDF2 y ReportLab).
- **Descarga sin interrupciones:** Integra Cloudscraper para recuperar contenido de la API de O'Reilly sin interrupciones.
- **Mejoras de Formato y Visualización:** Soluciona problemas de renderizado en Apple Books definiendo correctamente la codificación de caracteres y manteniendo las proporciones originales de las imágenes.

## Instalación y Configuración

1. Clona este repositorio en tu computadora local:
   ```bash
   git clone https://github.com/prismaticamedia/Safaridownloader.git
   cd Safaridownloader
   ```
2. Instala las dependencias necesarias de Python:
   ```bash
   pip3 install -r requirements.txt
   ```
3. Ejecuta la aplicación:
   ```bash
   python3 s4f4ridownload_ui.py
   ```

## Cómo Usar S4f4riDownload

1. **Obtén tus Cookies:** Dado que el inicio de sesión está protegido, debes iniciar sesión en O'Reilly desde tu navegador web y extraer tus cookies de sesión.
2. **Pega las Cookies:** Abre la aplicación, ve a la pestaña "1. Paste Cookies", pega tus cookies y haz clic en **Save cookies.json**.
3. **Descarga el Libro:** Navega a la pestaña "2. Download Book", ingresa el ID del libro (por ejemplo, `9781617299339`), elige si deseas generar un PDF y presiona **Download**.

---

## Agradecimientos y Aviso Legal

Esta herramienta es una versión profundamente modificada y modernizada basada en el increíble trabajo fundacional del proyecto original [safaribooks de Lorenzo Di Fuccia](https://github.com/lorenzodifuccia/safaribooks). Hemos desarrollado sobre su lógica central para incorporar una GUI de escritorio y capacidades PDF mejoradas.

### Aviso Legal Importante (adaptado del autor original):
> Descarga y genera EPUBs de tus libros favoritos desde la biblioteca de Safari Books Online.
> No soy responsable del uso de este programa; esto es estrictamente para fines personales y educativos.
> Antes de cualquier uso, por favor lee los Términos de Servicio de O'Reilly.
