#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convertidor de archivos .txt con colores hexadecimales a archivos .pal
Para sprites de Pokémon ROM hacking
"""

import os
import sys

def hex_to_rgb(hex_color):
    """Convierte color hexadecimal a RGB"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def read_colors_from_txt(txt_file):
    """Lee colores hexadecimales desde archivo .txt"""
    colors = []
    try:
        with open(txt_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and line.startswith('#'):
                    colors.append(line)
        return colors
    except Exception as e:
        print(f"Error leyendo {txt_file}: {e}")
        return []

def create_pal_file(hex_colors, output_filename):
    """Crea archivo .pal desde lista de colores hexadecimales"""
    
    # Header del archivo PAL (Microsoft RIFF palette format)
    pal_content = bytearray()
    
    # RIFF header
    pal_content.extend(b'RIFF')
    
    # Tamaño del archivo (se calculará después)
    file_size_pos = len(pal_content)
    pal_content.extend(b'\x00\x00\x00\x00')  # Placeholder
    
    # PAL header
    pal_content.extend(b'PAL ')
    pal_content.extend(b'data')
    
    # Tamaño de los datos de paleta
    data_size = 4 + (len(hex_colors) * 4)  # 4 bytes header + 4 bytes por color
    pal_content.extend(data_size.to_bytes(4, 'little'))
    
    # Versión de paleta (0x0300)
    pal_content.extend(b'\x00\x03')
    
    # Número de colores
    pal_content.extend(len(hex_colors).to_bytes(2, 'little'))
    
    # Colores (formato RGBA, pero A siempre es 0)
    for hex_color in hex_colors:
        r, g, b = hex_to_rgb(hex_color)
        pal_content.extend(bytes([r, g, b, 0]))  # RGBA
    
    # Actualizar tamaño del archivo
    file_size = len(pal_content) - 8  # Tamaño total menos header RIFF
    pal_content[file_size_pos:file_size_pos+4] = file_size.to_bytes(4, 'little')
    
    # Escribir archivo
    with open(output_filename, 'wb') as f:
        f.write(pal_content)
    
    print(f"✓ Archivo {output_filename} creado exitosamente!")
    print(f"  Colores incluidos: {len(hex_colors)}")

def create_gpl_file(hex_colors, output_filename, palette_name):
    """Crea archivo .gpl (GIMP palette) desde lista de colores hexadecimales"""
    with open(output_filename, 'w') as f:
        f.write("GIMP Palette\n")
        f.write(f"Name: {palette_name}\n")
        f.write("Columns: 4\n")
        f.write("#\n")
        
        for i, hex_color in enumerate(hex_colors):
            r, g, b = hex_to_rgb(hex_color)
            f.write(f"{r:3d} {g:3d} {b:3d} Color {i+1}\n")
    
    print(f"✓ Archivo {output_filename} creado exitosamente!")

def process_txt_files(input_path, output_dir=None):
    """Procesa archivos .txt en la ruta especificada"""
    
    if output_dir is None:
        output_dir = os.path.dirname(input_path) if os.path.isfile(input_path) else input_path
    
    # Si es un archivo específico
    if os.path.isfile(input_path) and input_path.endswith('.txt'):
        txt_files = [input_path]
    # Si es un directorio
    elif os.path.isdir(input_path):
        txt_files = [os.path.join(input_path, f) for f in os.listdir(input_path) if f.endswith('.txt')]
    else:
        print(f"Error: {input_path} no es un archivo .txt válido o directorio")
        return
    
    if not txt_files:
        print(f"No se encontraron archivos .txt en {input_path}")
        return
    
    print(f"Procesando {len(txt_files)} archivo(s) .txt...")
    
    for txt_file in txt_files:
        print(f"\n--- Procesando: {os.path.basename(txt_file)} ---")
        
        # Leer colores del archivo
        colors = read_colors_from_txt(txt_file)
        
        if not colors:
            print(f"⚠ No se encontraron colores válidos en {txt_file}")
            continue
        
        # Generar nombres de salida
        base_name = os.path.splitext(os.path.basename(txt_file))[0]
        pal_output = os.path.join(output_dir, f"{base_name}.pal")
        gpl_output = os.path.join(output_dir, f"{base_name}.gpl")
        
        # Crear archivos
        create_pal_file(colors, pal_output)
        create_gpl_file(colors, gpl_output, base_name)

def main():
    print("=== Convertidor TXT a PAL ===")
    print("Convierte archivos .txt con colores hexadecimales a archivos .pal y .gpl")
    print()
    
    if len(sys.argv) > 1:
        input_path = sys.argv[1]
        output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    else:
        input_path = input("Introduce la ruta del archivo .txt o directorio: ").strip().strip('"')
        output_dir = input("Directorio de salida (Enter para usar el mismo): ").strip().strip('"')
        if not output_dir:
            output_dir = None
    
    if not os.path.exists(input_path):
        print(f"Error: La ruta {input_path} no existe")
        return
    
    process_txt_files(input_path, output_dir)
    print("\n¡Conversión completada!")

if __name__ == "__main__":
    main()
