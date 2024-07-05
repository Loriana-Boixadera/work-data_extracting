import re
import pandas as pd

#     street_type = self.return_street_type(df, calle)
#   File "C:\Users\loria\Documents\github-projects\work-data_extracting\scraprealestate\scraprealestate\spiders\realestatespider.py", line 166, in return_street_type
#     street_type = "1" if df["TIPO"].item().strip() == "C" else "0"
#   File "C:\Users\loria\Documents\github-projects\work-data_extracting\venv\lib\site-packages\pandas\core\base.py", line 418, in item
#     raise ValueError("can only convert an array of size 1 to a Python scalar")
# ValueError: can only convert an array of size 1 to a Python scalar

PATH_TO_FILE = "C:/Users/loria/Documents/github-projects/work-data_extracting/nomenclador_de_calles/Nomenclador de Calles.csv"
df_calles = pd.read_csv(
                PATH_TO_FILE,
                sep=",",
                usecols=["NOMBRE","TIPO","NOMBRE_ABREV"]
            )

streets = [
    "SAN LUIS al 1400",
    "Alem 1229 | Monoambiente (09-02)",
    "ALEM 1200",
    "COLON al 2400",
    "Alvear 300, Piso 01",
    "San Juan 1800",
    "Montevideo 1596",
    "Republica Siria 100, Piso 2º",
    "Urquiza 2700",
    "Catamarca al 1300",
    "1 De Mayo 900, Piso 6",
    "Dorrego al 100",
    "Tucuman  al 3500",
    "Torres Dolfines",
    "Rioja 3759",
    "Maipú 2200, Piso 10",
    "San Lorenzo 1754",
    "Dorrego 34",
    "Sarmiento 1550 | 1 Dormitorio (01-01)",
    "Juan Manuel De Rosas 1500, Piso 4",
    "Pasco al 1800 2 dormitorios",
    "Alsina 540 08-01 2 dormitorios Apto Credito",
    "Maui - Av Estanislao Lopez 2600. 44 - 1A",
    "Vera Mújica 860",
    "Mendoza N° 200",
    "Pte. Roca 1500",
    "Italia 690 (06-01)",
    "Tucumán al 2600 Monoambientes",
    "Güemes  2018 - Parque España",
    "Juan Manuel De Rosas 1100",
    "Tucumán al 2600 1Dormitorio",
    "Vera Mujica 1352 - Edificio Silene II",
    "Avenida Jorge Newbery al 9100",
    "Bv. Oroño 600",
    "MAUI. Av. Estanislao Lopez 2671. S31A2",
    "9 de julio  357 | 1 dormitorio (2-03)",
    "Callao 400",
    "Bv. Avellaneda 1080 bis - Torre Brisa - Vista Rio",
    "Paraguay 1800, Piso 2",
    "9 de Julio 3800, Piso 3",
    "Av. Pellegrini  4043 | Monoambiente"
]


def replace_accent(address_to_parse): # self
    dict_letter = {
        "Á" : "A",
        "É" : "E",
        "Í" : "I",
        "Ó" : "O",
        "Ú" : "U",
        "Ü" : "U",
        "Ñ" : "N"
    }
    for elem in ["Á","É","Í","Ó","Ú","Ü","Ñ"]:
        if elem in address_to_parse:
            address_to_parse = address_to_parse.replace(elem, dict_letter.get(elem))
        else:
            continue
    return address_to_parse

def parse_street(street): # self
    street = re.split(r"\s\d", street)[0]
    if "MAUI" in street:
        street = street.split("MAUI")[1]
        if " - " in street:
            street = street.split(" - ")[1]
    if " AL" in street:
        street = street.split(" AL")[0]
    if "AV" in street:
        try:
            street = re.split(r"AV[.|\s]", street)[1].strip()
        except:
            pass
    if "BV" in street:
        try:
            street = re.split(r"BV[.|\s]", street)[1].strip()
        except:
            pass
    if "1" in street:
        street = street.replace("1", "PRIMERO")
    if "TORRES DOLFINES" in street:
        street = "ESTANISLAO LOPEZ"
    if "N°" in street:
        street = street.replace("N°", "").strip()
    if "º" in street:
        street = street.replace("º", "").strip()
    if "ROCA" in street:
        street = "PTE. ROCA"
    if "AVENIDA " in street:
        street = street.replace("AVENIDA ", "")
    for elem in ["'","-","|",","]:
        if elem in street:
            street = street.split(elem)[0].strip()
    if "COLON" in street:
        street = "C. COLON"
    if "ALVEAR" in street:
        street = "MARCELO ALVEAR"
    return street

# def return_street_type(df, calle): # self
#     df1 = df[df["NOMBRE_ABREV"].str.strip() == calle[0]]
#     df2 = df[df["NOMBRE"].str.strip() == calle[0]]
#     if df1.empty and df2.empty:
#         if calle.__len__() >= 3:
#             df = df[(
#                         df["NOMBRE_ABREV"].str.contains(calle[0]) &
#                         df["NOMBRE_ABREV"].str.contains(calle[1]) &
#                         df["NOMBRE_ABREV"].str.contains(calle[2])
#                     ) | (
#                         df["NOMBRE"].str.contains(calle[0]) &
#                         df["NOMBRE"].str.contains(calle[1]) &
#                         df["NOMBRE"].str.contains(calle[2])
#                     )
#                 ]
#             if not df.empty:
#                 street_type = "1" if df["TIPO"].item().strip() == "C" else "0"
#             else: street_type = "LEN Greater 3 - STREET NOT FOUND"
#         elif calle.__len__() == 2:
#             df = df[(
#                         df["NOMBRE_ABREV"].str.contains(calle[0]) &
#                         df["NOMBRE_ABREV"].str.contains(calle[1])
#                     ) | (
#                         df["NOMBRE"].str.contains(calle[0]) &
#                         df["NOMBRE"].str.contains(calle[1])
#                     )]
#             if not df.empty:
#                 street_type = "1" if df["TIPO"].item().strip() == "C" else "0"
#             else: street_type = "LEN 2 - STREET NOT FOUND"
#         elif calle.__len__() == 1:
#             df = df[df["NOMBRE"].str.contains(calle[0]) | df["NOMBRE_ABREV"].str.contains(calle[0])]
#             if not df.empty:
#                 street_type = "1" if df["TIPO"].item().strip() == "C" else "0"
#             else: street_type = "LEN 1 - STREET NOT FOUND"
#         else: street_type = None
#     else:
#         try: street_type = "1" if df1["TIPO"].item().strip() == "C" else "0"
#         except:
#             try: street_type = "1" if df2["TIPO"].item().strip() == "C" else "0"
#             except: street_type = "NOT FOUND"
#     return street_type

def get_street_type(address): # self
    calle = replace_accent(parse_street(address.upper())).strip().split(" ")

    if calle.__len__() == 1:
        df = df_calles[
            (df_calles["NOMBRE"].str.strip() == calle[0]) |
            (df_calles["NOMBRE_ABREV"].str.strip() == calle[0])
        ]
        if not df.empty:
            street_type = "1" if df["TIPO"].item().strip() == "C" else "0"
        else:
            df = df_calles[
                df_calles["NOMBRE"].str.contains(fr"\s{calle[0]}\s") |
                df_calles["NOMBRE_ABREV"].str.contains(fr"\s{calle[0]}\s")
            ]
            if not df.empty:
                street_type = "1" if df["TIPO"].item().strip() == "C" else "0"
            else:
                street_type = "LEN 1 - ELSE with regex searching"
    elif calle.__len__() == 2:
        df = df_calles[
            (df_calles["NOMBRE"].str.strip() == " ".join(calle[:2])) |
            (df_calles["NOMBRE_ABREV"].str.strip() == " ".join(calle[:2])) |
            (df_calles["NOMBRE"].str.strip() == calle[-1] + " " + calle[-2]) |
            (df_calles["NOMBRE_ABREV"].str.strip() == calle[-1] + " " + calle[-2])
        ]
        if not df.empty:
            street_type = "1" if df["TIPO"].item().strip() == "C" else "0"
        else:
            df = df_calles[(
                    df_calles["NOMBRE"].str.contains(calle[0]) &
                    df_calles["NOMBRE"].str.contains(calle[1])
                ) | (
                    df_calles["NOMBRE_ABREV"].str.contains(calle[0]) &
                    df_calles["NOMBRE_ABREV"].str.contains(calle[1])
                ) | (
                    df_calles["NOMBRE"].str.contains(calle[1]) &
                    df_calles["NOMBRE"].str.contains(calle[0])
                ) | (
                    df_calles["NOMBRE_ABREV"].str.contains(calle[1]) &
                    df_calles["NOMBRE_ABREV"].str.contains(calle[0])
                )
            ]
            if not df.empty:
                street_type = "1" if df["TIPO"].item().strip() == "C" else "0"
            else: street_type = "LEN 2 - ELSE with regex searching"
    else:
        df = df_calles[(
                    df_calles["NOMBRE_ABREV"].str.contains(calle[0]) &
                    df_calles["NOMBRE_ABREV"].str.contains(calle[1]) &
                    df_calles["NOMBRE_ABREV"].str.contains(calle[2])
                ) | (
                    df_calles["NOMBRE"].str.contains(calle[0]) &
                    df_calles["NOMBRE"].str.contains(calle[1]) &
                    df_calles["NOMBRE"].str.contains(calle[2])
                )
            ]
        if not df.empty:
            street_type = "1" if df["TIPO"].item().strip() == "C" else "0"
        else:
            street_type = "LEN Greater 3 - STREET NOT FOUND"
    return calle, street_type