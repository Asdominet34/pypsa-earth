import pandas as pd
import country_converter as coco

def transform_hydropower_data(input_file_path, output_csv_path, selected_countries):
    # Caricamento del file Excel e lettura del foglio specifico
    excel_data = pd.read_excel(input_file_path, sheet_name="1 - Spatial and technical data", skiprows=2)
    
    # Correggi manualmente eventuali valori specifici nella colonna "Country"
    excel_data["Country"] = excel_data["Country"].replace({"DRC": "CD"})

    # Converti i codici paese in formato ISO alpha-2
    excel_data["Country"] = coco.convert(names=excel_data["Country"], to="iso2")

    # Filtraggio delle centrali per i paesi selezionati
    filtered_data = excel_data[excel_data["Country"].isin(selected_countries)]
    
    # Preparazione delle colonne per il file di output
    rows = []
    for index, row in filtered_data.iterrows():
        name = row["Unit Name"]
        fueltype = "Hydro"
        technology = "Reservoir" if pd.notna(row["Reservoir Size"]) else "Run-Of-River"
        set_type = "PP"
        country = row["Country"]
        capacity = row["Capacity"]
        efficiency = ""
        duration = ""
        volume_Mm3 = row["Reservoir Size"] if pd.notna(row["Reservoir Size"]) else 0
        dam_height_m = ""
        storage_capacity_mwh = ""
        date_in = int(row["First Year"])
        date_retrofit = date_in
        date_out = date_in + 100
        lat = row["Latitude"]
        lon = row["Longitude"]
        eic = ""
        project_id = ""
        bus = ""
        
        # Creazione della riga di output
        rows.append([
            index + 1, name, fueltype, technology, set_type, country, capacity,
            efficiency, duration, volume_Mm3, dam_height_m, storage_capacity_mwh,
            date_in, date_retrofit, date_out, lat, lon, eic, project_id, bus
        ])
    
    # Scrittura del file CSV
    columns = [
        "","Name", "Fueltype", "Technology", "Set", "Country", "Capacity",
        "Efficiency", "Duration", "Volume_Mm3", "DamHeight_m",
        "StorageCapacity_MWh", "DateIn", "DateRetrofit", "DateOut",
        "lat", "lon", "EIC", "projectID", "bus"
    ]
    output_df = pd.DataFrame(rows, columns=columns)
    output_df.to_csv(output_csv_path, index=False)
    
    print(f"File CSV generato: {output_csv_path}")

# Utilizzo del codice
input_file_path = "C:/Users/Davide/pypsa-earth-project/pypsa-earth/data/African_Hydropower_Atlas_v2-0_PoliTechM.xlsx"
output_csv_path = "AHA_custom_powerplants.csv"
selected_countries = ['AO', 'BW', 'CD', 'MW', 'MZ', 'NA', 'SZ', 'TZ', 'ZA', 'ZM', 'ZW']
transform_hydropower_data(input_file_path, output_csv_path, selected_countries)
