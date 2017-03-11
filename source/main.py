"""
Created on Feb 28, 2017
@author: Souvik
@Program Function: Download NSE Bhavcopy

"""
import os
import dates
import currderivs, eqderivs

root = 'C:/Users/Souvik/OneDrive/Python/nsedata/'
os.chdir(root)

# print('Initiating NSE Currency derivatives bhavcopy download')
# date_range = dates.dates('2011-12-03')
# date_range = dates.adhoc_dates
# currderivs.get_bhavcopy(date_range)
# currderivs.dbf_to_csv()

# currderivs.clean_csv()

#currderivs.format_csv_futures('data/currderivs/csv/cleaned/',
#                              'Symbol', 'Date', 'OPEN_PRICE', 'HIGH_PRICE', 'LOW_PRICE', 'CLOSE_PRIC', 'TRD_NO_CON',
#                              'OI_NO_CON', 'Expiry')

#currderivs.format_csv_futures('data/currderivs/csv/uncleaned/',
#                              'CONTRACT_D', 'Date', 'OPEN_PRICE', 'HIGH_PRICE', 'LOW_PRICE', 'CLOSE_PRIC', 'TRD_NO_CON',
#                              'OI_NO_CON', 'Expiry')

currderivs.ren_csv_files('data/currderivs/csv/cleaned/formatted/')

# print('Initiating NSE Equity derivatives bhavcopy download')
# date_range.reverse()
# eqderivs.get_bhavcopy(date_range)

