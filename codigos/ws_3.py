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

# Envio de los graficos anteriores por Telegram a mi
# SmartPhone con la informacion de Contaminados COVID
#---------------------------------------------------

Bot = Te.Bot('12193XXXXX:AAHRFjMEYVKl_XXXXXXXXXXXXXXXX)
aGraf = ['contaminados.png','contagiados.png','muertos.png']
    
#-----------------------------------------------------
# Envio de Mensaje de Texto al Chat de mi Boe Telegram
#-----------------------------------------------------
# Cambiar por su propio Token y Chat ID
#-----------------------------------------------------
        
Bot.sendMessage(7955XXXXX,text='Envio Graficos COVID!')
for nPos in range(3):
 Img = open(aGraf[nPos],'rb')
 sLin = 'Grafico: %003d' %(nPos)   
 # Envio grafico COVID
 Bot.sendPhoto(7955XXXXX,Img,sLin)
 ti.sleep(3)
 Img.close()
Bot.sendMessage(7955XXXXX,text='Fin envio Graficos COVID!') 
    
#------------------------------------------------------------
# Envio Archivo CSV del DataFrame Anterior a mi Boe Telegram
#------------------------------------------------------------

sFile = 'data_covid_10_19_2021.csv'
Bot.sendDocument(7955XXXXX,document=open(sFile,'rb'))
    

