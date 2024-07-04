import re
import scrapy
from random import sample
from scrapy.http import HtmlResponse
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
import pandas as pd


# How many pages are for each domanins? (get into ramdonly)
# There is real estate agency:
#       - Argenprop --> por pag muestra 20 / (500) 30 paginas a consultar --> Scrapy

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
PATH_TO_FILE = "C:/Users/loria/Documents/github-projects/work-data_extracting/nomenclador_de_calles/Nomenclador de Calles.csv"
df_calles = pd.read_csv(
                PATH_TO_FILE,
                sep=",",
                usecols=["NOMBRE","TIPO","NOMBRE_ABREV"]
            )
# NO MATCH:
#   - Alvear
#   - Pellegrini
#   - Rodriguez
#   - Alem
#   - Oroño

class ArgenpropSpider(scrapy.Spider):
    name = "argenprop_spider"
    allowed_domains = ["www.argenprop.com"]
    start_urls = ["https://www.argenprop.com/departamentos/venta/rosario-santa-fe"]
    pages_to_scrape = 5 # 30

    def parse(self, response):
        estates = response.css('div.listing__item')
        # amount_pages = response.css('li.pagination__page a::text').getall()[-1]
        # sample(range(amount_pages), 9)

        for estate in estates:
            price = estate.css('.card__monetary-values .card__price ::text').getall()

            if "Consultar precio" in price[1]:
                continue

            relative_estate = estate.css('a').attrib['href']

            if relative_estate is not None:
                real_estate_url = 'https://www.argenprop.com' + relative_estate
                yield response.follow(real_estate_url, callback=self.parse_real_estate_page)

        if self.pages_to_scrape != 0:
            next_page = response.css('li.pagination__page-next.pagination__page a::attr(href)').get()
            next_page_url = 'https://www.argenprop.com' + next_page
            self.pages_to_scrape -=1
            yield response.follow(next_page_url, callback=self.parse)

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

    def replace_accent(self, address_to_parse):
        dict_letter = {
            "Á" : "A",
            "É" : "E",
            "Í" : "I",
            "Ó" : "O",
            "Ú" : "U",
            "Ü" : "U"
        }
        for elem in ["Á","É","Í","Ó","Ú","Ü"]:
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
        if "Torres Dolfines" in street:
            street = "ESTANISLAO LOPEZ"
        if "N°" in street:
            street = street.replace("N°", "").strip()
        return street

    def return_street_type(self, df, calle):
        df1 = df[df["NOMBRE_ABREV"].str.strip() == calle[0]]
        if df1.empty:
            if calle.__len__() >= 3:
                df2 = df[df["NOMBRE_ABREV"].str.contains(calle[0]) &
                        df["NOMBRE_ABREV"].str.contains(calle[1]) &
                        df["NOMBRE_ABREV"].str.contains(calle[2])]
                if df2.empty:
                    df = df[df["NOMBRE"].str.contains(calle[0]) &
                        df["NOMBRE"].str.contains(calle[1]) &
                        df["NOMBRE"].str.contains(calle[2])]
                else: street_type = "1" if df2["TIPO"].item().strip() == "C" else "0"
            elif calle.__len__() == 2:
                df2 = df[df["NOMBRE_ABREV"].str.contains(calle[0]) &
                        df["NOMBRE_ABREV"].str.contains(calle[1])]
                if df2.empty:
                    df = df[df["NOMBRE"].str.contains(calle[0]) &
                        df["NOMBRE"].str.contains(calle[1])]
                    if not df.empty:
                        street_type = "1" if df["TIPO"].item().strip() == "C" else "0"
                else: street_type = "1" if df2["TIPO"].item().strip() == "C" else "0"
            else: street_type = None
        else: street_type = "1" if df1["TIPO"].item().strip() == "C" else "0"
        return street_type

    def get_street_type(self, address):
        calle = self.replace_accent(self.parse_street(address.upper())).strip().split(" ")
        df = df_calles[
                df_calles["NOMBRE"].str.contains(calle[0]) | df_calles["NOMBRE_ABREV"].str.contains(calle[0])
            ]
        if calle.__len__() > 1:
            df = df_calles[
                (df_calles["NOMBRE"].str.contains(calle[-2]) & df_calles["NOMBRE"].str.contains(calle[-1])) |
                (df_calles["NOMBRE_ABREV"].str.contains(calle[-2]) & df_calles["NOMBRE_ABREV"].str.contains(calle[-1]))
            ]
        if not df.empty:
            street_type = self.return_street_type(df, calle)
        else:
            if calle.__len__() > 1:
                df = df_calles[
                    (df_calles["NOMBRE"].str.contains(calle[0]) & df_calles["NOMBRE"].str.contains(calle[1])) |
                    (df_calles["NOMBRE_ABREV"].str.contains(calle[0]) & df_calles["NOMBRE_ABREV"].str.contains(calle[1]))
                ]
            if not df.empty:
                street_type = self.return_street_type(df, calle)
            else:
                street_type = "STREET NOT FOUND"
        return calle, street_type

    def parse_real_estate_page(self, response):
        address = response.css("div.location-container h2::text").get()
        if address is not None:
            zone_location = response.css("div.location-container p::text").get()
            section_caracteristicas = response.xpath("//ul[@id='section-caracteristicas']/li")
            section_superficies = response.xpath("//ul[@id='section-superficie']/li")
            section_inst_edif = response.xpath("//ul[@id='section-instalaciones-edificio']/li")

            characteristics = self.clean_sections(section_resp=section_caracteristicas)
            superficies = self.clean_sections(section_resp=section_superficies)
            instalaciones = [item.css("li ::text").get().replace(" ","").split("\n")[1].lower() for item in section_inst_edif]
            acceso_calle = self.get_street_type(address)

            yield {
            ## Add data variable here for each real estate
                "price"             : response.css("div.titlebar p::text").get().replace(" ","").split("\n")[1],
                "address"           : address,
                "acceso_calle"      : acceso_calle, # DUMMY
                # "acceso_condominio" : acceso_condominio, # DUMMY
                # "condominio"        : condominio, # DUMMY
                "zone_location"     : zone_location,
                "barrio"            : zone_location.split(",")[0],
                "dormitorios"       : characteristics["Cant.Dormitorios"] if "Cant.Dormitorios" in characteristics else 0,
                "baños"             : characteristics["Cant.Baños"] if "Cant.Baños" in characteristics else 0,
                "cocheras"          : characteristics["Cant.Cocheras"] if "Cant.Cocheras" in characteristics else 0,
                "superficie_total"  : float(superficies["Sup.Cubierta"].split("m2")[0].replace(",",".")) if "Sup.Cubierta" in superficies else 0.00 + (float(superficies["Sup.Descubierta"].split("m2")[0].replace(",",".")) if "Sup.Descubierta" in superficies else 0.00),
                "piscina"           : 1 if "pileta" in instalaciones else 0,
                "amenities"         : 1 if len(instalaciones)>0 and (elem in AMENITIES for elem in instalaciones) else 0
            }


# TO SAVE RESULT DATA EXTRACTING:
#   scrapy crawl argenprop -O namefile.json
