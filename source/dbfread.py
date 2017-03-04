from dbfread import DBF
import os

os.chdir('C:/Users/Souvik/OneDrive/Python/nsedata/data/currderivs/testdbf')

columns = {}
data = []
header = ''

key_count = 0
for rec in DBF('CD_NSE_FO011110.dbf'):
   """ rec_data = []
    for entry in rec:
        if entry[0] not in columns.keys():
            columns[entry[0]] = key_count
            key_count += 1
            header = header + entry[0] + ','
        rec_data.append(entry[1])"""
   print(rec)

