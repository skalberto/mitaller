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
    if cType in ['N']: 
       if sAux == u'\xa0':
          sAux = sAux.replace(u'\xa0',u'0')  
       return (True,int(sAux)) # Ahora dato numerico

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
    tRet = Clear_Data(sLine,'N') # sesLine espera dato tipo Numeric
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
        'C' : aContagiados[:216], # Contagiados
        'M' : aMuertos[:216],     # Muertos
        'F' : aConfirmados[:216]  # Confirmados
       } 

# DataFrame que resume y ordena de manera matricial
# toda la informacion anterior
#---------------------------------------------------
df = pd.DataFrame(dData,columns = ['P','C','F','M'],index = range(len(aPais)))
df.index.names = ['#'] # indice del pais.  

# Exportar datos DataFrame a Archivo CSV.003d
#---------------------------------------------------
sFile = 'data_export.csv'

df.to_csv(sFile)

#---------------------------------------------------
# Salida de los 10 primeros data
#---------------------------------------------------
df.head(10)
#---------------------------------------------------
'''
#                         P       C      F     M
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
                     C              F              M
count       216.000000     216.000000     216.000000
mean     572392.833333   30023.722222   12601.347222
std     2402869.898151  102405.744804   48007.153135
min           0.000000       0.000000       0.000000
25%        3910.500000     146.250000      55.000000
50%       39649.000000    1784.500000     605.000000
75%      250234.750000   13140.000000    4566.000000
max    29819108.000000  995861.000000  542359.000000
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
                     'Contagiados': aContagiados[:216]
                    })
#----------------------------------------------------                    
# Graficamos el DataFrame
# G = Info.plot(x = 'Pais', y = 'Contagiados',rot = 90 )
#-----------------------------------------------------
plt.plot(range(len(aPais)),aContagiados[:216])
plt.xlabel('Paises') ; plt.ylabel('Contagiados')
plt.title('Paises Contagiados COVID Semana 9-10 2020')
plt.grid(True)
plt.xlim([0,230])
plt.savefig('conta.png')
plt.show()

# Graficos de Confirmados de COVID por pais
# Al hacer ZOOM en Tools se detallan los paises
#---------------------------------------------------
Info = pd.DataFrame(
                    {
                     'Pais' : aPais,
                     'Confirmados': aConfirmados[:216]
                    })
#----------------------------------------------------                    
# Graficamos el DataFrame
# G = Info.plot(x = 'Pais', y = 'Contagiados',rot = 90 )
#-----------------------------------------------------
plt.plot(range(len(aPais)),aConfirmados[:216])
plt.xlabel('Paises') ; plt.ylabel('Confirmados')
plt.title('Paises Confirmados COVID Semana 9-10 2020')
plt.grid(True)
plt.xlim([0,230])
plt.savefig('confir.png')
plt.show()

# Graficos de Muertos de COVID por pais
# Al hacer ZOOM en Tools se detallan los paises
#---------------------------------------------------
Info = pd.DataFrame(
                    {
                     'Pais' : aPais,
                     'Muertos': aMuertos[:216]
                    })
#----------------------------------------------------                    
# Graficamos el DataFrame
# G = Info.plot(x = 'Pais', y = 'Contagiados',rot = 90 )
#-----------------------------------------------------
plt.plot(range(len(aPais)),aMuertos[:216])
plt.xlabel('Paises') ; plt.ylabel('Muertos')
plt.title('Paises Muertos CODIV Semana 9-10 2020')
plt.grid(True)
plt.xlim([0,230])
plt.savefig('muertos.png')
plt.show()
