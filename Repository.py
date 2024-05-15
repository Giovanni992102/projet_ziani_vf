
import os
import pandas as pd
import yfinance as yf
import requests
import matplotlib.pyplot as plt
from matplotlib import ticker
import statsmodels.api as sm
import seaborn as sns
import numpy as np
from yfinance import tickers


# Définition des variables
# path_local_data = 'combined_data.csv'
class Repository:
    def __init__(self, titre_etudie, tickers_list, indice_ref, start_date, end_date):
        self.titre_etudie = titre_etudie
        self.tickers_list = tickers_list
        self.indice_ref = indice_ref
        self.start_date = start_date
        self.end_date = end_date

    # Télechargement des données
    def download_yf_data(self, tickers):
        data = {}
        for index, ticker in tickers.items():
            data[index] = yf.download(ticker, start=self.start_date, end=self.end_date)['Close']
        return data

    """def save_df_csv(df, file_name):
        # Define the file path and name
        file_path = os.path.join(os.getcwd(), file_name)

        # Save the DataFrame as a CSV file
        df.to_csv(file_path, index=True)

   def download_all_necessary_data(self):
        raw_data = self.download_yf_data(self.tickers, self.start_date, self.end_date)
        raw_titre_etudie = self.download_yf_data(self.titre_etudie, self.start_date, self.end_date)

        ref_index_df = pd.DataFrame(raw_data)

        combined_data = pd.concat([ref_index_df, pd.DataFrame(raw_titre_etudie)], axis=1)
        clean_combined_data = combined_data.dropna()
        return clean_combined_data"""

    def get_tax_data(self, ticker):
        net_income_data = yf.Ticker(ticker).financials.loc['Net Income', :]
        pretax_income_data = yf.Ticker(ticker).financials.loc['Pretax Income', :]
        # Extract Net Income and Pretax Income values for the most recent year
        net_income = net_income_data.iloc[1]
        pretax_income = pretax_income_data.iloc[1]
        return net_income, pretax_income

    def get_financials_data(self, ticker):
        stock = yf.Ticker(ticker)

        info = stock.info

        balance_sheet = stock.balance_sheet.T

        # Extract market cap and total debt values
        market_cap = info.get("marketCap", "Not Available")
        total_debt = balance_sheet.get("Total Debt", None)

        financials_tuple = (market_cap, total_debt)
        return financials_tuple

    def get_titre_etudie(self):
        return self.titre_etudie

    def get_tickers_list(self):
        return self.tickers_list

    def get_indice_ref(self):
        return self.indice_ref

    def get_start_date(self):
        return self.start_date

    def get_end_date(self):
        return self.end_date



