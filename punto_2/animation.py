import os
import time
import imageio.v2 as imageio
import re
from PIL import Image, ImageDraw, ImageFont

def sort_numerically(data):
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(data, key=alphanum_key)

root_dir = 'images/ga'
output_path = 'output.gif'
scale_factor = 0.5  # Reducir la imagen a la mitad de su tamaño original

# Configuración para escribir texto en la imagen
font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"  # Ajusta la ruta a tu fuente
font_size = 80
font_color = (0, 0, 0)  # Color blanco

print("Explorando directorios...")
with imageio.get_writer(output_path, mode='I', duration=0.5) as writer:
    for subdir in sort_numerically(os.listdir(root_dir)):
        subdir_path = os.path.join(root_dir, subdir)
        if os.path.isdir(subdir_path):
            # Extraer el número de iteración del nombre de la carpeta
            iteration_number = re.search(r'\d+', subdir).group()
            print(f"Entrando en el directorio: {subdir_path}")
            files = sort_numerically(os.listdir(subdir_path))
            for file in files:
                if file.startswith('ruta_') and file.endswith('.png'):
                    full_path = os.path.join(subdir_path, file)
                    print(f"Añadiendo imagen: {full_path}")
                    img = Image.open(full_path)
                    # Reducir el tamaño de la imagen
                    img = img.resize((int(img.width * scale_factor), int(img.height * scale_factor)), Image.Resampling.LANCZOS)
                    # Preparar para añadir texto
                    draw = ImageDraw.Draw(img)
                    font = ImageFont.truetype(font_path, font_size)
                    text = f"Iteración {iteration_number}"
                    # Calcular la posición para el texto usando getbbox
                    bbox = font.getbbox(text)
                    textwidth, textheight = bbox[2] - bbox[0], bbox[3] - bbox[1]
                    
                    # quiero que quede centrado arriba en la imagen
                    position = (img.width // 2 - textwidth // 2, 100)

                    # Escribir el texto en la imagen
                    draw.text(position, text, font_color, font=font)

                    # Escribir el costo que tuvo dicha iteración obteniendola del json

                    json_path = os.path.join('json/ga', f'ruta_{iteration_number}.json')

                    # ejemplo contenido json { "ruta" : [], "costo": 123.45 }
                    with open(json_path, 'r') as file:
                        import json
                        data = json.load(file)
                        costo = data['costo']
                    
                    # Escribir el costo en la imagen, bajo la iteracion y con una fuente mas pequeña
                    font_size = 40
                    font = ImageFont.truetype(font_path, font_size)
                    text = f"Costo: {round(costo, 2)}"
                    bbox = font.getbbox(text)
                    textwidth, textheight = bbox[2] - bbox[0], bbox[3] - bbox[1]
                    position = (img.width // 2 - textwidth // 2, 200)
                    draw.text(position, text, font_color, font=font)

                        


                    # Guardar temporalmente para evitar errores de formato
                    img.save("temp.png")
                    # Leer la imagen modificada para añadir al GIF
                    img_array = imageio.imread("temp.png")
                    writer.append_data(img_array)

                    # Eliminar el archivo temporal
                    os.remove("temp.png")

                    

print(f'GIF creado exitosamente en {output_path}')
