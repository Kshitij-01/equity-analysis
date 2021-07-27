from datetime import date

from django.db import models


# Create your models here.


class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=100, default='-')
    dob = models.DateField(default=date.today)
    Username = models.CharField(max_length=20, default='-', primary_key=True)
    password = models.CharField(max_length=60, default='-')


class Company(models.Model):
    symbol = models.CharField(primary_key=True, max_length=20, default='unavailable')
    company_name = models.CharField(max_length=100, default='-')
    logo = models.TextField(default="No logo")
    description = models.TextField(default='no info')
    description_wiki = models.TextField(default='no info')
    financial_report = models.TextField(default='no info')


class income_ticker(models.Model):
    symbol = models.CharField(max_length=15, default='unavailable')
    Financial_Year = models.CharField(max_length=100, default='-')
    Total_Revenue = models.CharField(max_length=100, default='-')
    Raw_Materials = models.CharField(max_length=100, default='-')
    Power_and_Fuel_Cost = models.CharField(max_length=100, default='-')
    Employee_Cost = models.CharField(max_length=100, default='-')
    Selling_and_Administrative_Expenses = models.CharField(max_length=100, default='-')
    Operating_and_Other_expenses = models.CharField(max_length=100, default='-')
    EBITDA = models.CharField(max_length=100, default='-')
    DepreciationAmortization = models.CharField(max_length=100, default='-')
    PBIT = models.CharField(max_length=100, default='-')
    Interest_and_Other_Items = models.CharField(max_length=100, default='-')
    PBT = models.CharField(max_length=100, default='-')
    Taxes_and_Other_Items = models.CharField(max_length=100, default='-')
    Net_Income = models.CharField(max_length=100, default='-')
    EPS = models.CharField(max_length=100, default='-')
    DPS = models.CharField(max_length=100, default='-')
    Payout_ratio = models.CharField(max_length=100, default='-')


class balance_sheet_ticker(models.Model):
    symbol = models.CharField(max_length=15, default='unavailable')
    Financial_Year = models.CharField(max_length=100, default='-')
    Cash_and_Short_Term_Investments = models.CharField(max_length=100, default='-')
    Total_Receivables = models.CharField(max_length=100, default='-')
    Total_Inventory = models.CharField(max_length=100, default='-')
    Other_Current_Assets = models.CharField(max_length=100, default='-')
    Current_Assets = models.CharField(max_length=100, default='-')
    Loans_and_Advances = models.CharField(max_length=100, default='-')
    Net_PropertyPlantEquipment = models.CharField(max_length=100, default='-')
    Goodwill_and_Intangibles = models.CharField(max_length=100, default='-')
    Long_Term_Investments = models.CharField(max_length=100, default='-')
    Deferred_Tax_Assets_Net = models.CharField(max_length=100, default='-')
    Other_Assets = models.CharField(max_length=100, default='-')
    Non_Current_Assets = models.CharField(max_length=100, default='-')
    Total_Assets = models.CharField(max_length=100, default='-')
    Accounts_Payable = models.CharField(max_length=100, default='-')
    Total_Deposits = models.CharField(max_length=100, default='-')
    Other_Current_Liabilities = models.CharField(max_length=100, default='-')
    Current_Liabilities = models.CharField(max_length=100, default='-')
    Total_Long_Term_Debt = models.CharField(max_length=100, default='-')
    Deferred_Tax_Liabilities_Net = models.CharField(max_length=100, default='-')
    Other_Liabilities = models.CharField(max_length=100, default='-')
    Non_Current_Liabilities = models.CharField(max_length=100, default='-')
    Total_Liabilities = models.CharField(max_length=100, default='-')
    Common_Stock = models.CharField(max_length=100, default='-')
    Additional_Paid_in_Capital = models.CharField(max_length=100, default='-')
    Reserves_and_Surplus = models.CharField(max_length=100, default='-')
    Minority_Interest = models.CharField(max_length=100, default='-')
    Other_Equity = models.CharField(max_length=100, default='-')
    Total_Equity = models.CharField(max_length=100, default='-')
    Total_Liabilities_and_Shareholders_Equity = models.CharField(max_length=100, default='-')
    Total_Common_Shares_Outstanding = models.CharField(max_length=100, default='-')


class cashflow_ticker(models.Model):
    symbol = models.CharField(max_length=15, default='unavailable')
    Financial_Year = models.CharField(max_length=100, default='-')
    Cash_from_Operating_Activities = models.CharField(max_length=100, default='-')
    Cash_from_Investing_Activities = models.CharField(max_length=100, default='-')
    Cash_from_Financing_Activities = models.CharField(max_length=100, default='-')
    Net_Change_in_Cash = models.CharField(max_length=100, default='-')
    Changes_in_Working_Capital = models.CharField(max_length=100, default='-')
    Capital_Expenditures = models.CharField(max_length=100, default='-')
    Free_Cash_Flow = models.CharField(max_length=100, default='-')


class peers_ticker(models.Model):
    symbol = models.CharField(max_length=15, default='unavailable')
    Stock = models.CharField(max_length=100, default='-')
    Asian_Paints_Ltd = models.CharField(max_length=100, default='-')
    Berger_Paints_India_Ltd = models.CharField(max_length=100, default='-')
    Kansai_Nerolac_Paints_Ltd = models.CharField(max_length=100, default='-')
    Indigo_Paints_Ltd = models.CharField(max_length=100, default='-')


class Financial_Indicators_stockedge(models.Model):
    symbol = models.CharField(max_length=15, default='unavailable')
    Fundamental = models.CharField(max_length=100, default='-')
    Price = models.CharField(max_length=100, default='-')
    Market_Cap = models.CharField(max_length=100, default='-')
    Earnings_per_share_EPS = models.CharField(max_length=100, default='-')
    Price_Earning_Ratio_PE = models.CharField(max_length=100, default='-')
    Industry_PE = models.CharField(max_length=100, default='-')
    Book_Value_Share = models.CharField(max_length=100, default='-')
    Price_to_Book_Value = models.CharField(max_length=100, default='-')
    Dividend_Yield = models.CharField(max_length=100, default='-')
    No_of_Shares_Subscribed = models.CharField(max_length=100, default='-')
    FaceValue = models.CharField(max_length=100, default='-')
    Website = models.CharField(max_length=100, default='-')


class Overview_stockedge(models.Model):
    symbol = models.CharField(max_length=15, default='unavailable')
    Fundamental = models.CharField(max_length=100, default='-')
    Sector = models.CharField(max_length=100, default='-')
    Industry = models.CharField(max_length=100, default='-')
    Website = models.CharField(max_length=100, default='-')


class Balance_sheet_stockedge(models.Model):
    symbol = models.CharField(max_length=15, default='unavailable')
    Financials = models.CharField(max_length=100, default='-')
    Particulars = models.CharField(max_length=200,default='-')
    Shh_Funds = models.CharField(max_length=100, default='-')
    Non_Curr_Liab = models.CharField(max_length=100, default='-')
    Curr_Liab = models.CharField(max_length=100, default='-')
    Minority_Int = models.CharField(max_length=100, default='-')
    Equity_and_Liab = models.CharField(max_length=100, default='-')
    Non_Curr_Assets = models.CharField(max_length=100, default='-')
    Curr_Assets = models.CharField(max_length=100, default='-')
    Misc_Exp_not_WO = models.CharField(max_length=100, default='-')
    Total_Assets = models.CharField(max_length=100, default='-')
    Website = models.CharField(max_length=100, default='-')


class Profit_and_Loss_stockedge(models.Model):
    symbol = models.CharField(max_length=15, default='unavailable')
    Financials = models.CharField(max_length=100, default='-')
    Particulars = models.CharField(max_length=100, default='-')
    Net_Sales = models.CharField(max_length=100, default='-')
    Other_Income = models.CharField(max_length=100, default='-')
    Total_Income = models.CharField(max_length=100, default='-')
    Total_Expenditure = models.CharField(max_length=100, default='-')
    PBIDT = models.CharField(max_length=100, default='-')
    Interest = models.CharField(max_length=100, default='-')
    Depreciation = models.CharField(max_length=100, default='-')
    Taxation = models.CharField(max_length=100, default='-')
    Exceptional_Items = models.CharField(max_length=100, default='-')
    PAT = models.CharField(max_length=100, default='-')
    Website = models.CharField(max_length=100, default='-')


class Cash_Flow_stockedge(models.Model):
    symbol = models.CharField(max_length=15, default='unavailable')
    Financials = models.CharField(max_length=100, default='-')
    Particulars = models.CharField(max_length=1100,default='-')
    Cash_Fr_Operatn = models.CharField(max_length=100, default='-')
    Cash_Fr_Inv = models.CharField(max_length=100, default='-')
    Cash_Fr_Finan = models.CharField(max_length=100, default='-')
    Net_Change = models.CharField(max_length=100, default='-')
    Cash_and_Cash_Eqvt = models.CharField(max_length=100, default='-')
    Website = models.CharField(max_length=100, default='-')


class Pattern_stockedge(models.Model):
    symbol = models.CharField(max_length=15, default='unavailable')
    Shareholding = models.CharField(max_length=100, default='-')
    Qtrs = models.CharField(max_length=200)
    Promoter = models.CharField(max_length=100, default='-')
    Public = models.CharField(max_length=100, default='-')
    FIIFPI = models.CharField(max_length=100, default='-')
    DII = models.CharField(max_length=100, default='-')
    Non_Institution = models.CharField(max_length=100, default='-')
    Depository_Receipts = models.CharField(max_length=100, default='-')
    Promoter_Holding_Pledge = models.CharField(max_length=100, default='-')
