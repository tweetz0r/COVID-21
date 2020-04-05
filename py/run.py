__author__ = "Florian Thiery"
__copyright__ = "MIT Licence 2020, Florian Thiery, Research Squirrel Engineers"
__credits__ = ["Florian Thiery"]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Florian Thiery"
__email__ = "rse@fthiery.de"
__status__ = "draft"

import json
import requests
import uuid
import pandas as pd
import os
import codecs
import datetime
import hashlib

dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path.replace("\\py","\\ttl"))
file_out = dir_path.replace("\\py","\\ttl") + "\\" + "covid19.ttl"

responseJHU = requests.get("https://pomber.github.io/covid19/timeseries.json")
dataJHU = responseJHU.json()

responseECDC = requests.get("https://opendata.ecdc.europa.eu/covid19/casedistribution/json/")
dataECDC = responseECDC.json()['records']

#responseRKI = requests.get("https://opendata.arcgis.com/datasets/dd4580c810204019a7b8eb3e0b329dd6_0.geojson")
#dataRKI = responseRKI.json()['features']
#print(len(dataRKI))

countriesJHU = []
for item in dataJHU:
    countriesJHU.append(str(item))

lines = []

for c in countriesJHU:
    cstring = str(c)
    thiscountry = dataJHU[c]
    for item in thiscountry:
        m = hashlib.md5()
        m.update(cstring + str(item['date']) + "JHU")
        UUID = str(int(m.hexdigest(), 16))[0:16]
        lines.append("covid19:" + UUID + " " + "rdf:type" + " covid19:JHU_Dataset .")
        lines.append("covid19:" + UUID + " " + "covid19:country" + " world:" + str(cstring).replace(" ","_").replace("(","").replace(")","").replace("'","").replace("*","").replace(",","") + " .")
        lines.append("covid19:" + UUID + " " + "covid19:date" + " " + "'" + str(item['date']) + "'" + ".")
        lines.append("covid19:" + UUID + " " + "covid19:confirmed" + " " + "'" + str(item['confirmed']) + "'" + ".")
        lines.append("covid19:" + UUID + " " + "covid19:deaths" + " " + "'" + str(item['deaths']) + "'" + ".")
        lines.append("covid19:" + UUID + " " + "covid19:recovered" + " " + "'" + str(item['recovered']) + "'" + ".")
        lines.append("")

for item in dataECDC:
    cstr = item['countriesAndTerritories']
    dstr = item['dateRep']
    castr = item['cases']
    destr = item['deaths']
    ccode = item['countryterritoryCode']
    m = hashlib.md5()
    m.update(ccode + dstr + "ECDC")
    UUID = str(int(m.hexdigest(), 16))[0:16]
    lines.append("covid19:" + UUID + " " + "rdf:type" + " covid19:ECDC_Dataset .")
    lines.append("covid19:" + UUID + " " + "covid19:country" + " world:" + cstr.replace(" ","_").replace("(","").replace(")","").replace("'","").replace("*","").replace(",","") + " .")
    lines.append("covid19:" + UUID + " " + "covid19:date" + " " + "'" + dstr + "'" + ".")
    lines.append("covid19:" + UUID + " " + "covid19:confirmed" + " " + "'" + castr + "'" + ".")
    lines.append("covid19:" + UUID + " " + "covid19:deaths" + " " + "'" + destr + "'" + ".")
    lines.append("")

file = codecs.open(file_out, "w", "utf-8")
file.write("# create triples from JHU and ECDC" + "\r\n")
file.write("# on " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + "\r\n\r\n")
prefixes = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> \r\nPREFIX owl: <http://www.w3.org/2002/07/owl#> \r\nPREFIX xsd: <http://www.w3.org/2001/XMLSchema#> \r\nPREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> \r\nPREFIX dc: <http://purl.org/dc/elements/1.1/> \r\nPREFIX covid19: <http://covid19.squirrel.link/ontology#> \r\nPREFIX world: <http://world.squirrel.link/ontology#> \r\n\r\n";
file.write(prefixes)
file.write("covid19:COVID19_Data rdf:type rdfs:Resource .\r\n")
file.write("covid19:COVID19_Data rdf:type covid19:Dataset .\r\n")
file.write("covid19:COVID19_Data dc:created '2020-04-05T10:53:21.259+0100' .\r\n")
file.write("covid19:COVID19_Data dc:modified '" + datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000+0100") + "' .\r\n")
file.write("covid19:COVID19_Data dc:creator 'Florian Thiery' .\r\n")
file.write("covid19:COVID19_Data dc:contributor 'Timo Homburg' .\r\n")
file.write("covid19:COVID19_Data dc:language 'en' .\r\n")
file.write("covid19:COVID19_Data dc:type 'ontology' .\r\n")
file.write("covid19:COVID19_Data dc:title 'COVID-19 data by JHU and ECDC' .\r\n")
file.write("covid19:COVID19_Data dc:subject 'COVID-19' .\r\n")
file.write("covid19:COVID19_Data dc:rights 'CC BY 4.0' .\r\n\r\n")
for line in lines:
    file.write(line)
    file.write("\r\n")
file.close()
