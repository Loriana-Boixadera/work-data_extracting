import pandas as pd
import numpy as np
# from geopy.geocoders import Nominatim

from shapely.geometry.polygon import Polygon
import geopandas as gpd
import folium
from folium.plugins import BeautifyIcon
import json
import webbrowser
import matplotlib.pyplot as plt
import contextily as cx
import io
from PIL import Image



PATH = "C:/Users/loria/Documents/github-projects/work-data_extracting/"
# geolocator = Nominatim(user_agent="geoapiExercises")

# df_real_estates = pd.read_excel(PATH+"Tbl-vars-direccion.xlsx", index_col=None)
df_paseos_comerciales = pd.read_csv(PATH+"inputs/centros_comerciales-Juan.csv", index_col=None)

for idx, row in df_paseos_comerciales.iterrows():
    coords = json.loads(row["GEOJSON"])["geometry"]["coordinates"][0][0]
    df_paseos_comerciales.at[idx,"LAT"] = coords[0]
    df_paseos_comerciales.at[idx,"LONG"] = coords[1]
df_paseos_comerciales.drop("GEOJSON", axis=1, inplace=True)

# cols_rename = {
#     "price_per_m2"      : "precio_por_m2",
#     "superficie_total"  : "superficie",
#     "dormitorios"       : "dormitorios",
#     "baños"             : "baños",
#     "cocheras"          : "cocheras",
#     "pileta"            : "pileta",
#     "amenities"         : "amenities",
#     "condominio"        : "condominio",
#     "avenida"           : "avenida",
#     "acceso_condominio" : "acceso_condominio",
#     "plaza"             : "plaza",
#     "parque"            : "parque",
#     "vista_rio"         : "río",
#     "paseo_comercial"   : "centro_comercial",
#     # "barrios" ....
#     "address"           : "direccion"
# }
# BARRIOS_TO_CLEAN = {
#     "Nuestra señora de lourdes": "Ntra sra de lourdes",
#     "Ntra sra, de la guardia": "Ntra sra de la guardia",
#     "Republica de la 6ta": "Republica de la sexta"
# }

# BARRIOS_TO_JOIN = {
#     "Barrio Arroyito": ["Arroyito", "Lisandro de la torre"],
#     "Barrios Zona Oeste": ["Antartida argentina", "Belgrano", "Urquiza"],
#     "Barrios Zona Norte": ["Alberdi", "La florida", "Sarmiento"],
#     "Barrio Luis Agote": ["Ludueña", "Luis agote"],
#     "Barrios Zona Sur-Centro": [
#         "Republica de la sexta", "España y hospitales",
#         "General jose de san martin", "Parque casado", "Parque",
#         "Latinoamerica", "Jorge cura"
#     ],
#     "Barrios Zona Sur-Sur": [
#         "Alvear", "Matheu", "General las heras",
#         "La tablada", "Tiro suizo", "Las flores",
#         "Triangulo y moderno", "Ntra sra de la guardia",
#         "Las delicias"
#     ],
#     "Barrios Zona Oeste-Centro": [
#         "Bella vista", "Remedios de escalada de san martin", "Cinco esquinas"
#     ],
#     "Zona Barrio Pichincha": ["Alberto olmedo", "Pichincha"],
#     "Barrio Centro": ["Centro"],
#     "Barrio Abasto": ["Abasto"],
#     "Barrio Echesortu": ["Echesortu"],
#     "Barrio Fisherton": ["Fisherton"],
#     "Barrio Las Malvinas": ["Las malvinas"],
#     "Barrio Martin": ["Martin"],
#     "Barrio Ntra Sra de Lourdes": ["Ntra sra de lourdes"],
#     "Barrio Puerto Norte": ["Puerto norte"],
#     "Barrio Refinerías": ["Refinerias"],
#     "Barrio Rucci": ["Rucci", "La ceramica y cuyo"]
# }

# def clean_barrios(df_real_estates):
#     # barrios_all = []
#     for indx, row in df_real_estates.iterrows():
#         if "F.o.n.a.v.i" in row["barrio"]:
#             df_real_estates.at[indx, "barrio"] = "Antartida argentina"
#         if "Tablada /" in row["barrio"]:
#             df_real_estates.at[indx, "barrio"] = "La tablada"
#         if "sur y norte" in row["barrio"]:
#             df_real_estates.at[indx, "barrio"] = "Ludueña"
#         if "Del abasto" in row["barrio"]:
#             df_real_estates.at[indx, "barrio"] = "Abasto"
#         if "España" in row["barrio"]:
#             df_real_estates.at[indx, "barrio"] = "España y hospitales"
#     #    barrios_all.append(df_real_estates.at[indx, "barrio"])
#     # barrios = list(set(barrios_all))
#     # barrios.sort()
#     # print(barrios)
#     return df_real_estates

# def get_key(my_dict, val):
#     for key, values in my_dict.items():
#         if val in values:
#             return key
#     return "key doesn't exist"

# def reverse_geocoding(lat, lon):
#     try:
#         # location = geolocator.reverse(Point(lat, lon))
#         location = geolocator.geocode(str(lat)+","+str(lon))
#         return ",".join(location.address.split(",")[:3])
#     except:
#         return None

# def save_variables(df_real_estates, columns):
#     for barrio in list(BARRIOS_TO_JOIN.keys()):
#         df_real_estates[barrio] = None
#     for indx, row in df_real_estates.iterrows():
#         for c_barrios in list(BARRIOS_TO_JOIN.values()):
#             df_real_estates.at[indx, get_key(BARRIOS_TO_JOIN, c_barrios[0])] = 1 if row["barrio"] in c_barrios else 0
#     for idx, row in df_real_estates.iterrows():
#         address_c = reverse_geocoding(row["lat"], row["long"])
#         df_real_estates.at[idx, "address_clean"] = address_c if address_c != None else row["address"]
#     df_real_estates_vars = df_real_estates.drop(["barrio"], axis=1)
#     df_real_estates_vars.to_excel("testing2.xlsx", index=False) # Tbl-vars-direccion.xlsx
#     # df_real_estates_vars.rename(columns=columns, inplace=True)
#     # df_real_estates_vars.to_excel(PATH+"variables1_clean.xlsx")

# # df_real_estates_all_barrios_cleaning = clean_barrios(df_real_estates)

# # save_variables(df_real_estates_all_barrios_cleaning, list(cols_rename.keys()).extend(list(BARRIOS_TO_JOIN.keys())))

# # # df_real_estates_all_barrios_cleaning = df_real_estates_all_barrios_cleaning.drop(["url","calle_cleaning", "description","real_estate_coords"], axis=1)
# # # df_real_estates_all_barrios_cleaning.to_csv(PATH+"argenprop_clean.csv")

barrios = [
    "Barrio Arroyito",
    "Barrios Zona Oeste",
    "Barrios Zona Norte",
    "Barrio Luis Agote",
    "Barrios Zona Sur-Centro",
    "Barrios Zona Sur-Sur",
    "Barrios Zona Oeste-Centro",
    "Zona Barrio Pichincha",
    "Barrio Centro",
    "Barrio Abasto",
    "Barrio Echesortu",
    "Barrio Fisherton",
    "Barrio Las Malvinas",
    "Barrio Martin",
    "Barrio Ntra Sra de Lourdes",
    "Barrio Puerto Norte",
    "Barrio Refinerías",
    "Barrio Rucci"
]

# DEPARTAMENTOS

# DEPTOS S/ PRECIO      | COLOR     |   RANGO PRECIO
## BAJOS                | #FABF8F   |   214 - 1286
## MEDIO BAJOS          | #DA9694   |   1287 - 1634
## MEDIO SUPERIORES     | #E26B0A   |   1635 - 2050
## SUPERIORES           | #963634   |   2051 - 5545

# for c_barrio in barrios:
#     for indx, row in df_real_estates.iterrows():
#         if 214.0 <= row["price_per_m2"] <= 1286.0:
#             df_real_estates.at[indx,"color"] = "#FABF8F"
#             df_real_estates.at[indx,"Precios"] = "Bajos"
#         if 1287.0 <= row["price_per_m2"] <= 1634.0:
#             df_real_estates.at[indx,"color"] = "#DA9694"
#             df_real_estates.at[indx,"Precios"] = "Medio Bajos"
#         if 1635.0 <= row["price_per_m2"] <= 2050.0:
#             df_real_estates.at[indx,"color"] = "#E26B0A"
#             df_real_estates.at[indx,"Precios"] = "Medio Superiores"
#         if 2051.0 <= row["price_per_m2"] <= 5545.0:
#             df_real_estates.at[indx,"color"] = "#963634"
#             df_real_estates.at[indx,"Precios"] = "Superiores"
#         if row[c_barrio] == 1:
#             df_real_estates.at[indx,"barrios"] = c_barrio

# geo_df_real_estates = gpd.GeoDataFrame(
#     df_real_estates, geometry=gpd.points_from_xy(df_real_estates["long"], df_real_estates["lat"]), crs="epsg:4326"#4386
# )

# # DEPTOS S/ PRECIO
# m = geo_df_real_estates.explore(column="Precios", cmap=["lightsalmon","rosybrown","orangered","firebrick"], name="points")
# folium.LayerControl().add_to(m)
# outfp = PATH+"maps/departamentos_segun_precio.html"
# m.save(outfp)
# webbrowser.open(outfp)

# # DEPTOS
# m = geo_df_real_estates.explore(column="barrios", cmap="nipy_spectral", name="points")
# folium.LayerControl().add_to(m)
# outfp = PATH+"maps/departamentos.html"
# m.save(outfp)
# webbrowser.open(outfp)


# PASEOS COMERCIALES
geo_df_centros_comerciales = gpd.GeoDataFrame(
    df_paseos_comerciales, geometry=gpd.points_from_xy(df_paseos_comerciales["LAT"], df_paseos_comerciales["LONG"]), crs="EPSG:4326"
)
# m = geo_df_centros_comerciales.explore(column="NOMBRE", marker_type="marker", name="Residental")
# folium.LayerControl().add_to(m)
# outfp = PATH+"maps/centros_comerciales.html"
# m.save(outfp)
# webbrowser.open(outfp)

## TRY THIS:

geo_df_centros_comerciales["Label"] = range(1, len(geo_df_centros_comerciales)+1)

m = folium.Map(location=geo_df_centros_comerciales.loc[0, ["LONG", "LAT"]].tolist(), zoom_start=12)

cols = ["NOMBRE", "LAT", "LONG", "Label"]
for commercial_centre, lon, lat, label in geo_df_centros_comerciales[cols].to_numpy():

    # feel free to custom the html
    html=f"""<h4>{commercial_centre}</h4>"""

    iframe = folium.IFrame(html=html, width=200, height=150)

    folium.Marker(
        location=[lat, lon], popup=folium.Popup(iframe, max_width=650),
        icon=BeautifyIcon(
            icon="arrow-down",
            icon_shape="marker",
            number=str(label),
            border_color= "#000000",
            background_color="#000000",
            text_color="#FFFFFF"
        )
    ).add_to(m)

geo_df_centros_comerciales.explore(m=m)

outfp = PATH+"maps/centros_comerciales.html"
m.save(outfp)
webbrowser.open(outfp)