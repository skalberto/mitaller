# --------------------------------------------------
from bs4 import BeautifulSoup as BFS
import requests as RQ, pandas as pd
import urllib2 as UL2, numpy as np

# --------------------------------------------------
# Data Set COVID-19 de www.ecdc.europa.eu
# European Centre for Disease Prevention and Control
# By Alberto Caro S.
# --------------------------------------------------

# Arreglos Globales de datos relevantes infectados
# --------------------------------------------------
aLinks = []

def Save_Data(sURL,nType):
    dDFiles = {
               '1': 'csv',
               '2': 'xlsx',
               '3': 'json',
               '4': 'xml'
              }
    nFileHD = UL2.urlopen(sURL)
    aStream = nFileHD.read()

    # Verificamos la extension del archivo a bajar
    #-----------------------------------------------
    # CSV ?
    
    if nType == 1:
       with open('./data.' + dDFiles['1'],'wb') as F:
        F.write(aStream); F.close()
    if nType == 2:
       with open('./data.' + dDFiles['2'],'wb') as F:
        F.write(aStream); F.close()
    if nType == 3:
       with open('./data.' + dDFiles['3'],'wb') as F:
        F.write(aStream); F.close()
    if nType == 4:
       with open('./data.' + dDFiles['4'],'wb') as F:
        F.write(aStream); F.close()
    return
    
# URL donde se encuentran otros dataset de interes
#---------------------------------------------------

URL = 'https://www.ecdc.europa.eu/en/publications-data/data-covid-19-vaccination-eu-eea'

# Realizamos una peticion get al Servidor
#---------------------------------------------------
Res = RQ.get(URL)

# Parseamos el contenido devuelto en Res
# En web_info esta todo el contenido html del URL
#---------------------------------------------------
web_info = BFS(Res.content,'html.parser')

# El tag 'class_= 'btn btn-primary' es donde se encuentran
# los datos. Esto se descubrio analizando la pagina consultada
# mediante el Inspector del navegador Chrome
#---------------------------------------------------

Info = web_info.find_all(class_= 'btn btn-primary')
    
# Recorrimos todas las entradas de Links y sacamos 
# la informacion de interes Se exportan los datos
# a archivos XLSX, CSV, JSON y XML
#---------------------------------------------------
for url in Info:
    aLinks.append(url['href'])
print(aLinks)

Save_Data(aLinks[2],1)
Save_Data(aLinks[1],2)
Save_Data(aLinks[3],3)
Save_Data(aLinks[4],4)

