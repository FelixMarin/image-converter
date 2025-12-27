import argparse
import os
import subprocess
from datetime import datetime
from scour import scour
import xml.etree.ElementTree as ET
from PIL import Image

# -----------------------------
#   CONVERTIR .AI → PNG TEMPORAL
# -----------------------------
def ai_to_png(ai_path, temp_dir):
    """
    Convierte un archivo .ai a PNG usando Inkscape.
    Devuelve la ruta del PNG temporal generado.
    """
    os.makedirs(temp_dir, exist_ok=True)

    base_name = os.path.splitext(os.path.basename(ai_path))[0]
    temp_png = os.path.join(temp_dir, f"{base_name}.png")

    try:
        subprocess.run([
            "inkscape",
            ai_path,
            "--export-type=png",
            f"--export-filename={temp_png}"
        ], check=True)

        print(f"✔ Convertido .ai → PNG temporal: {temp_png}")
        return temp_png

    except Exception as e:
        print(f"❌ Error convirtiendo .ai a PNG: {e}")
        return None

# -----------------------------
#   ELIMINAR FONDO DEL SVG
# -----------------------------
def remove_background(svg_path):
    """
    Elimina cualquier rectángulo que cubra el lienzo, sin importar el color.
    También elimina rellenos negros o blancos como fallback.
    """
    try:
        tree = ET.parse(svg_path)
        root = tree.getroot()

        svg_ns = ""
        if root.tag.startswith("{"):
            svg_ns = root.tag.split("}")[0] + "}"

        # Obtener tamaño del lienzo
        view_box = root.attrib.get("viewBox")
        if view_box:
            parts = view_box.strip().split()
            if len(parts) == 4:
                _, _, vb_w, vb_h = parts
                canvas_w = float(vb_w)
                canvas_h = float(vb_h)
            else:
                canvas_w = canvas_h = None
        else:
            try:
                canvas_w = float(root.attrib.get("width", "0").replace("px", ""))
                canvas_h = float(root.attrib.get("height", "0").replace("px", ""))
            except:
                canvas_w = canvas_h = None

        removed = 0
        for elem in list(root):
            if elem.tag == f"{svg_ns}rect":
                x = float(elem.attrib.get("x", "0") or 0)
                y = float(elem.attrib.get("y", "0") or 0)
                w = elem.attrib.get("width")
                h = elem.attrib.get("height")

                if w is None or h is None:
                    continue

                try:
                    w = float(w)
                    h = float(h)
                except:
                    continue

                if canvas_w and canvas_h:
                    if (
                        w >= canvas_w * 0.95 and
                        h >= canvas_h * 0.95 and
                        x <= canvas_w * 0.05 and
                        y <= canvas_h * 0.05
                    ):
                        root.remove(elem)
                        removed += 1
                else:
                    root.remove(elem)
                    removed += 1

        tree.write(svg_path, encoding="utf-8")

        # Fallback: eliminar rellenos negros o blancos
        with open(svg_path, "r", encoding="utf-8") as f:
            svg_text = f.read()

        for color in ["#000000", "#ffffff", "#FFFFFF", "#000", "#fff"]:
            svg_text = svg_text.replace(f'fill="{color}"', 'fill="none"')

        with open(svg_path, "w", encoding="utf-8") as f:
            f.write(svg_text)

        if removed:
            print(f"✔ Eliminado {removed} fondo(s) del SVG")
        else:
            print("✔ No se detectó rectángulo de fondo, solo limpieza de rellenos")

    except Exception as e:
        print(f"⚠ Error al limpiar fondo: {e}")

# -----------------------------
#   OPTIMIZAR Y MINIFICAR SVG
# -----------------------------
def optimize_svg(svg_path):
    try:
        with open(svg_path, "r", encoding="utf-8") as f:
            svg_data = f.read()

        options = scour.sanitizeOptions()
        options.remove_metadata = True
        options.remove_descriptive_elements = True
        options.shorten_ids = True
        options.strip_comments = True
        options.indent_type = None
        options.newlines = False

        optimized = scour.scourString(svg_data, options)

        with open(svg_path, "w", encoding="utf-8") as f:
            f.write(optimized)

        print("✔ SVG optimizado y minificado")

    except Exception as e:
        print(f"⚠ No se pudo optimizar el SVG: {e}")


# -----------------------------
#   CONVERTIR A SVG
# -----------------------------
def convert_to_svg(input_file, output_dir, remove_bg=False):
    if not os.path.exists(input_file):
        print(f"❌ El archivo no existe: {input_file}")
        return

    os.makedirs(output_dir, exist_ok=True)

    base_name = os.path.splitext(os.path.basename(input_file))[0]
    timestamp = datetime.now().strftime("%d%m%Y%H%M%S")
    suffix = "_sf_" if remove_bg else "_cf_"
    suffix += timestamp

    output_svg = os.path.join(output_dir, f"{base_name}{suffix}.svg")

    # -----------------------------
    #   DETECTAR .AI Y CONVERTIRLO
    # -----------------------------
    ext = os.path.splitext(input_file)[1].lower()

    if ext == ".ai":
        print("→ Archivo .ai detectado, convirtiendo a PNG temporal...")
        temp_png = ai_to_png(input_file, "temp")
        if temp_png is None:
            print("❌ No se pudo procesar el archivo .ai")
            return
        input_for_vtracer = temp_png

    elif ext == ".pdf":
        print("→ Archivo PDF detectado, extrayendo imagen...")
        temp_png = pdf_to_png(input_file, "temp")
        if temp_png is None:
            print("❌ No se pudo procesar el archivo PDF")
            return
        input_for_vtracer = temp_png
        if remove_bg:
            print("→ Limpiando fondo negro del PNG antes de vectorizar...")
            clean_png_background_auto(temp_png)
    else:
        input_for_vtracer = input_file

    # -----------------------------
    #   VECTORIZAR CON VTRACER
    # -----------------------------
    print(f"→ Vectorizando {input_for_vtracer} ...")

    try:
        subprocess.run([
            "vtracer",
            "--input", input_for_vtracer,
            "--output", output_svg
        ], check=True)
    except Exception as e:
        print(f"❌ Error ejecutando vtracer: {e}")
        return

    print(f"✔ SVG generado: {output_svg}")

    # -----------------------------
    #   ELIMINAR FONDO SI PROCEDE
    # -----------------------------
    if remove_bg:
        remove_background(output_svg)

    # -----------------------------
    #   OPTIMIZAR SVG
    # -----------------------------
    optimize_svg(output_svg)

    # -----------------------------
    #   ELIMINAR PNG TEMPORAL
    # -----------------------------
    if ext == ".ai":
        try:
            os.remove(input_for_vtracer)
            print(f"✔ PNG temporal eliminado: {input_for_vtracer}")
        except:
            print("⚠ No se pudo eliminar el PNG temporal")

    print("✔ Proceso completado.")

# -----------------------------
#   CONVERTIR PDF → PNG TEMPORAL
# -----------------------------
def pdf_to_png(pdf_path, temp_dir):
    """
    Extrae la primera imagen de un PDF con UNA sola página.
    Si hay más de una imagen, se toma la primera sin error.
    """
    os.makedirs(temp_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]

    # 1. Validar que el PDF tiene solo una página
    try:
        result = subprocess.run(
            ["pdfinfo", pdf_path],
            capture_output=True,
            text=True,
            check=True
        )
        for line in result.stdout.splitlines():
            if "Pages:" in line:
                pages = int(line.split(":")[1].strip())
                if pages != 1:
                    print("❌ El PDF debe tener exactamente UNA página.")
                    return None
                break
    except Exception as e:
        print(f"❌ Error leyendo PDF: {e}")
        return None

    # 2. Extraer imágenes con pdfimages -all (conserva color)
    temp_prefix = os.path.join(temp_dir, base_name)
    try:
        subprocess.run(
            ["pdfimages", "-all", pdf_path, temp_prefix],
            check=True
        )
    except Exception as e:
        print(f"❌ Error extrayendo imágenes del PDF: {e}")
        return None

    # 3. Buscar la primera imagen extraída
    extracted = sorted([
        f for f in os.listdir(temp_dir)
        if f.startswith(base_name)
    ])

    if not extracted:
        print("❌ No se encontró ninguna imagen en el PDF.")
        return None

    first_image = os.path.join(temp_dir, extracted[0])

    # 4. Convertir a PNG si no lo es
    if not first_image.lower().endswith(".png"):
        try:
            from PIL import Image
            img = Image.open(first_image).convert("RGBA")
            png_path = os.path.join(temp_dir, f"{base_name}.png")
            img.save(png_path)
            print(f"✔ Convertido a PNG: {png_path}")
            return png_path
        except Exception as e:
            print(f"❌ Error convirtiendo imagen a PNG: {e}")
            return None
    else:
        print(f"✔ Imagen extraída del PDF: {first_image}")
        return first_image

def clean_png_background_auto(png_path, tolerance=10):
    """
    Detecta automáticamente el color de fondo (muestreando bordes)
    y lo elimina del PNG haciéndolo transparente.
    tolerance: diferencia máxima por canal para considerar que es "mismo color".
    """
    try:
        from PIL import Image

        img = Image.open(png_path).convert("RGBA")
        w, h = img.size
        pixels = img.load()

        # Muestrear esquinas y bordes
        samples = []
        border_points = [
            (0, 0),
            (w - 1, 0),
            (0, h - 1),
            (w - 1, h - 1),
            (w // 2, 0),
            (w // 2, h - 1),
            (0, h // 2),
            (w - 1, h // 2),
        ]
        for x, y in border_points:
            r, g, b, a = pixels[x, y]
            samples.append((r, g, b))

        # Calcular color medio de fondo
        avg_r = sum(s[0] for s in samples) // len(samples)
        avg_g = sum(s[1] for s in samples) // len(samples)
        avg_b = sum(s[2] for s in samples) // len(samples)
        bg_color = (avg_r, avg_g, avg_b)
        print(f"✔ Color de fondo detectado (aprox): {bg_color}")

        def is_bg(c):
            return (
                abs(c[0] - bg_color[0]) <= tolerance and
                abs(c[1] - bg_color[1]) <= tolerance and
                abs(c[2] - bg_color[2]) <= tolerance
            )

        # Crear nueva imagen sin fondo
        new_data = []
        for (r, g, b, a) in img.getdata():
            if is_bg((r, g, b)):
                new_data.append((r, g, b, 0))  # transparente
            else:
                new_data.append((r, g, b, a))

        img.putdata(new_data)
        img.save(png_path)
        print("✔ Fondo eliminado del PNG según color detectado")

    except Exception as e:
        print(f"⚠ No se pudo limpiar el fondo del PNG: {e}")


# -----------------------------
#   MAIN CLI
# -----------------------------
def main():
    parser = argparse.ArgumentParser(description="Convertir imagen a SVG optimizado")
    parser.add_argument("-i", "--input", required=True, help="Ruta del archivo de entrada")
    parser.add_argument("-o", "--output", help="Carpeta de salida")
    parser.add_argument("-b", "--background", default="false",
                        help="Eliminar fondo (true/false). Por defecto: false")

    args = parser.parse_args()

    remove_bg = args.background.lower() == "true"

    if args.output:
        output_dir = args.output
    else:
        base_name = os.path.splitext(os.path.basename(args.input))[0]
        output_dir = os.path.join("output", base_name)

    convert_to_svg(args.input, output_dir, remove_bg)


if __name__ == "__main__":
    main()
