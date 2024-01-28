import pandas as pd

from mergeddfread import MergedDfRead


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


def read_financial_statement(financial_statement, ticker):
    df = pd.read_csv(f'C:\\Users\\barto\\Desktop\\Inwestor_2024\\financial_statements\\{ticker}_{financial_statement}.csv', index_col=0).sort_index(ascending=True)
    df.index = pd.to_datetime(df.index)

    balance_not_summaring_cols = ['commonStockSharesOutstanding']

    for col in df.columns:
        if col != 'reportedCurrency' and col not in balance_not_summaring_cols:
            df[col] = df[col].rolling(window=4, min_periods=4).sum()  # summaring quarters to years
    df = df.iloc[3:, :]
    return df


def read_earnings(ticker):
    df = pd.read_csv(f'C:\\Users\\barto\\Desktop\\Inwestor_2024\\financial_statements\\{ticker}_EARNINGS.csv', index_col=0).sort_index(ascending=True)
    df.index = pd.to_datetime(df.index)
    df['EPS'] = df['reportedEPS'].rolling(window=4, min_periods=4).sum()
    df = df.iloc[3:, :]
    return df


def calculation_income_statement(df):
    # revenue growth
    df['i_revenue_growth_1y'] = df['totalRevenue'] / df['totalRevenue'].shift(1*4) - 1
    df['i_revenue_growth_2y'] = df['totalRevenue'] / df['totalRevenue'].shift(2*4) - 1
    df['i_revenue_growth_3y'] = df['totalRevenue'] / df['totalRevenue'].shift(3*4) - 1
    df['i_revenue_growth_4y'] = df['totalRevenue'] / df['totalRevenue'].shift(4*4) - 1
    return df


def indicators_calculation(df):
    mdf = MergedDfRead(df)

    # Capitalization
    mdf.marketCapitalization = mdf.Adj_Close * mdf.b_commonStockSharesOutstanding

    # Margins
    mdf.i_grossMargin = mdf.is_grossProfit / mdf.is_totalRevenue
    mdf.i_EBITDAMargin = mdf.is_ebitda / mdf.is_totalRevenue
    mdf.i_EBITMargin = mdf.is_ebit / mdf.is_totalRevenue
    mdf.i_netMargin = mdf.is_netIncome / mdf.is_totalRevenue

    # Price indicators
    mdf.i_PS = mdf.marketCapitalization / mdf.is_totalRevenue
    mdf.i_PE = mdf.marketCapitalization / mdf.is_netIncome

    mdf = mdf.update_df_columns_from_class_attributes(mdf)
    return mdf.df


def create_final_data_file(mytickers):
    global folder_path
    indicator_columns = []
    dfs = []
    for tic in mytickers:
        try:
            file_path = f'{folder_path}analyze\\{tic}_indicators.csv'
            df = pd.read_csv(file_path, index_col=0)
            df = df[[c for c in df.columns if 'i_' in c]]
            df['ticker'] = tic
            df['date'] = df.index
            dfs.append(df)
        except:
            print('No file {tic}_indicators.csv')

    final_df = pd.concat(dfs, ignore_index=True)
    final_df.to_csv(f'{folder_path}final_data.csv')




folder_path = 'C:\\Users\\barto\\Desktop\\Inwestor_2024\\'
pandas_df_display_options()
update_df = pd.read_excel('C:\\Users\\barto\\Desktop\\Inwestor_2024\\update_notebook.xlsx')
update_df = update_df[update_df['last_update_date'].notna()]
tickers = update_df['ticker']
for ticker in tickers:
    print(ticker)
    isdf = read_financial_statement('INCOME_STATEMENT', ticker)
    bdf = read_financial_statement('BALANCE_SHEET', ticker)
    cfdf = read_financial_statement('CASH_FLOW', ticker)
    edf = read_earnings(ticker)

    odf = pd.read_csv(f'C:\\Users\\barto\\Desktop\\Inwestor_2024\\financial_statements\\{ticker}_OVERVIEW.csv')

    pdf = pd.read_csv(f'C:\\Users\\barto\\Desktop\\Inwestor_2024\\price\\{ticker}_price.csv', index_col=0).sort_index(ascending=True)
    pdf.index = pd.to_datetime(pdf.index)

    pdf = pdf[pdf.index >= min(isdf.index)]

    # calculation in time (vertical)
    isdf = calculation_income_statement(isdf)

    # merging
    merged_df = pd.merge_asof(pdf, isdf.add_prefix('is_'), left_index=True, right_index=True, direction='backward')
    merged_df = pd.merge_asof(merged_df, bdf.add_prefix('b_'), left_index=True, right_index=True, direction='backward')
    merged_df = pd.merge_asof(merged_df, cfdf.add_prefix('cf_'), left_index=True, right_index=True, direction='backward')
    merged_df = pd.merge_asof(merged_df, edf.add_prefix('e_'), left_index=True, right_index=True, direction='backward')

    merged_df = merged_df.sort_index(ascending=True)
    merged_df = merged_df.apply(lambda col: col.ffill(), axis=0)

    # calculation
    merged_df = indicators_calculation(merged_df)

    merged_df.to_csv(f'C:\\Users\\barto\\Desktop\\Inwestor_2024\\analyze\\{ticker}_indicators.csv')

create_final_data_file(tickers)
