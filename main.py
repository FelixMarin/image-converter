import os
import sys
from vectorizer import convert_image_to_vector

INPUT_DIR = "input"
OUTPUT_DIR = "output"

def main():
    # Comprobar que input existe
    if not os.path.exists(INPUT_DIR):
        print(f"Error: no existe la carpeta '{INPUT_DIR}'")
        sys.exit(1)

    # Crear output si no existe
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Listar imágenes en input
    files = [f for f in os.listdir(INPUT_DIR)
             if f.lower().endswith((".png", ".jpg", ".jpeg"))]

    if not files:
        print("No hay imágenes en la carpeta input/")
        sys.exit(0)

    for filename in files:
        input_path = os.path.join(INPUT_DIR, filename)

        # Nombre base sin extensión
        base_name = os.path.splitext(filename)[0]

        # Carpeta de salida para esta imagen
        output_subdir = os.path.join(OUTPUT_DIR, base_name)
        os.makedirs(output_subdir, exist_ok=True)

        print(f"\nProcesando: {filename}")

        # Rutas de salida
        svg_path = os.path.join(output_subdir, f"{base_name}.svg")
        ai_path = os.path.join(output_subdir, f"{base_name}.ai")
        png_path = os.path.join(output_subdir, f"{base_name}.png")

        # Ejecutar vectorización
        svg_file, ai_file, png_file = convert_image_to_vector(
            input_path,
            save_svg=True,
            save_ai=True,
            save_png=True
        )

        # Mover archivos generados a la carpeta correspondiente
        if os.path.exists(svg_file):
            os.rename(svg_file, svg_path)
            print(f"SVG generado: {svg_path}")

        if os.path.exists(ai_file):
            os.rename(ai_file, ai_path)
            print(f"AI generado: {ai_path}")

        if os.path.exists(png_file):
            os.rename(png_file, png_path)
            print(f"PNG generado: {png_path}")

    print("\nProceso completado.")

if __name__ == "__main__":
    main()
