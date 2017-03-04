"""
Created on Feb 28, 2017
@author: Souvik
@Program Function: Download NSE Currency Derivatives Bhavcopy


"""

import requests, zipfile, os
import dates


NEW_URL = 'https://www.nseindia.com/archives/fo/bhav/'
OLD_URL = 'https://www.nseindia.com/content/historical/DERIVATIVES/'
PATH = 'data/eqderivs/'
DBF_PATH = 'data/eqderivs/dbf'
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
        zip_file_name = OLD_FILENAME_FORMAT.replace('DDMMMYYYY', dates.ddMMMyyyy(date))
    elif format == 'new':
        url = NEW_URL
        file_path = ''
        zip_file_name = NEW_FILENAME_FORMAT.replace('DDMMYY', dates.ddmmyy(date))

    try:
        files = ''

        zip_file = requests.get('{}{}{}'.format(url, file_path, zip_file_name))
        zip_file.raise_for_status()

        temp_file = open('{}{}'.format(PATH, zip_file_name), 'wb')
        temp_file.write(zip_file.content)
        temp_file.close()

        temp_file = zipfile.ZipFile('{}{}'.format(PATH, zip_file_name), 'r')
        for file in temp_file.namelist():
            temp_file.extract(file, DBF_PATH) if file[-3:] == 'dbf' else temp_file.extract(file, PATH)
            files = '{}{},'.format(files, file)
        temp_file.close()

        os.remove('{}{}'.format(PATH, zip_file_name))
        log_line = '{},{},File downloaded,{},{}'.format(date, dates.dayofweek(date), zip_file_name, files)
        log_lines.append('\n{}'.format(log_line))
        print(log_line)
    except:
        log_line = '{},{},File download error,{},{}'.format(date, dates.dayofweek(date), zip_file_name, files)
        log_lines.append('\n{}'.format(log_line))
        print(log_line)


def write_log():

    if os.path.isfile('{}{}'.format(PATH, LOGFILE)): # log file exists
        _log_lines = log_lines
    else:
        _log_lines = ['Date,DayOfWeek,Status,ZipFile,Files'] + log_lines

    f_log = open('{}{}'.format(PATH, LOGFILE), 'a')
    f_log.writelines(_log_lines)
    f_log.close()


def get_bhavcopy(date_range, format='old'):

    for date in date_range:
        download(date, format)

    write_log()

