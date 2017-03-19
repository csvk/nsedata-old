"""
Created on Feb 21, 2017
@author: Souvik
@Program Function: Date utility functions


"""

from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import calendar

#adhoc_dates = [] # Can be initiated with dates in YYYY-MM-DD format
yesterday = (date.today() - relativedelta(days=1)).strftime('%Y-%m-%d')
all_days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

def dates(start='2008-06-01', end=yesterday, days=all_days):
    """Return all dates between start and end"""

    dates = []

    curr_date = (datetime.strptime(start, '%Y-%m-%d') - relativedelta(days=1)).strftime('%Y-%m-%d')
    while curr_date < end:
        curr_date_strp = datetime.strptime(curr_date, '%Y-%m-%d') + relativedelta(days=1)
        curr_date = curr_date_strp.strftime('%Y-%m-%d')
        if calendar.day_name[curr_date_strp.weekday()] in days:
            dates.append(curr_date)

    #dates.append(curr_date)

    return dates

# Below functions take YYYY-MM-DD as input date format
def ddmmyy(date):
    return '{}{}{}'.format(date[8:10],date[5:7],date[2:4])

def mm_int(date):
    """
    :param date:
    :return: Month in integer format
    """
    return int(date[5:7])

def ddmmyyyy(date):
    return '{}{}{}'.format(date[8:10],date[5:7],date[0:4])

def ddMMMyyyy(date):
    return '{}{}{}'.format(date[8:10],MMM(date),date[0:4])


def yyyy(date):
    return '{}'.format(date[0:4])


def MMM(date):
    return months(date[5:7], 'MMM')

def weekday(date):
    return datetime.strptime(date, '%Y-%m-%d').weekday()

def dayofweek(date):
    return calendar.day_name[weekday(date)]

def relativedate(date, years=0, months=0, days=0):
    return (datetime.strptime(date, '%Y-%m-%d')
            + relativedelta(days=days, months=months, years=years)).strftime('%Y-%m-%d')

def setdate(date, year=0, month=0, day=0):

    strpdate = datetime.strptime(date, '%Y-%m-%d')

    if year > 0:
        strpdate = strpdate.replace(year=year)
    if month > 0:
        strpdate = strpdate.replace(month=month)
    if day > 0:
        strpdate = strpdate.replace(day=day)

    return strpdate.strftime('%Y-%m-%d')

def datediff(date1, date2):
    return (datetime.strptime(date1, '%Y-%m-%d') - datetime.strptime(date2, '%Y-%m-%d')).days

# Below functions take input as DDMMYY as input date format

def ddmmyy_to_yyyy_mm_dd(date): # Can handle dates years from 1961 to 2060
    return '{}{}-{}-{}'.format('19' if date[4:6] > '60' else '20', date[4:6], date[2:4], date[0:2])

# Below functions take input as DDMMMYY as input date format

def ddMMMyyyy_to_yyyy_mm_dd(date):
    return '{}-{}-{}'.format(date[5:9], mm(date[2:5]), date[0:2])

# Below functions take input as DD-MMM-YY as input date format

def dd_MMM_yyyy_to_yyyy_mm_dd(date):
    return '{}-{}-{}'.format(date[7:11], mm(date[3:6]), date[0:2])

def ddmmyyyy_to_yyyy_mm_dd(date):
    return '{}-{}-{}'.format(date[4:8], date[2:4], date[0:2])

# Below functions take Month name as input: full name of first three chars

def mm(month):
    """Return month in MM format"""

    months = {'JAN': '01',
              'FEB': '02',
              'MAR': '03',
              'APR': '04',
              'MAY': '05',
              'JUN': '06',
              'JUL': '07',
              'AUG': '08',
              'SEP': '09',
              'OCT': '10',
              'NOV': '11',
              'DEC': '12',
              'JANUARY': '01',
              'FEBRUARY': '02',
              'MARCH': '03',
              'APRIL': '04',
              'JUNE': '06',
              'JULY': '07',
              'AUGUST': '08',
              'SEPTEMBER': '09',
              'OCTOBER': '10',
              'NOVEMBER': '11',
              'DECEMBER': '12'
              }

    month = month.upper()

    if  month in months:
        return months[month]
    else:
        return None


# Accepts month in numeric format of numeric in text format
def months(month, format='x'):
    """Return full month name"""

    month = int(month)
    if month < 0 or month > 12:
        return None
    month = str(month)

    months = {'01': 'January',
              '02': 'February',
              '03': 'March',
              '04': 'April',
              '05': 'May',
              '06': 'June',
              '07': 'July',
              '08': 'August',
              '09': 'September',
              '10': 'October',
              '11': 'November',
              '12': 'December',
              '1': 'January',
              '2': 'February',
              '3': 'March',
              '4': 'April',
              '5': 'May',
              '6': 'June',
              '7': 'July',
              '8': 'August',
              '9': 'September'
              }

    if format == 'x':
        return_val = months[month]
    elif format == 'Mmm':
        return_val = months[month][0:3]
    elif format == 'MMM':
        return_val = months[month][0:3].upper()
    elif format == 'mmm':
        return_val = months[month][0:3].lower()
    else:
        return_val = months[month]

    return return_val


adhoc_dates = [
'2008-09-03',
'2008-10-02',
'2008-10-09',
'2008-10-30',
'2008-11-13',
'2008-11-27',
'2008-12-09',
'2008-12-25',
'2009-01-08',
'2009-01-26',
'2009-02-23',
'2009-03-10',
'2009-03-11',
'2009-03-27',
'2009-04-01',
'2009-04-03',
'2009-04-07',
'2009-04-10',
'2009-04-14',
'2009-04-30',
'2009-05-01',
'2009-08-19',
'2009-09-21',
'2009-09-28',
'2009-09-30',
'2009-10-02',
'2009-10-13',
'2009-10-19',
'2009-11-02',
'2009-12-25',
'2009-12-28',
'2010-01-26',
'2010-02-12',
'2010-03-01',
'2010-03-16',
'2010-03-24',
'2010-04-01',
'2010-04-02',
'2010-04-14',
'2010-05-27',
'2010-08-19',
'2010-09-10',
'2010-09-30',
'2010-11-17',
'2010-12-17',
'2011-01-26',
'2011-02-16',
'2011-03-02',
'2011-04-01',
'2011-04-04',
'2011-04-12',
'2011-04-14',
'2011-04-22',
'2011-05-17',
'2011-08-15',
'2011-08-19',
'2011-08-31',
'2011-09-01',
'2011-09-30',
'2011-10-06',
'2011-10-27',
'2011-11-07',
'2011-11-10',
'2011-12-06',
'2012-01-26',
'2012-02-16',
'2012-02-20',
'2012-03-08',
'2012-03-23',
'2012-04-02',
'2012-04-05',
'2012-04-06',
'2012-05-01',
'2012-08-15',
'2012-08-20',
'2012-09-19',
'2012-10-02',
'2012-10-24',
'2012-10-26',
'2012-11-14',
'2012-11-28',
'2012-12-25',
'2013-01-25',
'2013-02-19',
'2013-03-27',
'2013-03-29',
'2013-04-01',
'2013-04-11',
'2013-04-19',
'2013-04-24',
'2013-05-01',
'2013-08-09',
'2013-08-15',
'2013-09-09',
'2013-10-02',
'2013-10-16',
'2013-11-04',
'2013-11-15',
'2013-12-25',
'2014-01-14',
'2014-02-19',
'2014-02-27',
'2014-03-17',
'2014-03-31',
'2014-04-01',
'2014-04-08',
'2014-04-14',
'2014-04-18',
'2014-04-24',
'2014-05-01',
'2014-05-14',
'2014-07-29',
'2014-08-15',
'2014-08-18',
'2014-08-29',
'2014-10-02',
'2014-10-03',
'2014-10-06',
'2014-10-15',
'2014-10-24',
'2014-11-04',
'2014-11-06',
'2014-12-25',
'2015-01-26',
'2015-02-17',
'2015-02-19',
'2015-03-06',
'2015-04-01',
'2015-04-02',
'2015-04-03',
'2015-04-14',
'2015-05-01',
'2015-05-04',
'2015-08-18',
'2015-09-17',
'2015-09-25',
'2015-10-02',
'2015-10-22',
'2015-11-12',
'2015-11-25',
'2015-12-24',
'2015-12-25',
'2016-01-26',
'2016-02-19',
'2016-03-07',
'2016-03-24',
'2016-03-25',
'2016-04-01',
'2016-04-08',
'2016-04-14',
'2016-04-15',
'2016-04-19',
'2016-07-06',
'2016-08-15',
'2016-08-17',
'2016-09-05',
'2016-09-13',
'2016-10-11',
'2016-10-12',
'2016-10-31',
'2016-11-14',
'2016-12-12',
'2017-01-26',
'2017-02-21',
'2017-02-24'
]


