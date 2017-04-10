"""
Created on Feb 28, 2017
@author: Souvik
@Program Function: Download NSE Currency Derivatives Bhavcopy


"""

import os
import requests, zipfile
import dates, dbfhandler, utils
import pandas as pd
import pickle as pkl

URL = 'https://www.nseindia.com/archives/cd/bhav/'
PATH = 'data/currderivs/fresh/'
DBF_PATH = 'data/currderivs/fresh/dbf/'
CSV_PATH = 'data/currderivs/fresh/csv/'
CSV_BKP_PATH = 'data/currderivs/fresh/csv_bkp/'
LOGFILE = 'log.csv'
NEW_FILENAME_FORMAT = 'CD_BhavcopyDDMMYY.zip'
OLD_FILENAME_FORMAT = 'CD_NSEUSDINRDDMMYY.dbf.zip'
CLEANED = 'cleaned/'
UNCLEANED = 'uncleaned/'
FORMATTED = 'formatted/'
EXPIRIES = 'expiries.txt'
ROLLOVER_MULT = 'rollover_multipliers.txt'
CONTINUOUS = 'continuous/'
VOL_CONTINUOUS = 'continuous_vol/'
OI_CONTINUOUS = 'continuous_oi/'
RATIO_ADJUSTED = 'ratio_adjusted/'
FUTURES = 'futures/'
OPTIONS = 'options/'

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

def csv_copy_with_bkp():

    utils.mkdir(CSV_BKP_PATH)

    csv_files = [f for f in os.listdir(PATH) if f.endswith('.csv')]
    print('Initiating move for ', len(csv_files), ' files...')

    bkp, move = 0, 0
    for file in csv_files:
        if os.path.isfile(CSV_PATH + file):
            os.rename(PATH + file, CSV_BKP_PATH + file)
            print(PATH + file + ' moved to ' + CSV_BKP_PATH + file)
            bkp += 1
        else:
            os.rename(PATH + file, CSV_PATH + file)
            print(PATH + file + ' moved to ' + CSV_PATH + file)
            move += 1
    print('{} files backed up, {} files copied'.format(bkp, move))


def dbf_to_csv(dbf_path=DBF_PATH, csv_path=CSV_PATH):

    utils.mkdir(csv_path)

    dbf_files = [f for f in os.listdir(dbf_path) if f.endswith('.dbf')]

    for file in dbf_files:
        csv_records = dbfhandler.dbf_to_csv('{}{}'.format(dbf_path, file))

        csv_file = open('{}{}.csv'.format(csv_path, file[:-4]), 'w')
        csv_file.writelines(csv_records)
        csv_file.close()
        print('File written: {}'.format('{}{}.csv'.format(csv_path, file[:-4])))


def clean_csv():

    utils.mkdir(CLEANED)

    csv_files = [f for f in os.listdir(os.curdir) if f.endswith('.csv')]
    csv_files.sort()
    print('Initiating cleaning of {} files'.format(len(csv_files)))

    success, error = 0, 0
    TDM, TDW = 0, 0
    save_month = 0
    for file in csv_files:
        try:
            df = pd.read_csv(file)
            date = file[0:10] # Extract date from filename
            # Trading day of month
            if dates.mm_int(date) != save_month: # New month
                save_month = dates.mm_int(date)
                TDM = 1
            else:
                TDM += 1
            # Trading day of week
            if dates.weekday(date) == 0: # Monday
                TDW = 1
            else:
                TDW += 1
            df['Date'] = [date] * len(df['CONTRACT_D'])
            df['Symbol'] = df['CONTRACT_D'].str[0:12]
            df['Expiry'] = df['CONTRACT_D'].str[12:23]
            df['Expiry'] = df['Expiry'].apply(dates.dd_MMM_yyyy_to_yyyy_mm_dd)
            df['TDM'] = [TDM] * len(df['CONTRACT_D'])
            df['TDW'] = [TDW] * len(df['CONTRACT_D'])

            first_cols = ['Symbol', 'Date', 'TDM', 'TDW', 'Expiry']
            df = df.reindex_axis( first_cols + list(set(df.columns) - set(first_cols)), axis=1)
            if file.find('OP') >= 0:
                df['OptionType'] = df['CONTRACT_D'].str[23:25]
                df['StrikePrice'] = df['CONTRACT_D'].str[25:50]
                first_cols = ['Symbol', 'Date', 'TDM', 'TDW', 'Expiry', 'OptionType', 'StrikePrice']
                df = df.reindex_axis(first_cols + list(set(df.columns) - set(first_cols)), axis=1)

            df.drop('CONTRACT_D', axis=1, inplace=True)

            df.to_csv('{}{}'.format(CLEANED, file), sep=',', index=False)
            os.remove(file)
            print(df['Date'][0], ',File Cleaned')
            success += 1
        except:
            print(df['Date'][0], ',Error in cleaning')
            error += 1

    print('{} files cleaned, {} errors'.format(success, error))


def format_csv_futures(*columns):

    utils.mkdir(FORMATTED)

    csv_files = [f for f in os.listdir(os.curdir) if f.find('OP') < 0 and f.endswith('.csv')]

    print('Initiating formatting of {} files'.format(len(csv_files)))

    cols = [c for c in columns]

    success, error = 0, 0
    for file in csv_files:
        try:
            df = pd.read_csv(file)
            date = file[0:10]  # Extract date from filename
            df = df.reindex_axis(cols, axis=1)
            df.to_csv('{}{}'.format(FORMATTED, file), sep=',', index=False)
            print(date, ',File formatted', file)
            success += 1
        except:
            print(date, ',Error in formatting', file)
            error += 1

    print('{} files formatted, {} errors'.format(success, error))


def ren_csv_files():

    utils.mkdir(FUTURES)
    utils.mkdir(OPTIONS)

    fut_files = [f for f in os.listdir(os.curdir) if f.find('OP') < 0 and f.endswith('.csv')]
    opt_files = [f for f in os.listdir(os.curdir) if f.find('OP') >= 0 and f.endswith('.csv')]

    print('Initiating renaming of {} futures & {} options files'.format(len(fut_files), len(opt_files)))

    successf, errorf = 0, 0
    successo, erroro = 0, 0
    for file in fut_files:
        try:
            new_name = '{}{}.csv'.format(FUTURES, dates.ddmmyy_to_yyyy_mm_dd(file[-10:][:6]))
            os.rename(file, new_name)
            print(new_name, 'file renamed')
            successf += 1
        except:
            print(new_name, 'file rename failed')
            errorf += 1

    for file in opt_files:
        try:
            new_name = '{}{}.csv'.format(OPTIONS, dates.ddmmyy_to_yyyy_mm_dd(file[-10:][:6]))
            os.rename(file, new_name)
            print(new_name, 'file renamed')
            successo += 1
        except:
            print(new_name, 'file rename failed')
            erroro += 1

    print('{} futures files renamed, {} errors'.format(successf, errorf))
    print('{} options files renamed, {} errors'.format(successo, erroro))


def select_expiry(expiry_dates, date, symbol, delta, series=0):

    expiry_index = 0
    for expiry in expiry_dates[symbol]:
        if expiry > dates.relativedate(date, days=delta):
            print('select_expiry', symbol, date, delta, series, expiry_dates[symbol][expiry_index + series])
            return expiry_dates[symbol][expiry_index + series]
        expiry_index += 1


def select_expiry_new(csv_files, expiry_hist, date, symbol, delta):

    #expiry_index = 0
    #print('select_expiry_new', symbol, date, delta)
    #print(trading_days_between('2010-01-01', '2010-01-04', csv_files))
    for expiry in expiry_hist['expiry_dates'][symbol]:
        #if expiry > dates.relativedate(date, days=delta):
        #if expiry_hist['eexpiry_hist['expiry_TDMs'][expiry] - TDM < deltaxpiry_TDMs'][exp[d][symbol]] - df['TDM'][0] >= d:
        #print('select_expiry_new 2 %%%%%%%%%', expiry_hist['expiry_TDMs'][expiry], TDM, delta, expiry, date)
        #if expiry_hist['expiry_TDMs'][expiry] - TDM > delta and expiry > date:
        #print(type(expiry), type(date))
        if trading_days_between(date, expiry, csv_files) > delta and expiry > date:
            #print('select_expiry', symbol, date, delta, TDM, expiry_hist['expiry_dates'][symbol][expiry_index + delta])
            #print('select_expiry_new', symbol, date, delta, TDM, expiry)
            return expiry
        #expiry_index += 1

def select_near_expiry(expiry_dates, date, symbol, delta):

    for expiry in expiry_dates[symbol]:
        if expiry > dates.relativedate(date, days=delta):
            # print('select_near_expiry', symbol, date, delta, expiry)
            return expiry

def select_far_expiry(expiry_dates, date, symbol, delta):

    #print('select_expiry', symbol, date, delta)
    for expiry in expiry_dates[symbol]:
        if int(date[8:10]) < delta:
            month_delta = 1
        else:
            month_delta = 2
        if expiry > dates.relativedate(date, months=month_delta):
            #print('select_far_expiry', symbol, date, delta, expiry)
            return expiry


def continuous_contracts(delta=0):
    """
    Create continuous contracts file for near and far series
    :param delta: Contract switch day difference from expiry day
    :return: None, Create continuous contracts file
    """

    if not os.path.isfile(EXPIRIES):
        write_expiry_hist()
    expiry_hist = read_expiry_hist(EXPIRIES)
    print(expiry_hist)

    utils.mkdir(CONTINUOUS)

    csv_files = [f for f in os.listdir(os.curdir) if f.endswith('.csv')]

    print('Initiating continuous contract creation for {} days'.format(len(csv_files)))

    near_exp, far_exp = {}, {}  # '1900-01-01', '1900-01-01' # Initialize

    success, error = 0, 0
    for file in csv_files:
        try:
            date = file[0:10]
            df = pd.read_csv(file)
            date_pd = pd.DataFrame()
            for symbol in df['Symbol'].unique():
                if symbol not in near_exp:
                    near_exp[symbol], far_exp[symbol] = '1900-01-01', '1900-01-01'  # Initialize

                if near_exp[symbol] <= dates.relativedate(date, days=delta):
                    near_exp[symbol] = select_expiry(expiry_hist['expiry_dates'], date, symbol, delta, 0)
                    far_exp[symbol] = select_expiry(expiry_hist['expiry_dates'], date, symbol, delta, 1)
                series1 = df.loc[(df['Symbol'] == symbol) & (df['Expiry'] == near_exp[symbol])]
                series2 = df.loc[(df['Symbol'] == symbol) & (df['Expiry'] == far_exp[symbol])]
                series1['Symbol'], series2['Symbol'] = series1['Symbol'] + '-I', series2['Symbol'] + '-II'
                if date_pd.empty:
                    date_pd = pd.concat([series1, series2], axis=0)
                else:
                    date_pd = pd.concat([date_pd, series1, series2], axis=0)
            date_pd.to_csv('{}{}'.format(CONTINUOUS, file), sep=',', index=False)
            print(date, ',Continuous contract created', file)
            success += 1
        except:
            print(date, ',Error creating Continuous contract', file)
            error += 1

    print('Contract created for {} days, {} errors'.format(success, error))


def continuous_contracts_all(delta=None):
    """
    Create continuous contracts file for near and far series
    :param delta: List of Contract switch day differences from expiry day
    :return: None, Create continuous contracts file
    """

    if delta is None:
        delta = [0]

    if not os.path.isfile(EXPIRIES):
        write_expiry_hist()
    expiry_hist = read_expiry_hist(EXPIRIES)
    print(expiry_hist)

    utils.mkdir(CONTINUOUS)

    romans = {0:'0', 1:'I', 2:'II', 3:'III', 4:'IV', 5:'V', 6:'VI', 7:'VII', 8:'VIII', 9:'IX', 10:'X', 11:'XI',
              12:'XII', 13:'XIII', 14:'XIV', 15:'XV'}

    csv_files = [f for f in os.listdir(os.curdir) if f.endswith('.csv')]
    print('Initiating continuous contract creation for {} days'.format(len(csv_files)))

    exp = [{}]
    success, error = 0, 0
    for file in csv_files:
        try:
            date = file[0:10]
            df = pd.read_csv(file)
            date_pd = pd.DataFrame()
            for symbol in df['Symbol'].unique():
                if symbol not in exp[0]:
                    for d in delta:
                        if d > 0:
                            exp.append({})
                        exp[d][symbol] = '1900-01-01'  # Initialize

                # print('#####', exp)

                series = []
                for d in delta:
                    # if exp[d][symbol] <= dates.relativedate(date, days=d):
                    # print('$$$$$$$$', d, symbol, exp[d][symbol], '%%%%', exp)
                    if expiry_hist['expiry_TDMs'][exp[d][symbol]] - df['TDM'][0] < d:
                        exp[d][symbol] = select_expiry_new(csv_files, expiry_hist, date, symbol, d)
                    series.append(df.loc[(df['Symbol'] == symbol) & (df['Expiry'] == exp[d][symbol])])
                    #if d == 0:
                    #    series[d]['Symbol'] = series[d]['Symbol'] + '-0'
                    #else:
                    #    series[d]['Symbol'] = series[d]['Symbol'] + '-' + 'I' * d
                    series[d]['Symbol'] = series[d]['Symbol'] + '-' + romans[d]
                    date_pd = pd.concat([date_pd, series[d]], axis=0)

            date_pd.to_csv('{}{}'.format(CONTINUOUS, file), sep=',', index=False)
            print(date, ',Continuous contract created', file)
            success += 1

        except:
            print(date, ',Error creating Continuous contract', file)
            error += 1


    print('Contract created for {} days, {} errors'.format(success, error))


def continuous_contracts_far_switch(near_delta=0, far_delta=10):
    """
    Create continuous contracts file for near and far series, with far series switching on far_delta days
    :param near_delta: Near Contract switch day difference from expiry day
    :param far_delta: Far Contract switch day as month calendar day
    :return: None, Create continuous contracts file
    """

    if not os.path.isfile(EXPIRIES):
        write_expiry_hist()
    expiry_hist = read_expiry_hist(EXPIRIES)
    print(expiry_hist)

    utils.mkdir(CONTINUOUS)

    csv_files = [f for f in os.listdir(os.curdir) if f.endswith('.csv')]

    print('Initiating continuous contract creation for {} days'.format(len(csv_files)))

    near_exp, far_exp = {}, {} #'1900-01-01', '1900-01-01' # Initialize

    success, error = 0, 0
    for file in csv_files:
        try:
            date = file[0:10]
            df = pd.read_csv(file)
            date_pd = pd.DataFrame()
            for symbol in df['Symbol'].unique():
                if symbol not in near_exp:
                    near_exp[symbol], far_exp[symbol] = '1900-01-01', '1900-01-01'  # Initialize

                if near_exp[symbol] <= dates.relativedate(date, days=near_delta):
                    near_exp[symbol] = select_near_expiry(expiry_hist['expiry_dates'], date, symbol, near_delta)

                if int(date[8:10]) < far_delta:
                    month_delta = 1
                else:
                    month_delta = 2
                exp_month_start_date = dates.relativedate(date, months=month_delta)
                exp_month_start_date = dates.setdate(exp_month_start_date, day=1)

                if far_exp[symbol] < exp_month_start_date:
                    far_exp[symbol] = select_far_expiry(expiry_hist['expiry_dates'], date, symbol, far_delta)
                series1 = df.loc[(df['Symbol'] == symbol) & (df['Expiry'] == near_exp[symbol])]
                series2 = df.loc[(df['Symbol'] == symbol) & (df['Expiry'] == far_exp[symbol])]
                series1['Symbol'], series2['Symbol'] = series1['Symbol'] + '-I', series2['Symbol'] + '-II'
                if date_pd.empty:
                    date_pd = pd.concat([series1, series2], axis=0)
                else:
                    date_pd = pd.concat([date_pd, series1, series2], axis=0)
            date_pd.to_csv('{}{}'.format(CONTINUOUS, file), sep=',', index=False)
            print(date, ',Continuous contract created', file)
            success += 1
        except:
            print(date, ',Error creating Continuous contract', file)
            error += 1

    print('Contract created for {} days, {} errors'.format(success, error))


def write_expiry_hist(e_file=EXPIRIES):

    expiries = {}
    expiry_TDMs = {}

    csv_files = [f for f in os.listdir(os.curdir) if f.endswith('.csv')]

    expiry_TDMs['1900-01-01'] = 0

    for file in csv_files:
        df = pd.read_csv(file)

        for index, row in df.iterrows():
            if row['Symbol'] not in expiries:
                expiries[row['Symbol']] = [row['Expiry']]
            if row['Expiry'] not in expiries[row['Symbol']]:
                #if row['Symbol'] == 'FUTCURUSDINR':
                #    print(row['Symbol'], row['Date'], row['Expiry'])
                expiries[row['Symbol']].append(row['Expiry'])
            if row['Expiry'] not in expiry_TDMs:
                expiry_TDMs[row['Expiry']] = 100 # Initialize
            if row['Expiry'] == row['Date'] and expiry_TDMs[row['Date']] == 100:
                expiry_TDMs[row['Expiry']] = row['TDM']

    for key, value in expiries.items():
        expiries[key].sort()

    max_date = max(csv_files)[0:10]

    for key, value in expiry_TDMs.items():
        fdate = key
        if value == 100 and fdate <= max_date:
            while(value == 100):
                if os.path.isfile('{}.csv'.format(fdate)):
                    df = pd.read_csv('{}.csv'.format(fdate))
                    #print(df['TDM'][0])
                    expiry_TDMs[key], value = df['TDM'][0], df['TDM'][0]
                fdate = dates.relativedate(fdate, days=-1)

    with open(e_file, 'wb') as handle:
        pkl.dump({'expiry_dates': expiries, 'expiry_TDMs': expiry_TDMs}, handle)


def read_expiry_hist(e_file=EXPIRIES):

    with open(e_file, 'rb') as handle:
        expiry_hist = pkl.load(handle)

    return expiry_hist

def trading_days_between(start, end, csv_files):
    return len([f[0:10] for f in csv_files if f[0:10] >= start and f[0:10] <= end])


def read_rollover_mult_hist(e_file=ROLLOVER_MULT):

    with open(e_file, 'rb') as handle:
        rollover_mult_hist = pkl.load(handle)

    return rollover_mult_hist


def continuous_contracts_vol_oi_rollover(parm):
    """
    Create continuous contracts file for near and far series
    :param 'Volume' or 'Open Interest'
    :return: None, Create continuous contracts file
    """

    if not os.path.isfile(EXPIRIES):
        write_expiry_hist()

    e = read_expiry_hist()
    print(e)

    exphist = e['expiry_dates']

    if parm == 'Volume':
        path = VOL_CONTINUOUS
        field = 'TRD_NO_CON'
    elif parm == 'Open Interest':
        path = OI_CONTINUOUS
        field = 'OI_NO_CON'

    utils.mkdir(path)

    csv_files = [f for f in os.listdir(os.curdir) if f.endswith('.csv')]
    print('Initiating continuous contract creation for {} days'.format(len(csv_files)))

    exp_idx = {}
    exp_rollover = {}
    rollover_multiplier = {}
    success, error = 0, 0
    for file in csv_files:
        try:
            date = file[0:10]
            df = pd.read_csv(file)
            date_pd = pd.DataFrame()
            for symbol in df['Symbol'].unique():
                # print(symbol, '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
                if symbol not in exp_idx:
                    exp_idx[symbol] = -1  # Initialize
                    exp_rollover[symbol] = False  # Initialize
                    rollover_multiplier[symbol] = {}  # Initialize

                if exp_idx[symbol] == -1:  # First record for symbol
                    sel_record = df.loc[(df['Symbol'] == symbol) & (df['Expiry'] == exphist[symbol][0])]
                    exp_idx[symbol] = 0
                    # print('@@@ 1', exphist[symbol][0])
                # elif exp_idx[symbol] == len(exphist[symbol]) - 1:  # Last expiry for symbol
                #    sel_record = df.loc[
                #        (df['Symbol'] == symbol) & (df['Expiry'] == exphist[symbol][exp_idx[symbol]])]
                #    print('@@@ 2', exphist[symbol][exp_idx[symbol]])
                else:
                    curr_record = df.loc[
                        (df['Symbol'] == symbol) & (df['Expiry'] == exphist[symbol][exp_idx[symbol]])]
                    curr_exp_idx = exp_idx[symbol]
                    nxt_exp_idx = curr_exp_idx
                    # print('%%%%%%%%%%%%%%%%%%%%', exphist[symbol][curr_exp_idx][0:7], exphist[symbol][nxt_exp_idx][0:7])
                    while exphist[symbol][curr_exp_idx][0:7] == exphist[symbol][nxt_exp_idx][0:7]:
                        nxt_exp_idx += 1
                    nxt_record = df.loc[(df['Symbol'] == symbol)
                                        & (df['Expiry'] == exphist[symbol][nxt_exp_idx])]
                    # print('@@@ 3', exphist[symbol][exp_idx[symbol]], exphist[symbol][nxt_exp_idx])

                    if not curr_record.empty and not nxt_record.empty:
                        # print('@@@ 4')
                        if exp_rollover[symbol]:
                            sel_record = curr_record
                            exp_rollover[symbol] = False
                            # print('@@@ 5')
                        else:
                            sel_record = curr_record
                            # print('@@@ 6')
                        if int(curr_record[field]) < int(nxt_record[field]):
                            # print('@@@ 7')
                            exp_rollover[symbol] = True
                            # exp_idx[symbol] += 1
                            exp_idx[symbol] = nxt_exp_idx
                            # print(type(curr_record['CLOSE_PRIC'].iloc[0]), type(nxt_record['CLOSE_PRIC'].iloc[0]))
                            rollover_multiplier[symbol][date] = float(curr_record['CLOSE_PRIC'].iloc[0]) / \
                                                                float(nxt_record['CLOSE_PRIC'].iloc[0])
                    elif curr_record.empty and nxt_record.empty:
                        # print('@@@ 8')
                        pass
                    elif curr_record.empty:
                        sel_record = nxt_record
                        # print('@@@ 9')
                        exp_idx[symbol] += 1
                        # rollover_multiplier[str.strip(symbol)][date] = 1
                        rollover_multiplier[symbol][date] = 1
                    elif nxt_record.empty:
                        sel_record = curr_record
                        # print('@@@ 10')

                # print(sel_record['Symbol'], sel_record['Date'], sel_record['Expiry'])
                if not sel_record.empty:
                    date_pd = pd.concat([date_pd, sel_record], axis=0)

            # date_pd['Symbol'] = date_pd['Symbol'].apply(str.strip)
            date_pd.to_csv('{}{}'.format(path, file), sep=',', index=False)
            print(date, ',Continuous contract created', file)
            success += 1



        except:
            print(date, ',Error creating Continuous contract', file)
            error += 1


    with open(path + ROLLOVER_MULT, 'wb') as handle:
        pkl.dump(rollover_multiplier, handle)

    print('Contract created for {} days, {} errors'.format(success, error))

    print(rollover_multiplier)


def ratio_adjust():
    """
    Forward Ratio adjust continuous contract files
    :return: None, create forward ratio adjusted continuous contracts
    """

    csv_files = [f for f in os.listdir(os.curdir) if f.endswith('.csv')]
    csv_files.sort()

    rollover_mult_hist = read_rollover_mult_hist()
    print(rollover_mult_hist)

    utils.mkdir(RATIO_ADJUSTED)

    multipliers, symbol_curr_close = {}, {}
    success, error = 0, 0
    for file in csv_files:
        try:
            date = file[0:10]
            df = pd.read_csv(file)

            for symbol in df['Symbol'].unique():
                if symbol not in multipliers:
                    multipliers[symbol] = 1  # Initialize

            for i, row in df.iterrows():
                df.ix[i, 'OPEN_PRICE'] = round(df.ix[i, 'OPEN_PRICE'] * multipliers[df.ix[i, 'Symbol']], 2)
                df.ix[i, 'HIGH_PRICE'] = round(df.ix[i, 'HIGH_PRICE'] * multipliers[df.ix[i, 'Symbol']], 2)
                df.ix[i, 'LOW_PRICE'] = round(df.ix[i, 'LOW_PRICE'] * multipliers[df.ix[i, 'Symbol']], 2)
                df.ix[i, 'CLOSE_PRIC'] = round(df.ix[i, 'CLOSE_PRIC'] * multipliers[df.ix[i, 'Symbol']], 2)

            for symbol in df['Symbol'].unique():
                if date in rollover_mult_hist[symbol]:
                    multipliers[symbol] = multipliers[symbol] * rollover_mult_hist[symbol][date]


            df.to_csv('{}{}'.format(RATIO_ADJUSTED, file), sep=',', index=False)
            print(date, ',Continuous contract created', file)
            success += 1

        except:
            print(date, ',Error creating Continuous contract', file)
            error += 1

    print('Contract created for {} days, {} errors'.format(success, error))




