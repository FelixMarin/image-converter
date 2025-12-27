import os
import subprocess
import cairosvg

def convert_image_to_vector(input_path, save_svg=True, save_ai=True, save_png=True):
    """
    Convierte una imagen raster a SVG, AI y PNG transparente.
    Devuelve (svg_file, ai_file, png_file)
    """

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"El archivo no existe: {input_path}")

    base_name = os.path.splitext(os.path.basename(input_path))[0]

    svg_file = f"{base_name}.svg" if save_svg else None
    ai_file = f"{base_name}.ai" if save_ai else None
    png_file = f"{base_name}.png" if save_png else None

    # Generar SVG usando el binario CLI de vtracer
    if save_svg:
        subprocess.run([
            "vtracer",
            "--input", input_path,
            "--output", svg_file
        ], check=True)

    # Convertir SVG → AI
    if save_ai:
        cairosvg.svg2pdf(url=svg_file, write_to=ai_file)

    # Convertir SVG → PNG transparente
    if save_png:
        remove_white_background_from_svg(svg_file)
        cairosvg.svg2png(
            url=svg_file,
            write_to=png_file,
            dpi=300,
            background_color=None
    )

    return svg_file, ai_file, png_file

def svg_to_png(svg_path, png_path, dpi=300):
    """
    Convierte un SVG a PNG con fondo transparente.
    """
    cairosvg.svg2png(
        url=svg_path,
        write_to=png_path,
        dpi=dpi,
        background_color=None  # Transparencia
    )
    return png_path

def remove_white_background_from_svg(svg_path):
    """
    Elimina rectángulos o paths blancos del SVG.
    """
    with open(svg_path, "r", encoding="utf-8") as f:
        svg = f.read()

    # Eliminar rectángulos blancos
    svg = svg.replace('<rect width="100%" height="100%" fill="#ffffff"/>', "")
    svg = svg.replace('<rect width="100%" height="100%" fill="#FFFFFF"/>', "")

    # Eliminar paths blancos comunes
    svg = svg.replace('fill="#ffffff"', 'fill="none"')
    svg = svg.replace('fill="#FFFFFF"', 'fill="none"')

    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg)
