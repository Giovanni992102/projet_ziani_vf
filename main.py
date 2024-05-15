import pandas as pd
import Repository
import Model
import toml as toml
import View

class Main:
    with open("config.toml", "r") as file:
        data = toml.load(file)
        print("Read successful")

    # Définition de la liste des indices
    tickers = {
        'STOXX': '^STOXX',
        'NASDAQ': '^IXIC',
        'SP500': '^GSPC',
        'FTSE': '^FTSE',
        'CAC40': '^FCHI',
        'FTSEMIB': 'FTSEMIB.MI',
        'MSCI': 'MSCI',
        'MSCI ACWI': 'ACWI',
    }

    tickers_rates_us = {'1m': 'tmubmusd01m',
                        '3m': 'tmubmusd03m',
                        '6m': 'tmubmusd06m',
                        '1y': 'tmubmusd01y',
                        '2y': 'tmubmusd02y',
                        '3y': 'tmubmusd03y',
                        '5y': 'tmubmusd05y',
                        '7y': 'tmubmusd07y',
                        '10y': 'tmubmusd10y',
                        '30y': 'tmubmusd30y'
                        }

    tickers_rates_fr = {'1m': 'tmbmbfr-01m',
                        '3m': 'tmbmbfr-03m',
                        '6m': 'tmbmbfr-06m',
                        '1y': 'tmbmbfr-01y',
                        '2y': 'tmbmkfr-02y',
                        '3y': 'tmbmkfr-03y',
                        '4y': 'tmbmkfr-04y',
                        '5y': 'tmbmkfr-05y',
                        '6y': 'tmbmkfr-06y',
                        '7y': 'tmbmkfr-07y',
                        '10y': 'tmbmkfr-10y',
                        '15y': 'tmbmkfr-15y',
                        '20y': 'tmbmkfr-20y',
                        '25y': 'tmbmkfr-25y',
                        '30y': 'tmbmkfr-30y'
                        }

    # Dates
    start_date = '2017-10-18'
    end_date = '2023-10-18'
    rf_rate_date = '01/12/2024'

    # name info
    title_name = data['title_name']
    title_abbr = data['title_abbr']
    titre_etude = {
        f'{title_name}': f'{title_abbr}',
    }

    # Information sur le bond du titre à étudier
    face_value = data['face_value']
    coupon_rate = data['coupon_rate']
    current_market_price = data['current_market_price']
    remaining_years_to_maturity = data['remaining_years_to_maturity']
    relevant_market = data['relevant_market']
    french_rf_10_close_value = data['french_rf_10_close_value']

    repo = Repository.Repository(titre_etude, tickers, relevant_market, start_date, end_date)

    model = Model.Model(repo, french_rf_10_close_value, face_value, coupon_rate, current_market_price, remaining_years_to_maturity)

    # rates_fr = Model.Model.get_marketwatch_curve(rf_rate_date, tickers_rates_fr)
    # french_risk_free_rates = pd.DataFrame(rates_fr)
    # french_rf_10 = french_risk_free_rates[french_risk_free_rates['bucket'] == '10y']
    # french_rf_10_close_value = french_rf_10['Close'].values[0]

    view = View.View(repo, model)
    view.print_WACC(title_name)
