"""
Created on Feb 28, 2017
@author: Souvik
@Program Function: Download NSE Bhavcopy

"""
import os
import dates
import currderivs, eqderivs

ROOT = 'C:/Users/Souvik/OneDrive/Python/nsedata/'
PATH = 'data/currderivs/csv files/'


os.chdir(ROOT)

#### Steps Start for Currderivs download

# print('Initiating NSE Currency derivatives bhavcopy download')
# date_range = dates.dates('2011-12-03')
# date_range = dates.adhoc_dates
# currderivs.get_bhavcopy(date_range)
# currderivs.dbf_to_csv()

#### Steps End for Currderivs download

#### Steps Start for Currderivs edit
#os.chdir(PATH)
#currderivs.clean_csv()
#os.chdir('cleaned/')
#currderivs.format_csv_futures('Symbol', 'Date', 'OPEN_PRICE', 'HIGH_PRICE', 'LOW_PRICE', 'CLOSE_PRIC', 'TRD_NO_CON',
#                              'OI_NO_CON', 'Expiry')
#os.chdir('formatted/')
#currderivs.ren_csv_files()

### Steps End for Currderivs edit

os.chdir(PATH + 'cleaned/formatted/')
#os.chdir(PATH + 'test/')
#currderivs.continuous_contracts(1)
#currderivs.write_expiries(EXPIRIES) # Use this function to refresh the expiry list







# print('Initiating NSE Equity derivatives bhavcopy download')
# date_range.reverse()
# eqderivs.get_bhavcopy(date_range)

