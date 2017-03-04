"""
Created on Feb 28, 2017
@author: Souvik
@Program Function: Download NSE Currency Derivatives Bhavcopy


"""

import requests, zipfile, os
import dates
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import traceback, logging

CHROME_DRIVER = 'C:\Program Files (x86)/chromedriver_win32/chromedriver.exe'
NEW_URL = 'https://www.nseindia.com/archives/fo/bhav/'
OLD_URL = 'https://www.nseindia.com/content/historical/DERIVATIVES/'
PATH = 'data/eqderivs/'
LOGFILE = 'log.csv'
NEW_FILENAME_FORMAT = 'foDDMMYY.zip'
OLD_FILENAME_PATH = 'YYYY/MMM/'
OLD_FILENAME_FORMAT = 'foDDMMMYYYYbhav.csv.zip'

log_lines = []

def download(date, format='old'):

    if date <= '2016-02-15' or format == 'old':
        url = OLD_URL
        file_path = OLD_FILENAME_PATH.replace('YYYY', dates.yyyy(date))
        file_path = file_path.replace('MMM', dates.MMM(date))
        file_name = OLD_FILENAME_FORMAT.replace('DDMMMYYYY', dates.ddMMMyyyy(date))
    elif format == 'new':
        url = NEW_URL
        file_path = ''
        file_name = NEW_FILENAME_FORMAT.replace('DDMMYY', dates.ddmmyy(date))

    try:
        zip_file = requests.get('{}{}{}'.format(url, file_path, file_name))
        zip_file.raise_for_status()

        temp_file = open('{}{}'.format(PATH, file_name), 'wb')
        temp_file.write(zip_file.content)
        temp_file.close()

        temp_file = zipfile.ZipFile('{}{}'.format(PATH, file_name), 'r')
        temp_file.extractall(PATH)
        temp_file.close()
        os.remove('{}{}'.format(PATH, file_name))
        log_line = '{},{},File downloaded,{}'.format(date, dates.dayofweek(date), file_name)
        log_lines.append('\n{}'.format(log_line))
        print(log_line)
    except:
        log_line = '{},{},File download error,{}'.format(date, dates.dayofweek(date), file_name)
        log_lines.append('\n{}'.format(log_line))
        print(log_line)


def write_log():

    if os.path.isfile('{}{}'.format(PATH, LOGFILE)): # log file exists
        _log_lines = log_lines
    else:
        _log_lines = ['Date,DayOfWeek,Status,FileName'] + log_lines

    f_log = open('{}{}'.format(PATH, LOGFILE), 'a')
    f_log.writelines(_log_lines)
    f_log.close()


def get_bhavcopy(date_range, format='old'):

    for date in date_range:
        download(date, format)

    write_log()

