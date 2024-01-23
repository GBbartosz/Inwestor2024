import datetime
import pandas as pd
import requests
import sys
import yfinance as yf


def pandas_df_display_options():
    pd.reset_option('display.max_rows')
    pd.reset_option('display.max_columns')
    pd.reset_option('display.width')
    pd.reset_option('display.float_format')
    pd.reset_option('display.max_colwidth')

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_colwidth', 20)
    pd.set_option('display.width', 400)


def get_update_notebook():
    # gets only records which haven't benn updated today already
    # updates first the oldest records
    global today
    df = pd.read_excel('C:\\Users\\barto\\Desktop\\Inwestor_2024\\update_notebook.xlsx', index_col=0)
    df = df.sort_values(by='last_update_date', ascending=True, na_position='first')
    df_to_update = df[df['last_update_date'] != today]
    return df, df_to_update


def download_financial_statements(ticker):
    # if function in 'INCOME_STATEMENT', 'BALANCE_SHEET', 'CASH_FLOW' creates new file or adds new data to existing files
    # if function in 'OVERVIEW' always creates new file

    def api_limit(mydata):
        # ends execution iif api limit is reached
        global total_update_df
        if 'Information' in mydata.keys():
            total_update_df.to_excel('C:\\Users\\barto\\Desktop\\Inwestor_2024\\update_notebook.xlsx')
            print('You reached api limit (25 per day)!')
            sys.exit()

    def download_data(myticker, myfunction):
        apikey = 'KMTF2LUFBCUIXYQU'
        url = f'https://www.alphavantage.co/query?function={myfunction}&symbol={myticker}&apikey={apikey}'
        r = requests.get(url)
        mydata = r.json()
        api_limit(mydata)
        return mydata

    functions = ['INCOME_STATEMENT', 'BALANCE_SHEET', 'CASH_FLOW']
    for function in functions:
        file_path = f'C:\\Users\\barto\\Desktop\\Inwestor_2024\\financial_statements\\{ticker}_{function}.csv'
        data = download_data(ticker, function)
        new_df = pd.DataFrame(data['quarterlyReports']).set_index('fiscalDateEnding')
        try:
            old_df = pd.read_csv(file_path, index_col=0)
            mask = ~new_df.index.isin(old_df.index)
            if True not in mask:  # break if no new data
                try:  # try to read last updated file. If doesn't exist there is still need to download data
                    pd.read_csv(f'C:\\Users\\barto\\Desktop\\Inwestor_2024\\financial_statements\\{ticker}_CASH_FLOW.csv', index_col=0)
                    break
                except FileNotFoundError:
                    pass
            df = pd.concat([new_df[mask], old_df])
        except FileNotFoundError:
            df = new_df
        df = df.sort_index(ascending=False)
        df.to_csv(file_path)

    function = 'OVERVIEW'
    file_path = f'C:\\Users\\barto\\Desktop\\Inwestor_2024\\financial_statements\\{ticker}_{function}.csv'
    data = download_data(ticker, function)
    df = pd.DataFrame(data=data.values(), columns=['data'], index=data.keys())
    df.to_csv(file_path)


def download_price(ticker):
    # always creates new file
    price_df = yf.download(ticker, start='2018-01-01', end=datetime.datetime.today().date())
    price_df = price_df.sort_index(ascending=False)
    price_df.to_csv(f'C:\\Users\\barto\\Desktop\\Inwestor_2024\\price\\{ticker}_price.csv')


pandas_df_display_options()
today = pd.to_datetime(datetime.datetime.today().date())
total_update_df, to_update_df = get_update_notebook()
tickers = to_update_df.index

for ticker in tickers:
    print(ticker)
    download_financial_statements(ticker)
    download_price(ticker)
    total_update_df.loc[ticker, 'last_update_date'] = today
    print('Success!')

total_update_df.to_excel('C:\\Users\\barto\\Desktop\\Inwestor_2024\\update_notebook.xlsx')
