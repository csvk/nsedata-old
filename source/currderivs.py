"""
Created on Feb 28, 2017
@author: Souvik
@Program Function: Download NSE Currency Derivatives Bhavcopy


"""

import requests, zipfile, os
import dates


URL = 'https://www.nseindia.com/archives/cd/bhav/'
NEW_SAVE_PATH = 'data/currderivs/'
OLD_SAVE_PATH = 'data/currderivs/dbf/'
LOGFILE = 'log.csv'
NEW_FILENAME_FORMAT = 'CD_BhavcopyDDMMYY.zip'
OLD_FILENAME_FORMAT = 'CD_NSEUSDINRDDMMYY.dbf.zip'

log_lines = []

def download(date):


    if date <='2010-10-28':
        file_name = OLD_FILENAME_FORMAT.replace('DDMMYY', dates.ddmmyy(date))
        save_path = OLD_SAVE_PATH
    else:
        file_name = NEW_FILENAME_FORMAT.replace('DDMMYY', dates.ddmmyy(date))
        save_path = NEW_SAVE_PATH

    try:
        zip_file = requests.get('{}{}'.format(URL, file_name))
        zip_file.raise_for_status()

        temp_file = open('{}{}'.format(save_path, file_name), 'wb')
        temp_file.write(zip_file.content)
        temp_file.close()

        temp_file = zipfile.ZipFile('{}{}'.format(save_path, file_name), 'r')
        temp_file.extractall(save_path)
        temp_file.close()
        os.remove('{}{}'.format(save_path, file_name))
        log_line = '{},{},File downloaded,{}'.format(date, dates.dayofweek(date), file_name)
        log_lines.append('\n{}'.format(log_line))
        print(log_line)
    except:
        log_line = '{},{},File download error,{}'.format(date, dates.dayofweek(date), file_name)
        log_lines.append('\n{}'.format(log_line))
        print(log_line)


def write_log():

    if os.path.isfile('{}{}'.format(NEW_SAVE_PATH, LOGFILE)): # log file exists
        _log_lines = ['Date,DayOfWeek,Status,FileName'] + log_lines
    else:
        _log_lines = log_lines

    f_log = open('{}{}'.format(NEW_SAVE_PATH, LOGFILE), 'a')
    f_log.writelines(_log_lines)
    f_log.close()


def get_bhavcopy(date_range):

    for date in date_range:
        download(date)

    write_log()


