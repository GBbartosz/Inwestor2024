class MergedDfRead:
    def __init__(self, df):
        self.df = df

        self.Open = self.df['Open']
        self.High = self.df['High']
        self.Low = self.df['Low']
        self.Close = self.df['Close']
        self.Adj_Close = self.df['Adj_Close']
        self.Volume = self.df['Volume']

        # INCOME STATEMENT
        self.is_reportedCurrency = self.df['is_reportedCurrency']
        self.is_grossProfit = self.df['is_grossProfit']
        self.is_totalRevenue = self.df['is_totalRevenue']
        self.is_costOfRevenue = self.df['is_costOfRevenue']
        self.is_costofGoodsAndServicesSold = self.df['is_costofGoodsAndServicesSold']
        self.is_operatingIncome = self.df['is_operatingIncome']
        self.is_sellingGeneralAndAdministrative = self.df['is_sellingGeneralAndAdministrative']
        self.is_researchAndDevelopment = self.df['is_researchAndDevelopment']
        self.is_operatingExpenses = self.df['is_operatingExpenses']
        self.is_investmentIncomeNet = self.df['is_investmentIncomeNet']
        self.is_netInterestIncome = self.df['is_netInterestIncome']
        self.is_interestIncome = self.df['is_interestIncome']
        self.is_interestExpense = self.df['is_interestExpense']
        self.is_nonInterestIncome = self.df['is_nonInterestIncome']
        self.is_otherNonOperatingIncome = self.df['is_otherNonOperatingIncome']
        self.is_depreciation = self.df['is_depreciation']
        self.is_depreciationAndAmortization = self.df['is_depreciationAndAmortization']
        self.is_incomeBeforeTax = self.df['is_incomeBeforeTax']
        self.is_incomeTaxExpense = self.df['is_incomeTaxExpense']
        self.is_interestAndDebtExpense = self.df['is_interestAndDebtExpense']
        self.is_netIncomeFromContinuingOperations = self.df['is_netIncomeFromContinuingOperations']
        self.is_comprehensiveIncomeNetOfTax = self.df['is_comprehensiveIncomeNetOfTax']
        self.is_ebit = self.df['is_ebit']
        self.is_ebitda = self.df['is_ebitda']
        self.is_netIncome = self.df['is_netIncome']

        self.is_i_revenue_growth_1y = self.df['is_i_revenue_growth_1y']
        self.is_i_revenue_growth_2y = self.df['is_i_revenue_growth_2y']
        self.is_i_revenue_growth_3y = self.df['is_i_revenue_growth_3y']
        self.is_i_revenue_growth_4y = self.df['is_i_revenue_growth_4y']

        # BALANCE SHEET
        self.b_reportedCurrency = self.df['b_reportedCurrency']
        self.b_totalAssets = self.df['b_totalAssets']
        self.b_totalCurrentAssets = self.df['b_totalCurrentAssets']
        self.b_cashAndCashEquivalentsAtCarryingValue = self.df['b_cashAndCashEquivalentsAtCarryingValue']
        self.b_cashAndShortTermInvestments = self.df['b_cashAndShortTermInvestments']
        self.b_inventory = self.df['b_inventory']
        self.b_currentNetReceivables = self.df['b_currentNetReceivables']
        self.b_totalNonCurrentAssets = self.df['b_totalNonCurrentAssets']
        self.b_propertyPlantEquipment = self.df['b_propertyPlantEquipment']
        self.b_accumulatedDepreciationAmortizationPPE = self.df['b_accumulatedDepreciationAmortizationPPE']
        self.b_intangibleAssets = self.df['b_intangibleAssets']
        self.b_intangibleAssetsExcludingGoodwill = self.df['b_intangibleAssetsExcludingGoodwill']
        self.b_goodwill = self.df['b_goodwill']
        self.b_investments = self.df['b_investments']
        self.b_longTermInvestments = self.df['b_longTermInvestments']
        self.b_shortTermInvestments = self.df['b_shortTermInvestments']
        self.b_otherCurrentAssets = self.df['b_otherCurrentAssets']
        self.b_otherNonCurrentAssets = self.df['b_otherNonCurrentAssets']
        self.b_totalLiabilities = self.df['b_totalLiabilities']
        self.b_totalCurrentLiabilities = self.df['b_totalCurrentLiabilities']
        self.b_currentAccountsPayable = self.df['b_currentAccountsPayable']
        self.b_deferredRevenue = self.df['b_deferredRevenue']
        self.b_currentDebt = self.df['b_currentDebt']
        self.b_shortTermDebt = self.df['b_shortTermDebt']
        self.b_totalNonCurrentLiabilities = self.df['b_totalNonCurrentLiabilities']
        self.b_capitalLeaseObligations = self.df['b_capitalLeaseObligations']
        self.b_longTermDebt = self.df['b_longTermDebt']
        self.b_currentLongTermDebt = self.df['b_currentLongTermDebt']
        self.b_longTermDebtNoncurrent = self.df['b_longTermDebtNoncurrent']
        self.b_shortLongTermDebtTotal = self.df['b_shortLongTermDebtTotal']
        self.b_otherCurrentLiabilities = self.df['b_otherCurrentLiabilities']
        self.b_otherNonCurrentLiabilities = self.df['b_otherNonCurrentLiabilities']
        self.b_totalShareholderEquity = self.df['b_totalShareholderEquity']
        self.b_treasuryStock = self.df['b_treasuryStock']
        self.b_retainedEarnings = self.df['b_retainedEarnings']
        self.b_commonStock = self.df['b_commonStock']
        self.b_commonStockSharesOutstanding = self.df['b_commonStockSharesOutstanding']

        # CASH FLOW
        self.cf_reportedCurrency = self.df['cf_reportedCurrency']
        self.cf_operatingCashflow = self.df['cf_operatingCashflow']
        self.cf_paymentsForOperatingActivities = self.df['cf_paymentsForOperatingActivities']
        self.cf_proceedsFromOperatingActivities = self.df['cf_proceedsFromOperatingActivities']
        self.cf_changeInOperatingLiabilities = self.df['cf_changeInOperatingLiabilities']
        self.cf_changeInOperatingAssets = self.df['cf_changeInOperatingAssets']
        self.cf_depreciationDepletionAndAmortization = self.df['cf_depreciationDepletionAndAmortization']
        self.cf_capitalExpenditures = self.df['cf_capitalExpenditures']
        self.cf_changeInReceivables = self.df['cf_changeInReceivables']
        self.cf_changeInInventory = self.df['cf_changeInInventory']
        self.cf_profitLoss = self.df['cf_profitLoss']
        self.cf_cashflowFromInvestment = self.df['cf_cashflowFromInvestment']
        self.cf_cashflowFromFinancing = self.df['cf_cashflowFromFinancing']
        self.cf_proceedsFromRepaymentsOfShortTermDebt = self.df['cf_proceedsFromRepaymentsOfShortTermDebt']
        self.cf_paymentsForRepurchaseOfCommonStock = self.df['cf_paymentsForRepurchaseOfCommonStock']
        self.cf_paymentsForRepurchaseOfEquity = self.df['cf_paymentsForRepurchaseOfEquity']
        self.cf_paymentsForRepurchaseOfPreferredStock = self.df['cf_paymentsForRepurchaseOfPreferredStock']
        self.cf_dividendPayout = self.df['cf_dividendPayout']
        self.cf_dividendPayoutCommonStock = self.df['cf_dividendPayoutCommonStock']
        self.cf_dividendPayoutPreferredStock = self.df['cf_dividendPayoutPreferredStock']
        self.cf_proceedsFromIssuanceOfCommonStock = self.df['cf_proceedsFromIssuanceOfCommonStock']
        self.cf_proceedsFromIssuanceOfLongTermDebtAndCapitalSecuritiesNet = self.df['cf_proceedsFromIssuanceOfLongTermDebtAndCapitalSecuritiesNet']
        self.cf_proceedsFromIssuanceOfPreferredStock = self.df['cf_proceedsFromIssuanceOfPreferredStock']
        self.cf_proceedsFromRepurchaseOfEquity = self.df['cf_proceedsFromRepurchaseOfEquity']
        self.cf_proceedsFromSaleOfTreasuryStock = self.df['cf_proceedsFromSaleOfTreasuryStock']
        self.cf_changeInCashAndCashEquivalents = self.df['cf_changeInCashAndCashEquivalents']
        self.cf_changeInExchangeRate = self.df['cf_changeInExchangeRate']
        self.cf_netIncome = self.df['cf_netIncome']

        # EARNINGS
        self.e_reportedDate = self.df['e_reportedDate']
        self.e_reportedEPS = self.df['e_reportedEPS']
        self.e_estimatedEPS = self.df['e_estimatedEPS']
        self.e_surprise = self.df['e_surprise']
        self.e_surprisePercentage = self.df['e_surprisePercentage']
        self.e_EPS = self.df['e_EPS']

        # INDICATORS
        self.shares = None
        self.marketCapitalization = None
        self.PS = None
        self.PE = None

    def update_df_columns_from_class_attributes(self, this_class_instance):
        # giving back attribute values to df
        for attribute in dir(this_class_instance):
            if '__' not in attribute and attribute not in ['df', 'update_df_columns_from_class_attributes']:
                print(attribute)
                this_class_instance.df[attribute] = getattr(self, attribute)
        return this_class_instance
