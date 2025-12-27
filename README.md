# Image-to-Vector-Converter
Conversor modular de imágenes a SVG optimizado y PNG para impresión DTF.  
Soporta PNG, JPG, AI y PDF con extracción automática de imágenes y eliminación inteligente de fondo.

---

## Características principales

- Convierte PNG, JPG, AI y PDF a SVG optimizado y minificado.
- Elimina el fondo automáticamente (-b true) detectando el color dominante.
- Soporte completo para:
  - Archivos AI → conversión a PNG temporal mediante Inkscape.
  - Archivos PDF → extracción de imagen mediante pdfimages -all.
- Limpieza de fondo ANTES de vectorizar (clave para SVG limpio).
- Optimización y minificación del SVG con scour.
- Sufijos automáticos:
  - _sf_ → sin fondo
  - _cf_ → con fondo
- Módulo adicional svg_to_png.py para generar PNG listo para DTF (600 DPI).
- Carpetas input/, output/ y temp/ ignoradas por Git.

---

## Requisitos

### Dependencias del sistema
sudo apt install inkscape  
sudo apt install poppler-utils

### Dependencias Python
pip install pillow  
pip install cairosvg  
pip install scour

---

## Estructura del proyecto

Image-to-Vector-Converter/
│
├── convert_to_svg.py        # Módulo principal: raster/AI/PDF → SVG
├── svg_to_png.py            # Módulo DTF: SVG → PNG 600 DPI
│
├── input/                   # Imágenes de entrada (IGNORADO por Git)
├── output/                  # Resultados SVG/PNG (IGNORADO por Git)
├── temp/                    # Archivos temporales (IGNORADO por Git)
│
└── README.md

---

## Uso del módulo convert_to_svg.py

### Convertir una imagen raster (PNG/JPG)
python -m convert_to_svg -i input/foto.png -o output/foto -b true

### Convertir un archivo AI
python -m convert_to_svg -i input/logo.ai -o output/logo -b true

### Convertir un PDF con una sola página
python -m convert_to_svg -i input/alien.pdf -o output/alien -b true

### Parámetros
- -i : archivo de entrada (png, jpg, ai, pdf)
- -o : carpeta de salida
- -b : true = eliminar fondo, false = conservar fondo

---

## Cómo funciona internamente

### 1. Detección del tipo de archivo
- PNG/JPG → se usan directamente.
- AI → se convierte a PNG temporal con Inkscape.
- PDF → se extrae la primera imagen con pdfimages -all.

### 2. Eliminación automática del fondo (si -b true)
- Se analiza el borde del PNG.
- Se detecta el color dominante del fondo.
- Se elimina con tolerancia configurable.
- Se guarda el PNG limpio.

### 3. Vectorización con VTracer
vtracer --input temp.png --output final.svg

### 4. Optimización del SVG
- Se eliminan metadatos.
- Se minifica.
- Se limpian rellenos residuales.

### 5. Sufijos automáticos
- _sf_ → sin fondo
- _cf_ → con fondo
- Timestamp DDMMYYYYHHMMSS

Ejemplo:
alien_sf_27122025130648.svg

---

## Uso del módulo svg_to_png.py (DTF)

Convierte un SVG optimizado a PNG 600 DPI:

python -m svg_to_png -i output/alien/alien_sf_27122025130648.svg

Opcionalmente:
python -m svg_to_png -i vector.svg -o dtf -d 300

---

## .gitignore recomendado

input/  
output/  
temp/  

venv/  
env/  
.myenv/  
*.env  
*.venv  

__pycache__/  
*.py[cod]  
*$py.class  

*.log  
*.tmp  
*.swp  

.DS_Store  
Thumbs.db  

.vscode/  
.idea/  

dist/  
build/

---

## Notas técnicas

- El fondo debe eliminarse antes de vectorizar, o VTracer lo convertirá en paths.
- pdfimages -all conserva los colores originales del PDF.
- La detección automática del fondo funciona con blanco, negro, gris y colores sólidos.
- Si el fondo es complejo (degradados), se puede aumentar la tolerancia.

---

## Próximos módulos (opcional)

- Generación automática del canal blanco para DTF.
- Modo espejo para impresión en rollo.
- Validación de resolución mínima.
- Procesamiento por lotes.

---

## Autor

Proyecto desarrollado por Félix, optimizado para flujos NBES de producción real.

---

## Estado

Estable y listo para producción.
