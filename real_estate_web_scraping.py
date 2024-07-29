import pandas as pd


PATH = "C:/Users/loria/Documents/github-projects/work-data_extracting/output/"

df = pd.read_json(PATH+"argenprop.json")
df = df.astype({"avenida": str})
cols = [
    "price_per_m2",
    "acceso_condominio",
    "condominio",
    "avenida",
    "vista_rio",
    "parque",
    "plaza",
    "paseo_comercial",
    #"barrio",
    "dormitorios",
    "baños",
    "cocheras",
    "superficie_total",
    "pileta",     
    "amenities"
]
BARRIOS_TO_CLEAN = {
    "Nuestra señora de lourdes": "Ntra sra de lourdes",
    "Ntra sra, de la guardia": "Ntra sra de la guardia",
    "Republica de la 6ta": "Republica de la sexta"
}
df = df[df["avenida"].str.contains("LEN") == False]
df = df[df["avenida"].str.contains("2") == False]
df = df[df["barrio"] != None]
df = df[df["price_per_m2"] != 0.0]

def clean_barrios(df):
    barrios_all = []
    barrios_to_delete = []
    for indx, row in df.iterrows():
        barrio_from_df = row["barrio"].capitalize() if row["barrio"] is not None else row["barrio"]
        for b in list(BARRIOS_TO_CLEAN.keys()):
            if barrio_from_df == b:
                df.at[indx, "barrio"] = BARRIOS_TO_CLEAN.get(b)
                break
            else:
                df.at[indx, "barrio"] = barrio_from_df
        barrios_all.append(df.at[indx, "barrio"])
    barrios = list(set(barrios_all))
    for i in range(barrios.__len__()):
        if barrios_all.count(barrios[i]) == 1:
            barrios_to_delete.append(barrios[i])
    df = df.drop(df[df["barrio"].isin(barrios_to_delete)].index)
    df = df.astype({"avenida": int})
    return barrios, df


def save_variables(df, columns):
    df_vars = df.drop(["url","address","calle_cleaning", "real_estate_coords","description"], axis=1)
    for barrio in barrios:
        df_vars[barrio] = None
    for indx, row in df_vars.iterrows():
        for barrio in barrios:
            df_vars.at[indx, barrio] = 1 if row["barrio"] == barrio else 0
    df_vars = df_vars.drop(["barrio"], axis=1)
    df_vars.to_excel(PATH+"variables.xlsx", columns=columns)

barrios, df_all_barrio_cleaning = clean_barrios(df)

save_variables(df_all_barrio_cleaning.sample(500), cols.extend(barrios))