"""
Created on Feb 28, 2017
@author: Souvik
@Program Function: Download NSE Bhavcopy

"""
import os
import dates
import currderivs as cd, eqderivs as ed

ROOT = 'C:/Users/Souvik/OneDrive/Python/nsedata/'
PATH = 'data/currderivs/fresh/'


os.chdir(ROOT)

#### Steps Start for Currderivs download

#print('Initiating NSE Currency derivatives bhavcopy download')
#date_range = dates.dates('2009-01-07')
#date_range = dates.adhoc_dates
#cd.get_bhavcopy(date_range)
#DBF_PATH = 'data/currderivs/fresh/dbftest/'
#CSV_PATH = 'data/currderivs/fresh/csvtest/'
#cd.dbf_to_csv(DBF_PATH, CSV_PATH)
#cd.dbf_to_csv()
#cd.csv_copy_with_bkp()

#### Steps End for Currderivs download

#### Steps Start for Currderivs edit
os.chdir(PATH + 'csv/')
#cd.clean_csv()
os.chdir('cleaned/')
#cd.format_csv_futures('Symbol', 'Date', 'OPEN_PRICE', 'HIGH_PRICE', 'LOW_PRICE', 'CLOSE_PRIC', 'TRD_NO_CON',
#                              'OI_NO_CON', 'Expiry')
os.chdir('formatted/test/')
#cd.ren_csv_files()

### Steps End for Currderivs edit

### Steps for creating continuous contract
#os.chdir(PATH + 'cleaned/formatted/')
cd.continuous_contracts_all([0,1,2])

### Steps end for continuous contract


# print('Initiating NSE Equity derivatives bhavcopy download')
# date_range.reverse()
# ed.get_bhavcopy(date_range)

