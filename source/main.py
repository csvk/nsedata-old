"""
Created on Feb 28, 2017
@author: Souvik
@Program Function: Download NSE Bhavcopy

"""

import dates, os
import currderivs

root = 'C:/Users/Souvik/OneDrive/Python/nsedata'
os.chdir(root)

date_range = dates.dates('2008-06-01')
currderivs.get_bhavcopy(date_range)



