import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests

MyWeb = requests.get('https://covid19.ncdc.gov.ng/').text
MyInf = BeautifulSoup(MyWeb,'lxml')
Table = MyInf.find('table',id='custom1')
MyRow = Table.thead.findAll('tr')

for nPos in range(len(MyRow)):
    MyHeads = MyRow[nPos].find_all('th')
    NameCol = [i.string.strip() for i in MyHeads]

Row_Data = Table.tbody.findAll('
')

aData = [] 
for nPos in range(len(Row_Data)):
    xAux = [i.string.strip() for i in Row_Data[nPos].find_all('td')]
    aData.append(xAux)
    
dD = dict(enumerate(aData))
df = pd.DataFrame(dD)
df = df.T
df.columns = NameCol
