"""
Created on Feb 28, 2017
@author: Souvik
@Program Function: Download NSE Currency Derivatives Bhavcopy


"""

import requests, zipfile, os
import dates

URL = 'https://www.nseindia.com/archives/cd/bhav/'
LOGFILE = 'data/log.txt'
NEW_FILENAME_FORMAT = 'CD_BhavcopyDDMMYY.zip'
OLD_FILENAME_FORMAT = 'CD_NSEUSDINRDDMMYY.dbf.zip'

log_lines = []

def download(date):

    if date <='2010-10-28':
        file_name = OLD_FILENAME_FORMAT.replace('DDMMYY', dates.ddmmyy(date))
    else:
        file_name = NEW_FILENAME_FORMAT.replace('DDMMYY', dates.ddmmyy(date))

    try:
        zip_file = requests.get('{}{}'.format(URL, file_name))
        zip_file.raise_for_status()

        temp_file = open('data/{}'.format(file_name), 'wb')
        temp_file.write(zip_file.content)
        temp_file.close()

        temp_file = zipfile.ZipFile('data/{}'.format(file_name), 'r')
        temp_file.extractall('data')
        temp_file.close()
        os.remove('data/{}'.format(file_name))
        log_line = '{}, {}: File downloaded: {}'.format(date, dates.dayofweek(date), file_name)
        log_lines.append('\n{}'.format(log_line))
        print(log_line)
    except:
        log_line = '{}, {}: File download error: {}'.format(date, dates.dayofweek(date), file_name)
        log_lines.append('\n{}'.format(log_line))
        print(log_line)


def write_log():

    f_log = open(LOGFILE, 'a')
    f_log.writelines(log_lines)
    f_log.close()


def get_bhavcopy(date_range):

    for date in date_range:
        download(date)

    write_log()

