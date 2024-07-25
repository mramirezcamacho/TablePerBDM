import os
import pandas as pd

# Path to the folder containing CSV files
folder_path = 'BDL_tables'

# List all CSV files in the folder and sort them
csv_files = sorted([f for f in os.listdir(folder_path) if f.endswith('.csv')])

# Excel writer object with XlsxWriter as the engine
excel_file = 'AllBDLs.xlsx'
with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
    # Loop through each CSV file, read it into pandas and write to Excel
    for csv_file in csv_files:
        # Extract sheet name from CSV file name (remove extension)
        sheet_name = os.path.splitext(csv_file)[0]

        # Read CSV file into pandas DataFrame
        df = pd.read_csv(os.path.join(folder_path, csv_file),
                         delimiter=',', encoding='utf-8')

        # Write DataFrame to Excel sheet
        df.to_excel(writer, sheet_name=sheet_name, index=False)

print(f'Combined Excel file "{excel_file}" has been created successfully.')
