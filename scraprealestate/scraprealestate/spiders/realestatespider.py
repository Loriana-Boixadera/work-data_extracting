import re
import gc
import scrapy
import numpy as np
import pandas as pd
from random import sample
from geopy import distance
from ast import literal_eval
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


# There is real estate agency:
#       - Argenprop --> por pag muestra 20 / (500) 30 paginas a consultar --> Scrapy

# AT the end save:
#   - All variables for each real estate
#   - Map with references
#   - Program Workflow and a short non-tecnic description about the function

AMENITIES = [
    "piscina",
    "pileta"
    "salondeusosmúltiples",
    "SUM",
    "gimnasio",
    "parrilla",
    "spa",
    "sauna",
    "saladecine",
    "solarium",
    "terraza",
    "espaciodeplaza",
    "juegos",
    "juegosparachicos",
    "salóndefiestas"
]
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
df_barrios = pd.read_csv(
    RELAT_PATH_TO_BARRIOS,
    sep=",",
    usecols=["BARRIO","GEOJSON"]
)
df_squares = pd.read_csv(
        RELAT_PATH_TO_SQUARE,
        sep=",",
        usecols=["COD_EV_PL","NOMBRE","GEOJSON"]
    )
df_squares = df_squares.astype({"NOMBRE": str})
df_malls = pd.read_csv(
        RELAT_PATH_TO_MALLS,
        sep=",",
        usecols=["NOMBRE","GEOJSON"]
    )
L_CONDOS = ["CONDOMINIO","CONDOS","CONDOMINIOS"]
L_PILETAS = ["PISCINA","PISCINAS","PILETA","PILETAS"]
L_VISTA_AL_RIO = ["VISTA AL RIO","VISTA AL RÍO","VISTA PARCIAL DEL RIO"]

class ArgenpropSpider(scrapy.Spider):
    name = "argenprop_spider"
    allowed_domains = ["www.argenprop.com"]
    start_urls = ["https://www.argenprop.com/departamentos/venta/rosario-santa-fe?solo-ver-dolares"]
    pages_to_scrape = 1 # 30

    def parse(self, response):
        estates = response.css('div.listing__item')

        for estate in estates:
            price = estate.css('.card__monetary-values .card__price ::text').getall()

            if "Consultar precio" in price[1]:
                continue

            relative_estate = estate.css('a').attrib['href']

            if relative_estate is not None:
                real_estate_url = 'https://www.argenprop.com' + relative_estate
                yield response.follow(real_estate_url, callback=self.parse_real_estate_page)

        if self.pages_to_scrape != 0:
            # amount_pages = int(response.css('li.pagination__page a::text').getall()[-1])
            # random_page = f"/departamentos/venta/rosario-santa-fe?pagina-{sample(range(amount_pages), 1)[0]}&solo-ver-dolares"
            next_page = response.css('li.pagination__page-next.pagination__page a::attr(href)').get()
            next_page_url = 'https://www.argenprop.com' + next_page
            self.pages_to_scrape -=1
            yield response.follow(next_page_url, callback=self.parse, dont_filter = True)

    def clean_sections(self, section_resp):
        properties = {}
        for item in section_resp:
            try:
                title = item.css("li p::text").get().replace(" ", "").split("\n")[1].replace(":","")
            except:
                title = None
            try:
                charac = item.css("li p strong::text").get().replace(" ", "").split("\n")[1]
            except:
                charac = None
            properties[title] = charac
        return properties

    def parse_description(self, descriptions):
        descript = []
        for desc in [d.get() for d in descriptions]:
            if "\n" in desc:
                desc = desc.split("\n")[1].strip()
            if desc=="":
                continue
            descript.append(desc)
        return descript

    def which_barrio(self, coord_real_estate):
        point = Point(coord_real_estate[1], coord_real_estate[0])
        for _, row in df_barrios.iterrows():
            l_lons_vect = []
            l_lats_vect = []
            for coords in literal_eval(row["GEOJSON"]).get("geometry").get("coordinates"):
                for coord in coords:
                    l_lons_vect.append(coord[0])
                    l_lats_vect.append(coord[1])
            lons_vect = np.array(l_lons_vect)
            lats_vect = np.array(l_lats_vect)
            polygon = Polygon(np.column_stack((lons_vect, lats_vect))) # create polygon
            if polygon.contains(point) or point.within(polygon):
                barrio = row["BARRIO"]
                break
            else: barrio = None
        return barrio

    def front_of_square(self, coord_real_estate):
        point = Point(coord_real_estate[1], coord_real_estate[0])
        for _, row in df_squares.iterrows():
            l_lons_vect = []
            l_lats_vect = []
            for coords in literal_eval(row["GEOJSON"]).get("geometry").get("coordinates"):
                for coord in coords:
                    l_lons_vect.append(coord[0])
                    l_lats_vect.append(coord[1])
            lons_vect = np.array(l_lons_vect)
            lats_vect = np.array(l_lats_vect)
            polygon = Polygon(np.column_stack((lons_vect, lats_vect)))
            if polygon.exterior.distance(point) <= 0.0005:
                plaza = 1
                break
            else: plaza = 0
        return plaza

    def get_metres_between_nearest_malls(self, coord_real_estate):
        dist = {
            "obj": [],
            "distance_in_km": [],
            "minimun": []    
        }
        nearest_of_real_estate = {
            "obj": None,
            "distance_in_km": None
        }
        for _, row in df_malls.iterrows():
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
        return round(nearest_of_real_estate["distance_in_km"]*1000, 2)

    def replace_accent(self, address_to_parse):
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

    def parse_street(self, street):
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
        if "CONDOS REFINERIA" in street:
            street = "VELEZ SARSFIELD"
        if "RODRIGUEZ" in street:
            street = "MARTIN RODRIGUEZ"
        if "QUINQUELA PLAZA" in street:
            street = "DEL HUERTO"
        if "MSR PUERTO NORTE" in street:
            street = "CARBALLO"
        if "ESPANA" in street:
            street = "ESPAÑA"
        if "THEDY" in street:
            street = "THEDY"
        if "WHEEELWRIGHT" in street:
            street = "WHEELWRIGHT"
        if "SANTA CRUZ" in street:
            street = "SANTA CRUZ"
        if "COSTAVIA" in street:
            street = "RIVADAVIA"
        return street

    def get_street_type(self, address):
        calle = self.parse_street(self.replace_accent(address.upper())).strip().split(" ")
        if calle.__len__() == 1:
            df = df_calles[
                (df_calles["NOMBRE"].str.strip() == calle[0]) |
                (df_calles["NOMBRE_ABREV"].str.strip() == calle[0])
            ]
            if not df.empty:
                street_type = 1 if df["TIPO"].item().strip() != "C" else 0
            else:
                df = df_calles[
                    df_calles["NOMBRE"].str.contains(fr"\s{calle[0]}\s") |
                    df_calles["NOMBRE_ABREV"].str.contains(fr"\s{calle[0]}\s")
                ]
                if not df.empty:
                    street_type = 1 if df["TIPO"].item().strip() != "C" else 0
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
                street_type = 1 if df["TIPO"].item().strip() != "C" else 0
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
                    street_type = 1 if df["TIPO"].item().strip() != "C" else 0
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
                street_type = 1 if df["TIPO"].item().strip() != "C" else 0
            else:
                street_type = "LEN Greater 3 - STREET NOT FOUND"
        return street_type, calle

    def parse_real_estate_page(self, response):
        address = response.css("div.location-container h2::text").get()
        if address is not None:
            avenida, calle_cleaning = self.get_street_type(address)
            # if "LEN" not in calle_cleaning:
            zone_location = response.css("div.location-container p::text").get()
            section_caracteristicas = response.xpath("//ul[@id='section-caracteristicas']/li")
            section_superficies = response.xpath("//ul[@id='section-superficie']/li")
            section_inst_edif = response.xpath("//ul[@id='section-instalaciones-edificio']/li")

            characteristics = self.clean_sections(section_resp=section_caracteristicas)
            superficies = self.clean_sections(section_resp=section_superficies)
            instalaciones = [item.css("li ::text").get().replace(" ","").split("\n")[1].lower() for item in section_inst_edif]

            description = " ".join(self.parse_description(descriptions=response.xpath('//div[@class="section-description--content"]/text()'))).upper()
            amenities = 1 if len(instalaciones)>0 and (elem in AMENITIES for elem in instalaciones) else 0

            pileta = 1 if any(w in instalaciones for w in L_PILETAS) else 0
            pileta = (1 if any(w in description for w in L_PILETAS) else 0) if pileta != 0 else pileta
            acceso_condominio = condominio = 1 if any(w in description for w in L_CONDOS) else 0
            parque = vista_rio = 1 if any(w in description for w in L_VISTA_AL_RIO) else 0

            coord = [response.xpath("//div[@class='map-container']/div/@data-latitude").get().replace(",","."),response.xpath("//div[@class='map-container']/div/@data-longitude").get().replace(",",".")]
            plaza = self.front_of_square(coord_real_estate=coord)
            paseo_comercial = self.get_metres_between_nearest_malls(coord_real_estate=coord)
            barrio = zone_location.split(",")[0]
            if barrio == "Rosario":
                barrio = self.which_barrio(coord_real_estate=coord)#.capitalize()

            yield {
                "url"               : response.request.url,
                "price"             : response.css("div.titlebar p::text").get().replace(" ","").split("\n")[1].split("USD")[1], # precio x m^2
                "acceso_condominio" : acceso_condominio, # DUMMY
                "condominio"        : condominio, # DUMMY
                "avenida"           : avenida, # Dummy - incl. av y bv
                "vista_rio"         : vista_rio,
                "parque"            : parque, # DUMMY
                "plaza"             : plaza, # DUMMY
                "paseo_comercial"   : paseo_comercial, # Metros
                "barrio"            : barrio, # TODO: source barrios vecinales, dummy por cada barrio que aparezca (a definir)
                "dormitorios"       : int(characteristics["Cant.Dormitorios"]) if "Cant.Dormitorios" in characteristics else 0,
                "baños"             : int(characteristics["Cant.Baños"]) if "Cant.Baños" in characteristics else 0,
                "cocheras"          : int(characteristics["Cant.Cocheras"]) if "Cant.Cocheras" in characteristics else 0,
                "superficie_total"  : float(superficies["Sup.Cubierta"].split("m2")[0].replace(",",".")) if "Sup.Cubierta" in superficies else 0.00 + (float(superficies["Sup.Descubierta"].split("m2")[0].replace(",",".")) if "Sup.Descubierta" in superficies else 0.00),
                "pileta"            : pileta,
                "amenities"         : (1 if "AMENITIES" in description else 0) if not amenities else amenities,
                "address"           : address,
                "calle_cleaning"    : calle_cleaning,
                "real_estate_coords": coord,
                "description"       : description
            }

