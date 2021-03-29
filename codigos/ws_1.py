# By Alberto Caro
# Librerias utilizadas
# Su instalacion en python
# --------------------------------------------------
# pip3 install bs4
# pip3 install requests
# pip3 install pandas
# pip3 install numpy
# pip3 install telepod
# --------------------------------------------------
from bs4 import BeautifulSoup as BFS
import requests as RQ, pandas as pd
import urllib2, numpy as np
import matplotlib.pyplot as plt
import telepot as Te, time as ti

# --------------------------------------------------
# Data Set COVID-19 de www.ecdc.europa.eu
# European Centre for Disease Prevention and Control
# By Alberto Caro S.
# --------------------------------------------------

# Arreglos Globales de datos relevantes infectados
# --------------------------------------------------
aPais        = [] # -> Pais de origen de personas infectadas
aContagiados = [] # -> Total de personas contagiadas por COVID
aMuertos     = [] # -> Total de personas muertas por COVID
aConfirmados = [] # -> Casos Confirmados de personas infectadas COVID
aPeriodo     = [] # -> Periodo ano 2021 semanas 9 y 10

# Funcion que limpia los datos cuando los valores
# utf-8 son mayores que el ordinal 128
# y los convierte a String o Numerico
# Se devuelve una Tupla(.)
#---------------------------------------------------
def Clear_Data( sEle, cType ):
    sTRUCO = 'BAD DATA'; sAux = sEle
    if cType in ['S']:
       if len(sAux) == 1: return (False,'')
       for i in range(len(sAux)):
           if ord(sAux[i]) > 128:
              sAux = sTRUCO    # Ahora String valido
       return (True,str(sAux)) # String no utf-8
    if cType in ['N']: return (True,int(sAux)) # Ahora dato numerico

    return (False,'')

# URL donde se encuentran los datos a obtener
#---------------------------------------------------
URL = 'https://www.ecdc.europa.eu/en/geographical-distribution-2019-ncov-cases'

# Realizamos una peticion get al Servidor
#---------------------------------------------------
Res = RQ.get(URL)

# Parseamos el contenido devuelto en Res
# En web_info esta todo el contenido html del URL
#---------------------------------------------------
web_info = BFS(Res.content,'html.parser')

# El tag 'tbody tr' es donde se encuentran los datos
# Esto se descubrio analizando la pagina consultada
# mediante el Inspector del navegador Chrome
#---------------------------------------------------
data = web_info.select('tbody tr')

# Recorrimos todas las entradas de data y sacamos la
# la informacion de interes
#---------------------------------------------------
for xEle in data:
    #Procesamos pais de procedencia
    sLine = xEle.select('td')[1].get_text()  
    tRet = Clear_Data(sLine,'S') # Se espera datos tipo String
    if tRet[0] : aPais.append(tRet[1]) 

    #Procesamos total contagiados
    sLine = xEle.select('td')[2].get_text() 
    tRet = Clear_Data(sLine,'N') # se espera dato tipo Numeric
    if tRet[0] : aContagiados.append(tRet[1]) 

    #Procesamos total muertos
    sLine = xEle.select('td')[3].get_text() 
    tRet = Clear_Data(sLine,'N') # se espera dato tipo Numeric
    if tRet[0] : aMuertos.append(tRet[1]) 
    
    #Procesamos total confirmados
    sLine = xEle.select('td')[4].get_text() 
    tRet = Clear_Data(sLine,'N') # se espera dato tipo Numeric
    if tRet[0] : aConfirmados.append(tRet[1]) 
        
    #Procesamos periodo del estudio
    sLine = xEle.select('td')[5].get_text()
    tRet = Clear_Data(sLine,'S') # se espera dato tipo String
    if tRet[0] : aPeriodo.append(tRet[1]) 

# Pasando los datos anteriores a un DataFrame Pandas
# Armamos el dataframe desde los arreglos anteriores
# Solo tomamos los primeros 215 datos. El dato en
# posicion 216 -> Registra los Totales de cada columna
#---------------------------------------------------
dData = {
        'P' : aPais,              # Pais
        'C' : aContagiados[:215], # Contagiados
        'M' : aMuertos[:215],     # Muertos
        'F' : aConfirmados[:215]  # Confirmados
       } 

# DataFrame que resume y ordena de manera matricial
# toda la informacion anterior
#---------------------------------------------------
df = pd.DataFrame(dData,columns = ['P','C','F','M'],index = range(len(aPais)))

# Exportar datos DataFrame a Archivo CSV.003d
#---------------------------------------------------
sFile = 'data_covid_10_19_2021.csv'

df.to_csv(sFile)

#---------------------------------------------------
# Salida de los 10 primeros data
#---------------------------------------------------
df.head(10)
#---------------------------------------------------
'''
                          P       C      F     M
0                   Algeria  124265  11173  3036
1                    Angola   21380    573   521
2                     Benin    6501    867    81
3                  Botswana   35009   6628   447
4              Burkina_Faso   12378    396   144
5                   Burundi    2461    252     3
6                  Cameroon   38988   3274   588
7                Cape_Verde   16101    701   156
8  Central_African_Republic    5025     28    63
9                      Chad    4309    336   154
----------------------------------------------------
'''

# Resumen estadistico dataframe contaminacion COVID
#---------------------------------------------------
df.describe()
#----------------------------------------------------
'''
count       215.000000     215.000000     215.000000
mean     559388.032558   27434.227907   12371.172093
std     2366985.265277   97332.612742   47135.416403
min           0.000000       0.000000       0.000000
25%        3884.000000     149.000000      59.000000
50%       38988.000000    1859.000000     622.000000
75%      244211.500000   11176.000000    4447.000000
max    29495422.000000  932608.000000  535661.000000
----------------------------------------------------
'''

# Graficamos los casos de Contaminados, Contagiados
# y Muertos de Africa, Europa, Asia, America y Otros
#---------------------------------------------------
plt.close('all')

# Graficos de Contagiados de COVID por pais
# Al hacer ZOOM en Tools se detallan los paises
#---------------------------------------------------
Info = pd.DataFrame(
                    {
                     'Pais' : aPais,
                     'Contagiados': aContagiados[:215]
                    })
G = Info.plot(x = 'Pais', y = 'Contagiados',rot = 90 )
plt.show()

# Graficos de Confirmados de COVID por pais
# Al hacer ZOOM en Tools se detallan los paises
#---------------------------------------------------
Info = pd.DataFrame(
                    {
                     'Pais' : aPais,
                     'Confirmados': aConfirmados[:215]
                    })
G = Info.plot(x = 'Pais', y = 'Confirmados',rot = 90 )
plt.show()

# Graficos de Muertos de COVID por pais
# Al hacer ZOOM en Tools se detallan los paises
#---------------------------------------------------
Info = pd.DataFrame(
                    {
                     'Pais' : aPais,
                     'Muertos': aMuertos[:215]
                    })
G = Info.plot(x = 'Pais', y = 'Muertos',rot = 90 )
plt.show()

