import pandas as pd

# Percorso del file di input
input_excel_path = r"C:/Users/Davide/Downloads/PyPSA_all/custom_powerplants/powerplantmatching_original.xlsx"
input_csv_path = r"C:/Users/Davide/pypsa-earth-project/AHA_to_OSeMOSYS_ssp585.csv"
output_csv_path = r"C:/Users/Davide/pypsa-earth-project/custom_powerplants_ssp585.csv"

# Caricamento del file Excel in un DataFrame
df = pd.read_excel(input_excel_path)

# Rimozione della colonna "region_id" e svuotamento di colonne specifiche
if "region_id" in df.columns:
    df = df.drop(columns=["region_id"])
if "EIC" in df.columns:
    df["EIC"] = ""
if "projectID" in df.columns:
    df["projectID"] = ""
if "bus" in df.columns:
    df["bus"] = ""

# Rimuovi completamente la colonna "Unnamed: 0", se esiste
if "Unnamed: 0" in df.columns:
    df = df.drop(columns=["Unnamed: 0"])

# Filtra righe dove Fueltype non è "Hydro", ma mantiene le righe con Technology = "Pumped Storage"
df = df[(df["Fueltype"] != "Hydro") | (df["Technology"] == "Pumped Storage")]

# Modifica degli indici per partire da 400
df.index = range(405, 405 + len(df))

# Filtra righe dove "DateOut" è maggiore di 2049 o dove "DateOut" è nullo
if "DateOut" in df.columns:
    df = df[(df["DateOut"].isnull()) | (df["DateOut"] > 2049)]

print(df)

# Leggi il file CSV esistente come semplice testo per evitare l'errore dell'indice
with open(input_csv_path, 'r') as f:
    existing_rows = f.readlines()

# Converte il DataFrame in una lista di righe CSV
new_rows = df.to_csv(index=True, header=False).splitlines()

# Combina le righe esistenti con le nuove
final_rows = existing_rows + [row + "\n" for row in new_rows]

# Scrivi il risultato finale nel file di output
with open(output_csv_path, 'w') as f:
    f.writelines(final_rows)

print(f"File salvato in: {output_csv_path}")
