import argparse
import os
from datetime import datetime
import cairosvg
from PIL import Image

# -----------------------------
#   OPTIMIZAR PNG (minificar)
# -----------------------------
def optimize_png(png_path):
    """
    Minifica el PNG usando Pillow (optimize=True).
    """
    try:
        img = Image.open(png_path)
        img.save(png_path, optimize=True)
        print("✔ PNG optimizado")
    except Exception as e:
        print(f"⚠ No se pudo optimizar el PNG: {e}")


# -----------------------------
#   CONVERTIR SVG → PNG
# -----------------------------
def convert_svg_to_png(input_svg, output_dir, dpi=600):
    if not os.path.exists(input_svg):
        print(f"❌ El archivo no existe: {input_svg}")
        return

    os.makedirs(output_dir, exist_ok=True)

    base_name = os.path.splitext(os.path.basename(input_svg))[0]

    # Timestamp
    timestamp = datetime.now().strftime("%d%m%Y%H%M%S")

    # Sufijo para PNG DTF
    suffix = f"_dtf_{timestamp}"

    output_png = os.path.join(output_dir, f"{base_name}{suffix}.png")

    print(f"→ Convirtiendo SVG a PNG DTF ({dpi} DPI)...")

    try:
        cairosvg.svg2png(
            url=input_svg,
            write_to=output_png,
            dpi=dpi,
            background_color=None  # Transparencia real
        )
    except Exception as e:
        print(f"❌ Error convirtiendo SVG a PNG: {e}")
        return

    print(f"✔ PNG generado: {output_png}")

    # Optimizar PNG
    optimize_png(output_png)

    print("✔ Proceso completado.")


# -----------------------------
#   MAIN CLI
# -----------------------------
def main():
    parser = argparse.ArgumentParser(description="Convertir SVG a PNG para impresión DTF")
    parser.add_argument("-i", "--input", required=True, help="Ruta del archivo SVG de entrada")
    parser.add_argument("-o", "--output", help="Carpeta de salida")
    parser.add_argument("-d", "--dpi", default="600", help="Resolución en DPI (por defecto 600)")

    args = parser.parse_args()

    dpi = int(args.dpi)

    # Si no se indica -o → output/<nombre_svg>
    if args.output:
        output_dir = args.output
    else:
        base_name = os.path.splitext(os.path.basename(args.input))[0]
        output_dir = os.path.join("output", base_name)

    convert_svg_to_png(args.input, output_dir, dpi)


if __name__ == "__main__":
    main()
