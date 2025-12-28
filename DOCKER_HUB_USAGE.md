# Uso de la imagen Docker Hub: felixmurcia/image-converter

Repositorio: https://hub.docker.com/repository/docker/felixmurcia/image-converter/general

Instrucciones rápidas para usar la imagen publicada en Docker Hub.

## 1) Obtener la imagen

```bash
docker pull felixmurcia/image-converter:latest
```

## 2) Estructura de montaje recomendada

Se asume que en el host existen carpetas `input/`, `output/` y `temp/` (crear si no existen).

```bash
mkdir -p input output temp
```

## 3) Ejecutar `convert_to_svg` (convertir imágenes / AI / PDF → SVG)

Ejemplo básico (monta `input` y `output`):

```bash
docker run --rm -it \
  -v "$(pwd)/input":/app/input \
  -v "$(pwd)/output":/app/output \
  felixmurcia/image-converter:latest \
  python -m convert_to_svg -i input/foto.png -o output/foto -b true
```

Explicación:
- `-i` archivo de entrada (ruta dentro del contenedor: `input/...`).
- `-o` carpeta/identificador de salida (se escribirá en `output/`).
- `-b true|false` eliminar/retener fondo.

## 4) Ejecutar `svg_to_png` (SVG → PNG para DTF)

```bash
docker run --rm -it \
  -v "$(pwd)/input":/app/input \
  -v "$(pwd)/output":/app/output \
  felixmurcia/image-converter:latest \
  python -m svg_to_png -i output/foto_sf.svg -o dtf -d 600
```

## 5) Ejecutar con permisos del usuario host (evitar archivos root en `output`)

Para que los archivos generados tengan el mismo `UID:GID` que su usuario local:

```bash
docker run --rm -it -u $(id -u):$(id -g) \
  -v "$(pwd)/input":/app/input \
  -v "$(pwd)/output":/app/output \
  felixmurcia/image-converter:latest \
  python -m convert_to_svg -i input/foto.png -o output/foto -b true
```

## 6) Nota sobre `inkscape` y `pdfimages`

La imagen publicada incluye `inkscape` y `poppler-utils` (por ejemplo `pdfimages`) para permitir:
- conversión de `*.ai` a PNG mediante `inkscape`.
- extracción de imágenes desde `*.pdf` mediante `pdfimages`.

Si el comportamiento de `inkscape` o `pdfimages` difiere por versión, puede ejecutar esos comandos en el host o ajustar el flujo dentro del contenedor.

## 7) Ejemplo completo (paso a paso)

```bash
# 1) Descargar la imagen
docker pull felixmurcia/image-converter:latest

# 2) Poner archivo en input/
cp ~/Downloads/logo.ai input/

# 3) Convertir
docker run --rm -it -u $(id -u):$(id -g) -v "$(pwd)/input":/app/input -v "$(pwd)/output":/app/output felixmurcia/image-converter:latest python -m convert_to_svg -i input/logo.ai -o output/logo -b true

# 4) Generar PNG DTF desde el SVG resultante
docker run --rm -it -u $(id -u):$(id -g) -v "$(pwd)/output":/app/output felixmurcia/image-converter:latest python -m svg_to_png -i output/logo_sf.svg -o dtf -d 600
```

## 8) Solución de problemas

- Si faltan dependencias en tiempo de ejecución, asegúrese de usar la etiqueta `latest` o la versión deseada publicada en Docker Hub.
- Si obtiene errores por permisos en `output/`, use la opción `-u $(id -u):$(id -g)` como se muestra arriba.

---

Si quieres, puedo añadir un `docker-compose.yml` de ejemplo o actualizar los scripts de la repo para usar directamente la imagen de Docker Hub.
