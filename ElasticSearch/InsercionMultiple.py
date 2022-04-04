import requests, utm, requests
from requests.sessions import extract_cookies_to_jar
import pandas as pd
from xml.etree import ElementTree
from datetime import datetime
from unidecode import unidecode

url ="https://practica7.es.francecentral.azure.elastic-cloud.com:9243/"
username = "admin"
password = "adminkibana"
index = "trafico-madrid"
headers = {"Content-type": "application/json"}

nums = ["idelem","accesoAsociado","intensidad","ocupacion","carga","nivelServicio","intensidadSat","subarea","velocidad"]
response=requests.get("https://informo.madrid.es/informo/tmadrid/pm.xml")
root = ElementTree.fromstring(response.content)

fecha=root[0].text
print(fecha)

data = ""
for pm in root[1:-1]:
    d={}
    coordenadas=[0,0]
    for i in pm:
        if i.tag in nums:
            try:
                d[i.tag]=int(i.text)
            except:
                pass
        elif i.tag == "st_x":
            coordenadas[0]=float(i.text.replace(",","."))
        elif i.tag == "st_y":
            coordenadas[1]=float(i.text.replace(",","."))
        else:
            d[i.tag]=unidecode(i.text.replace("Ø","n.").replace("´","").replace("'",""))
    d["fecha_hora"] = str(datetime.strptime(fecha, "%d/%m/%Y %H:%M:%S"))
    coordenadas = utm.to_latlon(coordenadas[0],coordenadas[1],30,"T")
    d["coordenadas"] = {"lat":coordenadas[0],"lon":coordenadas[1]}
    data =data + """{"index": {"_index": "trafico-madrid"}}"""+"\n"+str(d)+"\n"
print(data)
ndjson = data.replace("'","\"")
response = requests.post(url+index+"/_doc/_bulk", data=ndjson, headers=headers, auth=(username,password))
print(response.json())
