import pandas as pd

# Define the paths to your CSV files
csv1 = 'path/to/your/first_file.csv'
csv2 = 'path/to/your/second_file.csv'
csv3 = 'path/to/your/third_file.csv'

# Read the CSV files into DataFrames
df1 = pd.read_csv(csv1)
df2 = pd.read_csv(csv2)
df3 = pd.read_csv(csv3)

# Create a Pandas Excel writer using openpyxl as the engine
with pd.ExcelWriter('combined_file.xlsx', engine='openpyxl') as writer:
    # Write each DataFrame to a different sheet
    df1.to_excel(writer, sheet_name='Sheet1', index=False)
    df2.to_excel(writer, sheet_name='Sheet2', index=False)
    df3.to_excel(writer, sheet_name='Sheet3', index=False)

print("Files have been combined into combined_file.xlsx")
