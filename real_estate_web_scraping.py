import numpy as np
import pandas as pd
from random import sample
from geopy import distance
from ast import literal_eval


PATH_TO_INPUTS = "C:/Users/loria/Documents/github-projects/work-data_extracting/inputs"
RELAT_PATH_TO_STREETS = PATH_TO_INPUTS+"/nomenclador_de_calles/Nomenclador de Calles.csv"
RELAT_PATH_TO_SQUARE = PATH_TO_INPUTS+"/espacios_verdes_plazas_json.csv"
RELAT_PATH_TO_MALLS = PATH_TO_INPUTS+"/centros_comerciales.csv"
RELAT_PATH_TO_BARRIOS = PATH_TO_INPUTS+"/barrios_json.csv"
df_calles = pd.read_csv(
    RELAT_PATH_TO_STREETS,
    sep=",",
    usecols=["NOMBRE","TIPO","NOMBRE_ABREV","GEOJSON"]
)
# COORD = [-32.935585, -60.647083]
COORD = [-32.946569, -60.674746]

def get_metres_between_nearest_places(self, coord_real_estate, place_type):
    dist = {
        "obj": [],
        "distance_in_km": [],
        "minimun": []    
    }
    nearest_of_real_estate = {
        "obj": None,
        "distance_in_km": None
    }
    if place_type=="avenida":
        df = df_calles[df_calles["TIPO"].str.strip() == "AV"]
    elif place_type=="plaza":
        df = pd.read_csv(
            RELAT_PATH_TO_SQUARE,
            sep=",",
            usecols=["COD_EV_PL","NOMBRE","GEOJSON"]
        )
        df = df[df["COD_EV_PL"] != 0]
        df = df.astype({"NOMBRE": str})
    elif place_type=="paseo_comercial":
        df = pd.read_csv(
            RELAT_PATH_TO_MALLS,
            sep=",",
            usecols=["NOMBRE","GEOJSON"]
        )

    if place_type:
        for _, row in df.iterrows():
            dist_for_coords = []
            dist["obj"].append(row["NOMBRE"].strip())
            for coords in literal_eval(row["GEOJSON"]).get("geometry").get("coordinates"):
                for coord in coords:
                    dist_for_coords.append(distance.distance((coord_real_estate[0], coord_real_estate[1]), (coord[1], coord[0])).km)
            dist["distance_in_km"].append(dist_for_coords)
            dist["minimun"] = sorted(dist["distance_in_km"])[0]
        nearest_of_real_estate["distance_in_km"] = sorted(dist["minimun"])[0]

        i = 0
        for l in dist["distance_in_km"]:
            if not nearest_of_real_estate["distance_in_km"] in l:
                i += 1
            else:
                nearest_of_real_estate["obj"] = dist["obj"][i]
        return nearest_of_real_estate

print(get_metres_between_nearest_places(self=None, coord_real_estate=COORD, place_type="plaza"))