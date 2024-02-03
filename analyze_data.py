import numpy as np
import pandas as pd
import re
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

    def multiply_shares(mdf, mdate, multiplication):
        condition = mdf.index <= mdate
        mdf.loc[condition, 'commonStockSharesOutstanding'] *= multiplication
        return mdf

    def update_balance(df, ticker):
        if financial_statement == 'BALANCE_SHEET':
            if ticker == 'AAPL':
                df = multiply_shares(df, '2020-06-30', 4)
                df = multiply_shares(df, '2014-03-31', 5)
            if ticker == 'AMZN':
                df = multiply_shares(df, '2022-03-31', 20)
            if ticker == 'GOOGL':
                df = multiply_shares(df, '2022-03-31', 20)
            if ticker == 'JD':
                df = multiply_shares(df, '2021-03-31', 0.5)
            if ticker == 'NVDA':
                df = multiply_shares(df, '2021-05-02', 4)
            if ticker == 'TSLA':
                df = multiply_shares(df, '2022-06-30', 3)
                df = multiply_shares(df, '2020-06-30', 5)

        return df

    df = pd.read_csv(f'C:\\Users\\barto\\Desktop\\Inwestor_2024\\financial_statements\\{ticker}_{financial_statement}.csv', index_col=0).sort_index(ascending=True)
    df.index = pd.to_datetime(df.index)

    balance_not_summaring_cols = ['commonStockSharesOutstanding']
    df = update_balance(df, ticker)

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
    mdf.i_marketCapitalization = mdf.Adj_Close * mdf.b_commonStockSharesOutstanding

    # Margins
    mdf.i_grossMargin = mdf.is_grossProfit / mdf.is_totalRevenue
    mdf.i_EBITDAMargin = mdf.is_ebitda / mdf.is_totalRevenue
    mdf.i_EBITMargin = mdf.is_ebit / mdf.is_totalRevenue
    mdf.i_netMargin = mdf.is_netIncome / mdf.is_totalRevenue

    # Price indicators
    mdf.i_PS = mdf.i_marketCapitalization / mdf.is_totalRevenue
    mdf.i_PE = mdf.i_marketCapitalization / mdf.is_netIncome

    mdf = mdf.update_df_columns_from_class_attributes(mdf)
    return mdf.df


def create_final_data_file(mytickers):
    global folder_path

    def get_columns(df):
        base_columns = ['ticker', 'date']
        i_columns = [c for c in df.columns if 'i_' in c]
        is_columns = ['is_nonInterestIncome', 'is_operatingIncome', 'is_researchAndDevelopment', 'is_netIncome', 'b_commonStockSharesOutstanding']

        mycolumns = base_columns + is_columns + i_columns
        return mycolumns

    def rename_df_columns(df):
        renaming_columns = {}
        pattern_is_ = re.compile('^is_.*')
        pattern_b_ = re.compile('^b_.*')
        pattern_i_ = re.compile('^i_.*')
        for col in df.columns:
            changed_col = col
            changed_col = changed_col[3:] if pattern_is_.match(changed_col) else changed_col
            changed_col = changed_col[2:] if pattern_b_.match(changed_col) else changed_col
            changed_col = changed_col[2:] if pattern_i_.match(changed_col) else changed_col
            renaming_columns[col] = changed_col
        df = df.rename(columns=renaming_columns)
        return df

    dfs = []
    for tic in mytickers:
        try:
            file_path = f'{folder_path}analyze\\{tic}_indicators.csv'
            df = pd.read_csv(file_path, index_col=0)
            df['ticker'] = tic
            df['date'] = df.index
            indicator_columns = get_columns(df)
            df = df[indicator_columns]
            df = rename_df_columns(df)
            dfs.append(df)
        except FileNotFoundError:
            print('No file {tic}_indicators.csv')

    final_df = pd.concat(dfs, ignore_index=True)
    final_df['id'] = final_df['ticker'] + final_df['date'].astype(str)
    final_df.to_csv(f'{folder_path}final_data.csv', index=False)

    final_df2 = final_df.copy()
    final_df2.columns = [f'{c}2' for c in final_df2.columns]
    final_df2.to_csv(f'{folder_path}final_data2.csv', index=False)

    return final_df, final_df2


def prepare_functions_for_power_bi(cols, num):

    def change_data_type(cols):
        strs = []
        for col in cols:
            if col not in ['ticker', 'date']:
                strs.append(f'{{"{col}", type number}}')
        mystr = ', '.join(strs)
        print('-----------------------------------------------')
        print(mystr)
        print('-----------------------------------------------')

    def prepare_parameter_table_string(cols, num):
        row_strs = []
        for col in cols:
            if col not in ['ticker', 'date']:
                row_strs.append(f'ROW("ColumnName", "{col}")')
        row_str = ', '.join(row_strs)
        parameter_table_str = f'ParameterTable{num} =\nUNION(\n{row_str}\n)'
        print('-----------------------------------------------')
        print(parameter_table_str)
        print('-----------------------------------------------')

    def prepare_dynamicyaxismeasure(cols, num):
        row_strs = []
        for col in cols:
            if col not in [f'ticker{num}', f'date{num}', f'id{num}']:
                row_strs.append(f'"{col}", SUM(final_data{num}[{col}])')
        row_str = ', '.join(row_strs)
        dynamicyaxismeasure_str = f'DynamicYAxisMeasure{num} = SWITCH(\n[SelectedColumn{num}],\n{row_str},\nBLANK()\n)'
        print('-----------------------------------------------')
        print(dynamicyaxismeasure_str)
        print('-----------------------------------------------')

    change_data_type(cols)
    prepare_parameter_table_string(cols, num)
    prepare_dynamicyaxismeasure(cols, num)


folder_path = 'C:\\Users\\barto\\Desktop\\Inwestor_2024\\'
pandas_df_display_options()
update_df = pd.read_excel(f'{folder_path}update_notebook.xlsx')
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
    merged_df = merged_df.replace([np.inf, -np.inf], np.nan)

    merged_df.to_csv(f'C:\\Users\\barto\\Desktop\\Inwestor_2024\\analyze\\{ticker}_indicators.csv')

final_df, final_df2 = create_final_data_file(tickers)
prepare_functions_for_power_bi(final_df.columns, '')
prepare_functions_for_power_bi(final_df2.columns, 2)
