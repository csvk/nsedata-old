"""
Created on Feb 28, 2017
@author: Souvik
@Program Function: Download NSE Bhavcopy

"""

import dates, os
import currderivs, eqderivs

root = 'C:/Users/Souvik/OneDrive/Python/nsedata'
os.chdir(root)

print('Initiating NSE Currency derivatives bhavcopy download')
date_range = dates.dates('2010-10-24', '2010-11-05')
currderivs.get_bhavcopy(date_range)

# print('Initiating NSE Equity derivatives bhavcopy download')
# date_range.reverse()
# eqderivs.get_bhavcopy(date_range)

