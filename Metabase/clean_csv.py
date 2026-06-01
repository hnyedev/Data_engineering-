import csv
import os

# Define file paths
input_file_path = os.path.join('raw_data', 'DATAW.csv')
output_file_path = os.path.join('raw_data', 'DATAW_cleaned.csv')

print(f"Iniciando limpieza de {input_file_path}...")

try:
    with open(input_file_path, 'r', encoding='utf-8') as infile,         open(output_file_path, 'w', encoding='utf-8', newline='') as outfile:
        
        # Usar el módulo csv para leer y escribir, es más robusto
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        # La tabla de destino espera 11 columnas
        expected_columns = 11
        
        for i, row in enumerate(reader):
            # 1. Limpiar los caracteres '\r' en cada campo
            cleaned_row = [field.replace('\r', '') for field in row]
            
            # 2. Truncar la fila al número esperado de columnas para eliminar las extras
            trimmed_row = cleaned_row[:expected_columns]
            
            # Escribir la fila limpia en el nuevo archivo
            writer.writerow(trimmed_row)

    print(f"🎉 Limpieza completada. Archivo guardado en: {output_file_path}")
    print(f"Se procesaron {i+1} líneas.")

except FileNotFoundError:
    print(f"❌ Error: No se encontró el archivo de entrada en {input_file_path}")
except Exception as e:
    print(f"❌ Ocurrió un error inesperado: {e}")
