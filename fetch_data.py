from datetime import datetime,timedelta,date
from typing import List
import pandas as pd
import json
import tables
from dateutil.relativedelta import relativedelta
from flask import Flask, render_template, request
import requests
import re

#Hey
#New branch work

from config import (
    SYMBOL_EQUITY_QUOTE_URL,
    SYMBOL_FUTURES_QUOTE_URL,
    SYMBOL_SUBSCRIPTION_URL,
    SYMBOLS,
)

app = Flask(__name__)


def is_float(string: str):
    pattern = r"^-?\d+(\.\d+)?$"
    return re.match(pattern, string) is not None

#! OG Code
# def subscribe_equity_symbols(symbols: List = SYMBOLS):

#     for symbol in symbols:
#         response = requests.get(
#             url=SYMBOL_SUBSCRIPTION_URL.format(stock_symbol=f"{symbol}EQ")
#         )
#         if (
#             not response.status_code == 200
#             or f"Subscription requested for dispname : {symbol}EQ"
#             != response.content.decode("utf-8")
#         ):
#             subscribe_equity_symbols(symbols=[symbol])
#         else:
#             print(f"{symbol} SUBSCRIBED SUCCESSFULLY")


# this is the chnanged code to resolve the recurssion error
def subscribe_equity_symbols(symbols: List = SYMBOLS):
    retry_dict = {symbol: 0 for symbol in symbols}  # Initialize retry count for each symbol

    for symbol in symbols:
        while retry_dict[symbol] < 5:  # Retry up to 5 times
            response = requests.get(
                url=SYMBOL_SUBSCRIPTION_URL.format(stock_symbol=f"{symbol}EQ")
            )
            if (
                response.status_code == 200
                and f"Subscription requested for dispname : {symbol}EQ" == response.content.decode("utf-8")
            ):
                print(f"{symbol} SUBSCRIBED SUCCESSFULLY")
                break  # Move to the next symbol if subscription is successful
            else:
                retry_dict[symbol] += 1
                print(f"Retry {retry_dict[symbol]} for {symbol}EQ")

        if retry_dict[symbol] >= 5:
            print(f"Subscription failed for {symbol}EQ after 5 attempts, moving to next symbol.")


# OG Code
# def subscribe_futures_symbols(symbols: List = SYMBOLS):

#     near_expiry = datetime.now().strftime('%y%b').upper()
#     mid_expiry = (datetime.now() + relativedelta(months=+1)).strftime('%y%b').upper()
#     far_expiry = (datetime.now() + relativedelta(months=+2)).strftime('%y%b').upper()
    
#     for expiry in [near_expiry,mid_expiry,far_expiry]:
#         for symbol in symbols:
#             print(f'stock_symbol : {symbol}{expiry}FUT')
#             response = requests.get(
#                 url=SYMBOL_SUBSCRIPTION_URL.format(stock_symbol=f"{symbol}{expiry}FUT")
#             )
#             if (
#                 not response.status_code == 200
#                 or f"Subscription requested for dispname : {symbol}{expiry}FUT"
#                 != response.content.decode("utf-8")
#             ):
#                 print(f'error in symbol : {symbol}')
#                 subscribe_futures_symbols(symbols=[symbol])
#             else:
#                 print(f"{symbol}{expiry}FUT SUBSCRIBED SUCCESSFULLY")


# this is the chnanged code to resolve the recurssion error
def subscribe_futures_symbols(symbols: List = SYMBOLS):
    retry_dict = {symbol: 0 for symbol in symbols}  # Initialize retry count for each symbol

    near_expiry = datetime.now().strftime('%y%b').upper()
    mid_expiry = (datetime.now() + relativedelta(months=+1)).strftime('%y%b').upper()
    far_expiry = (datetime.now() + relativedelta(months=+2)).strftime('%y%b').upper()

    for expiry in [near_expiry, mid_expiry, far_expiry]:
        for symbol in symbols:
            while retry_dict[symbol] < 5:  # Retry up to 5 times
                print(f'Subscribing: stock_symbol : {symbol}{expiry}FUT')
                response = requests.get(
                    url=SYMBOL_SUBSCRIPTION_URL.format(stock_symbol=f"{symbol}{expiry}FUT")
                )
                if (
                    response.status_code == 200
                    and f"Subscription requested for dispname : {symbol}{expiry}FUT" == response.content.decode("utf-8")
                ):
                    print(f"{symbol}{expiry}FUT SUBSCRIBED SUCCESSFULLY")
                    break  # Move to the next symbol if subscription is successful
                else:
                    retry_dict[symbol] += 1
                    print(f"Retry {retry_dict[symbol]} for {symbol}{expiry}FUT")

            if retry_dict[symbol] >= 5:
                print(f"Subscription failed for {symbol}{expiry}FUT after 5 attempts, moving to next symbol.")




def fetch_equity_data(symbol: str):
    response = requests.get(url=SYMBOL_EQUITY_QUOTE_URL.format(stock_symbol=symbol))
    if not response.status_code == 200:
        raise Exception("Error in request")

    content = {}
    for data in response.content.decode("utf-8").split("\r\n"):
        if not data:
            continue
        key, value = data.split("=")
        content[key] = float(value) if is_float(value) else value
    return content


def fetch_futures_data(symbol: str,expiry):

    # expiry = datetime.now().strftime('%y%b').upper()  # Nearest expiry

    # if expiry == 'near':
    #     expiry = datetime.now().strftime('%y%b').upper()
    # elif expiry == 'mid':
    #     expiry = (datetime.now() + relativedelta(months=+1)).strftime('%y%b').upper()
    # elif expiry == 'far':
    #     expiry = (datetime.now() + relativedelta(months=+2)).strftime('%y%b').upper()

    if expiry == 'near':
        expiry = (datetime.now() + relativedelta(months=+1)).strftime('%y%b').upper()
    elif expiry == 'mid':
        expiry = (datetime.now() + relativedelta(months=+2)).strftime('%y%b').upper()
    elif expiry == 'far':
        expiry = (datetime.now() + relativedelta(months=+3)).strftime('%y%b').upper()

    response = requests.get(
        url=SYMBOL_FUTURES_QUOTE_URL.format(stock_symbol=symbol, expiry=expiry)
    )
    if not response.status_code == 200:
        raise Exception("Error in request")

    content = {}
    for data in response.content.decode("utf-8").split("\r\n"):
        if not data:
            continue
        key, value = data.split("=")
        content[key] = float(value) if is_float(value) else value
    return content


# def fetch_symbol_data(symbol: str,dict_symbol_lotsize,expiry,no_of_days_left):
def fetch_symbol_data(symbol: str, dict_symbol_lotsize, expiry, no_of_days_left, open_factor):
    equity_data = fetch_equity_data(symbol=symbol)
    futures_data = fetch_futures_data(symbol,expiry)

    # lot ,  script,  open , close , intra open , intra close , delv open , delv close , return open  return close, round intra exp , round delv exp , exp detasil

    data = {}

    data['LOT_SIZE'] = dict_symbol_lotsize[symbol]

    data['SYMBOL'] = symbol

    #! Cash & Fut Bid & Ask
    data['CASH_BID'] = equity_data["bidp1"]
    data['CASH_ASK'] = equity_data["askp1"]
    data['FUT_BID'] = futures_data["bidp1"]
    data['FUT_ASK'] = futures_data["askp1"]

    #! Expense Details.
    data["CASH_INTRA_BUY_EXP"] = round((data["CASH_ASK"]*800/10000000),2)
    data["CASH_INTRA_SELL_EXP"] = round((data["CASH_BID"]*3000/10000000),2)

    data["CASH_DLV_BUY_EXP"] = round((data["CASH_ASK"]*12000/10000000),2)
    data["CASH_DLV_SELL_EXP"] = round((data["CASH_BID"]*10500/10000000),2)

    data["FUTURE_BUY_EXP"] = round((data["FUT_ASK"]*550/10000000),2)
    data["FUTURE_SELL_EXP"] = round((data["FUT_BID"]*1600/10000000),2)

    #! Open & Close
    data["CNN_OPEN"] = "{:.2f}".format(data["FUT_BID"] - data["CASH_ASK"])
    data["CNN_CLOSE"] = "{:.2f}".format(data["CASH_BID"] - data["FUT_ASK"])

    data['INTRA_OPEN'] = round((-(data["CASH_ASK"]) + data["FUT_BID"] - data["CASH_INTRA_BUY_EXP"] - data["FUTURE_SELL_EXP"])*data['LOT_SIZE'],2)
    data['INTRA_CLOSE'] = round((data["CASH_BID"] - data["FUT_ASK"] - data["CASH_INTRA_SELL_EXP"] - data["FUTURE_BUY_EXP"])*data['LOT_SIZE'],2)

    data['DLV_OPEN'] = round((-(data["CASH_ASK"]) + data["FUT_BID"] - data["CASH_DLV_BUY_EXP"] - data["FUTURE_SELL_EXP"])*data['LOT_SIZE'],2)
    data['DLV_CLOSE'] = round((data["CASH_BID"] - data["FUT_ASK"] - data["CASH_DLV_SELL_EXP"] - data["FUTURE_BUY_EXP"])*data['LOT_SIZE'],2)

    #! Margin
    margin = equity_data['ltp'] * 1.2 * data['LOT_SIZE']

    # data['OPEN_PROFIT'] = round(data['DLV_OPEN']*data['LOT_SIZE'],2)
    # data['CLOSE_PROFIT'] = round(data['DLV_CLOSE']*data['LOT_SIZE'],2)

    #! Relative Return 
    data['RLT_RETURN_OPEN'] = round(((data['DLV_OPEN']*100 / margin)/no_of_days_left)*365,2)
    data['RLT_RETURN_CLOSE'] = round(((data['DLV_CLOSE']*100 / margin)/no_of_days_left)*365,2)

    #! Round Expense
    data['INTRA_ROUND_EXP'] = round(data["CASH_INTRA_BUY_EXP"] + data["CASH_INTRA_SELL_EXP"] + data["FUTURE_BUY_EXP"] + data["FUTURE_SELL_EXP"],2)
    data['DLV_ROUND_EXP'] = round(data["CASH_DLV_BUY_EXP"] + data["CASH_DLV_SELL_EXP"] + data["FUTURE_BUY_EXP"] + data["FUTURE_SELL_EXP"],2)

    expenses = {
            'CASH_INTRA_BUY_EXP': data['CASH_INTRA_BUY_EXP'],
            'CASH_INTRA_SELL_EXP': data['CASH_INTRA_SELL_EXP'],
            'CASH_DLV_BUY_EXP': data['CASH_DLV_BUY_EXP'],
            'CASH_DLV_SELL_EXP': data['CASH_DLV_SELL_EXP'],
            'FUTURE_BUY_EXP': data['FUTURE_BUY_EXP'],
            'FUTURE_SELL_EXP': data['FUTURE_SELL_EXP'],
            }

    # Remove the original keys from the dictionary
    del data['CASH_INTRA_BUY_EXP'], data['CASH_INTRA_SELL_EXP'], data['CASH_DLV_BUY_EXP'], data['CASH_DLV_SELL_EXP'], data['FUTURE_BUY_EXP'], data['FUTURE_SELL_EXP']

    # Update the dictionary by adding these keys at the end
    data.update(expenses)

    #! M_parity & Parity
    # open_factor = 0.08
    data['M_PARITY'] = round((equity_data['ltp']*data['LOT_SIZE']*open_factor/100) + data['DLV_OPEN']*data['LOT_SIZE'],2)
    data['PARITY'] = round((equity_data['ltp']*open_factor/100) + data['DLV_OPEN'],2)

    return data


#######################! Main !#######################

subscribe_equity_symbols()
subscribe_futures_symbols()

tables.update_index_html()

# Load the dictionary from the JSON file
with open('dict_symbol_lotsize.json', 'r') as f:
    dict_symbol_lotsize = json.load(f)


####################! MAIN !####################

#! Selection based on user

today, near_expiry, mid_expiry, far_expiry = tables.expiries()


# def fetch_all_stocks_data(expiry,no_of_days_left):
#     return [fetch_symbol_data(symbol, dict_symbol_lotsize, expiry,no_of_days_left) for symbol in SYMBOLS]

def fetch_all_stocks_data(expiry, no_of_days_left, open_factor):
    return [fetch_symbol_data(symbol, dict_symbol_lotsize, expiry, no_of_days_left, open_factor) for symbol in SYMBOLS]


# @app.route('/', methods=['GET', 'POST'])
# def index():
#     expiry = None
#     if request.method == 'POST':
#         exp = request.form.get('expiry')
        
#         # Determine expiry date based on selection
#         if exp == 'near':
#             expiry = datetime.now().strftime('%y%b').upper()
#             exp_date = near_expiry
#         elif exp == 'mid':
#             expiry = (datetime.now() + relativedelta(months=+1)).strftime('%y%b').upper()
#             exp_date = mid_expiry
#         elif exp == 'far':
#             expiry = (datetime.now() + relativedelta(months=+2)).strftime('%y%b').upper()
#             exp_date = far_expiry
        
#         # Number of days left
#         exp_date_dt = datetime.strptime(exp_date, '%d-%m-%Y')
#         today_date = datetime.today()
#         no_of_days_left = (exp_date_dt-today_date).days
#         print(f'no_of_days_left : {no_of_days_left}')
        
#         # Fetch data using the selected expiry
#         stocks_data = fetch_all_stocks_data(expiry,no_of_days_left)
#         print(f'stocks_data : {stocks_data}')
        
#         return render_template('index.html', stocks_data=stocks_data, expiry=expiry)

config_data = {
    "api_urls": {
        "equity_quote": SYMBOL_EQUITY_QUOTE_URL,
        "futures_quote": SYMBOL_FUTURES_QUOTE_URL,
        "subscription": SYMBOL_SUBSCRIPTION_URL
    },
    "symbols": SYMBOLS,
    "expiry_details": {
        "near": datetime.now().strftime('%y%b').upper(),
        "mid": (datetime.now() + relativedelta(months=+1)).strftime('%y%b').upper(),
        "far": (datetime.now() + relativedelta(months=+2)).strftime('%y%b').upper()
    }
}

if __name__ == '__main__':
    app.run(debug=True)