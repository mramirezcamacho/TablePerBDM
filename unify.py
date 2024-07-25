import pandas as pd
import os


def csv_to_excel(folder_path, output_excel):
    # Crear un objeto de ExcelWriter
    with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
        # Iterar sobre todos los archivos en la carpeta
        for filename in os.listdir(folder_path):
            if filename.endswith('.csv'):
                file_path = os.path.join(folder_path, filename)
                # Leer el archivo CSV
                df = pd.read_csv(file_path)
                # Eliminar la extensión .csv para usar el nombre del archivo como nombre de la hoja
                sheet_name = os.path.splitext(filename)[0]
                # Guardar el DataFrame en una hoja de Excel
                df.to_excel(writer, sheet_name=sheet_name, index=False)
    print(f"All CSV files have been added to {output_excel}")


# Ejemplo de uso
folder_path = 'BDL_tables'
output_excel = 'AllBDLS2.xlsx'

csv_to_excel(folder_path, output_excel)