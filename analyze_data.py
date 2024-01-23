import pandas as pd


# dodac shares_outstanding z overview -- zamiast tego EARNINGS i wyliczyc z EPS

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
    for col in df.columns:
        if col != 'reportedCurrency':
            df[col] = df[col].rolling(window=4, min_periods=4).sum()  # summaring quarters to years
    df = df.iloc[3:, :]
    return df


def calculation_income_statement(df):
    # revenue growth
    df['i_revenue_growth_1y'] = df['totalRevenue'] / df['totalRevenue'].shift(1*4)
    df['i_revenue_growth_2y'] = df['totalRevenue'] / df['totalRevenue'].shift(2*4)
    df['i_revenue_growth_3y'] = df['totalRevenue'] / df['totalRevenue'].shift(3*4)
    df['i_revenue_growth_4y'] = df['totalRevenue'] / df['totalRevenue'].shift(4*4)
    return df

pandas_df_display_options()
update_df = pd.read_excel('C:\\Users\\barto\\Desktop\\Inwestor_2024\\update_notebook.xlsx')
update_df = update_df[update_df['last_update_date'].notna()]
tickers = update_df['ticker']
#tickers = ['META']
for ticker in tickers:
    isdf = read_financial_statement('INCOME_STATEMENT', ticker)
    bdf = read_financial_statement('BALANCE_SHEET', ticker)
    cfdf = read_financial_statement('CASH_FLOW', ticker)

    odf = pd.read_csv(f'C:\\Users\\barto\\Desktop\\Inwestor_2024\\financial_statements\\{ticker}_OVERVIEW.csv')

    pdf = pd.read_csv(f'C:\\Users\\barto\\Desktop\\Inwestor_2024\\price\\{ticker}_price.csv', index_col=0).sort_index(ascending=True)
    pdf.index = pd.to_datetime(pdf.index)

    pdf = pdf[pdf.index >= min(isdf.index)]

    isdf = calculation_income_statement(isdf)
    print(isdf[['totalRevenue', 'i_revenue_growth_1y', 'i_revenue_growth_2y', 'i_revenue_growth_3y', 'i_revenue_growth_4y']])


    merged_df = pd.merge_asof(pdf, isdf.add_prefix('is_'), left_index=True, right_index=True, direction='backward')
    merged_df = pd.merge_asof(merged_df, bdf.add_prefix('b_'), left_index=True, right_index=True, direction='backward')
    merged_df = pd.merge_asof(merged_df, cfdf.add_prefix('cf_'), left_index=True, right_index=True, direction='backward')

    merged_df = merged_df.sort_index(ascending=True)
    merged_df = merged_df.apply(lambda col: col.ffill(), axis=0)

    #print(merged_df.head())



    merged_df.to_csv(f'C:\\Users\\barto\\Desktop\\Inwestor_2024\\analyze\\{ticker}_indicators.csv')
