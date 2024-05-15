import numpy as np
import pandas as pd
import Repository
from sklearn.preprocessing import StandardScaler

# Calcul du Cout des capitaux propres par la méthode du CAPM
class Model:
    def __init__(self, repo, bond_10yr, face_value, coupon_rate, current_market_price, remaining_years_to_maturity):
        self.repo = repo
        self.bond_10yr = bond_10yr
        self.face_value = face_value
        self.coupon_rate = coupon_rate
        self.current_market_price = current_market_price
        self.remaining_years_to_maturity = remaining_years_to_maturity

    def compute_beta(self, df, titre, index_ref='MSCI ACWI', beta_window=160):
        titre_ret = df[titre].iloc[-beta_window:].pct_change().dropna()
        index_ret = df[index_ref].iloc[-beta_window:].pct_change().dropna()
        expected_market_return = index_ret.mean()
        annualized_expected_market_return = (1 + expected_market_return) ** 365 - 1

        x = index_ret
        y = titre_ret
        covariance = y.cov(x)
        market_variance = x.var()

        beta = covariance / market_variance
        result_tuple = (beta, expected_market_return, annualized_expected_market_return)
        return result_tuple

    # Download of risk free curve
    def get_days(self, bucket):
        if bucket[-1].lower() == 'm':
            base = 30
        elif bucket[-1].lower() == 'y':
            base = 360
        else:
            raise ValueError(f'wrong bucket format| bucket={bucket}')
        return int(bucket[: -1]) * base

    def get_marketwatch_curve(self, date, tickers):
        url = r'https://www.marketwatch.com/investing/bonds/{ticker}/downloaddatapartial?startdate={startdate}%2000:00:00&enddate={enddate}%2000:00:00&daterange={daterange}&frequency=p1d&csvdownload=true&downloadpartial=false&newdates=false&countrycode=bx'

        daterange = 'd30'

        dfs = []
        i = 0
        for bucket, ticker in tickers.items():
            i += 1
            url_ = url.format(ticker=ticker, startdate=date, enddate=date, daterange=daterange)
            df = pd.read_csv(url_)
            df['bucket'] = bucket
            df['days'] = self.get_days(bucket)
            dfs.append(df)

        result = pd.concat(dfs)
        result = result[['Date', 'bucket', 'days', 'Close']]
        result['Close'] = result['Close'].str[: -1].astype(float) / 100

        return result

    # Calculation of Cost of Equity
    def calculate_CE(self, beta_value, annualized_expected_return):
        cost_of_equity = self.bond_10yr + beta_value * (annualized_expected_return - self.bond_10yr)
        return cost_of_equity

    # Calculation of yield to maturity (YTM)
    def calculate_ytm(self):
        try:
            ytm = (self.coupon_rate * self.face_value + (self.face_value - self.current_market_price) / self.remaining_years_to_maturity) / (
                    (self.face_value + self.current_market_price) / 2)
            return ytm

        except ZeroDivisionError:
            raise ZeroDivisionError(
                f"Unable to calculate the Cost of Debt. The remaining_years_to_maturity must not be equal to 0")

    # income tax calculation
    def compute_tax_is(self, net_income, pretax_income):
        t_is = 1 - (net_income / pretax_income)
        return t_is

    def compute_WACC(self):
        raw_data = self.repo.download_yf_data(self.repo.get_tickers_list())
        ref_index_df = pd.DataFrame(raw_data)
        raw_titre_etudie = self.repo.download_yf_data(self.repo.get_titre_etudie())
        combined_data = pd.concat([ref_index_df, pd.DataFrame(raw_titre_etudie)], axis=1)
        clean_combined_data = combined_data.dropna()

        titre, = self.repo.get_titre_etudie().keys()

        result = self.compute_beta(clean_combined_data, titre)
        beta_value, expected_return, annualized_expected_return = result

        # Calculation of cost of equity using CAPM Formula
        cost_of_equity = self.calculate_CE(beta_value, annualized_expected_return)

        # Calculation of Cost of Debt
        cost_of_debt = self.calculate_ytm()

        # tax calculations
        net_income = 0
        pretax_income = 0
        for company, ticker in self.repo.get_titre_etudie().items():
            net_income, pretax_income = self.repo.get_tax_data(ticker)

        tax = self.compute_tax_is(net_income, pretax_income)

        # get info about market cap and debt
        market_cap = 0
        total_debt = 0
        for company, ticker in self.repo.get_titre_etudie().items():
            market_cap, total_debt = self.repo.get_financials_data(ticker)
            total_debt = total_debt.iloc[0]

        WACC = market_cap / (market_cap + total_debt) * cost_of_equity + total_debt / (
                market_cap + total_debt) * cost_of_debt / 100 * (1 - tax)
        return WACC



    def get_repo(self):
        return self.repo

    def get_10yr_bond(self):
        return self.bond_10yr

    def get_face_value(self):
        return self.face_value

    def get_coupon_rate(self):
        return self.coupon_rate

    def get_current_market_price(self):
        return self.current_market_price

    def get_remaining_years_to_maturity(self):
        return self.remaining_years_to_maturity
