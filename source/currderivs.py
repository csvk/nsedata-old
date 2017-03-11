"""
Created on Feb 28, 2017
@author: Souvik
@Program Function: Download NSE Currency Derivatives Bhavcopy


"""

import os
import requests, zipfile
import dates, dbfhandler, utils
import pandas as pd

URL = 'https://www.nseindia.com/archives/cd/bhav/'
PATH = 'data/currderivs/'
DBF_PATH = 'data/currderivs/dbf/'
CSV_PATH = 'data/currderivs/csv/'
LOGFILE = 'log.csv'
NEW_FILENAME_FORMAT = 'CD_BhavcopyDDMMYY.zip'
OLD_FILENAME_FORMAT = 'CD_NSEUSDINRDDMMYY.dbf.zip'
CLEANED = 'cleaned/'
UNCLEANED = 'uncleaned/'
FORMATTED = 'formatted/'

log_lines = []

def download(date):

    utils.mkdir(PATH)
    utils.mkdir(DBF_PATH)

    if date <='2010-10-28':
        zip_file_name = OLD_FILENAME_FORMAT.replace('DDMMYY', dates.ddmmyy(date))
    else:
        zip_file_name = NEW_FILENAME_FORMAT.replace('DDMMYY', dates.ddmmyy(date))

    try:
        files = ''

        zip_file = requests.get('{}{}'.format(URL, zip_file_name))
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


def get_bhavcopy(date_range):

    for date in date_range:
        download(date)

    write_log()



def dbf_to_csv(dbf_path=DBF_PATH, csv_path=CSV_PATH):

    dbf_files = [f for f in os.listdir(dbf_path) if f.endswith('.dbf')]

    for file in dbf_files:
        csv_records = dbfhandler.dbf_to_csv('{}{}'.format(dbf_path, file))

        csv_file = open('{}{}.csv'.format(csv_path, file[:-4]), 'a')
        csv_file.writelines(csv_records)
        csv_file.close()
        print('File written: {}'.format('{}{}.csv'.format(csv_path, file[:-4])))

def clean_csv(path=CSV_PATH):

    cleaned_dir = '{}{}'.format(path, CLEANED)
    utils.mkdir(cleaned_dir)
    uncleaned_dir = '{}{}'.format(path, UNCLEANED)
    utils.mkdir(uncleaned_dir)

    csv_files = [f for f in os.listdir(path) if f.endswith('.csv')]

    for file in csv_files:
        try:
            df = pd.read_csv('{}{}'.format(path, file))
            df_bkp = df
            df['Date'] = [dates.ddmmyy_to_yyyy_mm_dd(file[-10:][:6])] * len(df['CONTRACT_D']) # Extract date from filename

            df['Symbol'] = df['CONTRACT_D'].str[0:12]
            df['Expiry'] = df['CONTRACT_D'].str[12:23]

            first_cols = ['Symbol', 'Date', 'Expiry']
            df = df.reindex_axis( first_cols + list(set(df.columns) - set(first_cols)), axis=1)
            if file.find('OP') >= 0:
                df['OptionType'] = df['CONTRACT_D'].str[23:25]
                df['StrikePrice'] = df['CONTRACT_D'].str[25:50]
                first_cols = ['Symbol', 'Date', 'Expiry', 'OptionType', 'StrikePrice']
                df = df.reindex_axis(first_cols + list(set(df.columns) - set(first_cols)), axis=1)

            df.drop('CONTRACT_D', axis=1, inplace=True)

            df.to_csv('{}{}{}'.format(path, CLEANED, file), sep=',', index=False)
            df_bkp.to_csv('{}{}{}'.format(path, UNCLEANED, file), sep=',', index=False)
            os.remove('{}{}'.format(path, file))
            print(df['Date'][0], ',File Cleaned')
        except:
            print(df['Date'][0], ',Error in cleaning')


def format_csv_futures(path, *columns):

    os.chdir(path)
    utils.mkdir(FORMATTED)

    csv_files = [f for f in os.listdir(os.curdir) if f.find('OP') < 0 and f.endswith('.csv')]

    print('Initiating formatting of {} files', len(csv_files))

    cols = [c for c in columns]

    for file in csv_files:
        try:
            df = pd.read_csv(file)
            date = dates.ddmmyy_to_yyyy_mm_dd(file[-10:][:6])  # Extract date from filename
            df = df.reindex_axis(cols, axis=1)
            df.to_csv('{}{}'.format(FORMATTED, file), sep=',', index=False)
            print(date, ',File Cleaned', file)
        except:
            print(date, ',Error in cleaning', file)











