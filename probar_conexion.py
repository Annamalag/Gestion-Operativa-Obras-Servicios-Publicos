import gspread
import pandas as pd

# Conectar con las credenciales existentes
gc = gspread.service_account(
    filename="chatbot-para-registro-de-datos-b292d3d251a3.json"
)

# Abrir la hoja de cálculo existente
spreadsheet = gc.open("Registro de accidentes")

# Acceder a las dos pestañas
hoja_residuos = spreadsheet.worksheet("Vol Recolectado")
hoja_accidentes = spreadsheet.worksheet("Accidentes")

# Leer los registros
df_residuos = pd.DataFrame(
    hoja_residuos.get_all_records()
)

df_accidentes = pd.DataFrame(
    hoja_accidentes.get_all_records()
)

print("\nCONEXIÓN EXITOSA")

print("\nRegistros de residuos:")
print(len(df_residuos))

print("\nRegistros de accidentes:")
print(len(df_accidentes))

print("\nPrimeros registros de residuos:")
print(df_residuos.head())

print("\nPrimeros registros de accidentes:")
print(df_accidentes.head())