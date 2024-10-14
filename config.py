from datetime import datetime

SYMBOLS = [
    'AARTIIND',
    'ABB',
    'ABBOTINDIA',
    'ABCAPITAL',
    'ABFRL',
    'ACC',
    'ADANIENT',
    'ADANIPORTS',
    'ALKEM',
    'AMBUJACEM',
    'APOLLOHOSP',
    'APOLLOTYRE',
    'ASHOKLEY',
    'ASIANPAINT',
    'ASTRAL',
    'ATUL',
    'AUBANK',
    'AUROPHARMA',
    'AXISBANK',
    'BAJAJFINSV',
    'BAJFINANCE',
    'BALKRISIND',
    'BANDHANBNK',
    'BANKBARODA',
    'BATAINDIA',
    'BEL',
    'BERGEPAINT',
    'BHARATFORG',
    'BHARTIARTL',
    'BHEL',
    'BIOCON',
    'BOSCHLTD',
    'BPCL',
    'BRITANNIA',
    'CANBK',
    'CANFINHOME',
    'CHAMBLFERT',
    'CHOLAFIN',
    'CIPLA',
    'COALINDIA',
    'COFORGE',
    'COLPAL',
    'CONCOR',
    'COROMANDEL',
    'CROMPTON',
    'CUB',
    'CUMMINSIND',
    'DABUR',
    'DALBHARAT',
    'DEEPAKNTR',
    'DIVISLAB',
    'DIXON',
    'DLF',
    'DRREDDY',
    'EICHERMOT',
    'ESCORTS',
    'EXIDEIND',
    'FEDERALBNK',
    'GAIL',
    'GLENMARK',
    'GMRINFRA',
    'GNFC',
    'GODREJCP',
    'GODREJPROP',
    'GRANULES',
    'GRASIM',
    'GUJGASLTD',
    'HAL',
    'HAVELLS',
    'HCLTECH',
    'HDFCAMC',
    'HDFCBANK',
    'HDFCLIFE',
    'HEROMOTOCO',
    'HINDALCO',
    'HINDCOPPER',
    'HINDPETRO',
    'HINDUNILVR',
    'ICICIBANK',
    'ICICIGI',
    'ICICIPRULI',
    'IDEA',
    'IDFC',
    'IDFCFIRSTB',
    'IEX',
    'IGL',
    'INDHOTEL',
    'INDIAMART',
    'INDIGO',
    'INDUSINDBK',
    'INDUSTOWER',
    'INFY',
    'IOC',
    'IPCALAB',
    'IRCTC',
    'ITC',
    'JINDALSTEL',
    'JKCEMENT',
    'JSWSTEEL',
    'JUBLFOOD',
    'KOTAKBANK',
    'LALPATHLAB',
    'LAURUSLABS',
    'LICHSGFIN',
    'LT',
    'LTIM',
    'LTTS',
    'LUPIN',
    'MANAPPURAM',
    'MARICO',
    'MARUTI',
    'MCX',
    'METROPOLIS',
    'MFSL',
    'MOTHERSON',
    'MPHASIS',
    'MRF',
    'MUTHOOTFIN',
    'NATIONALUM',
    'NAUKRI',
    'NAVINFLUOR',
    'NESTLEIND',
    'NMDC',
    'NTPC',
    'OBEROIRLTY',
    'OFSS',
    'ONGC',
    'PAGEIND',
    'PEL',
    'PERSISTENT',
    'PETRONET',
    'PFC',
    'PIDILITIND',
    'PIIND',
    'PNB',
    'POLYCAB',
    'POWERGRID',
    'PVRINOX',
    'RAMCOCEM',
    'RBLBANK',
    'RECLTD',
    'RELIANCE',
    'SAIL',
    'SBICARD',
    'SBILIFE',
    'SBIN',
    'SHREECEM',
    'SHRIRAMFIN',
    'SIEMENS',
    'SRF',
    'SUNPHARMA',
    'SUNTV',
    'SYNGENE',
    'TATACHEM',
    'TATACOMM',
    'TATACONSUM',
    'TATAMOTORS',
    'TATAPOWER',
    'TATASTEEL',
    'TCS',
    'TECHM',
    'TITAN',
    'TORNTPHARM',
    'TRENT',
    'TVSMOTOR',
    'UBL',
    'ULTRACEMCO',
    'UPL',
    'VEDL',
    'VOLTAS',
    'WIPRO',
    'ZYDUSLIFE'
]

SYMBOL_SUBSCRIPTION_URL = "http://127.0.0.1:8181/subscribe/dispname={stock_symbol}"

SYMBOL_EQUITY_QUOTE_URL = "http://127.0.0.1:8181/getquote/dispname={stock_symbol}EQ"

SYMBOL_FUTURES_QUOTE_URL = "http://127.0.0.1:8181/getquote/dispname={stock_symbol}{expiry}FUT"

SYMBOL_INFO_URL = "http://127.0.0.1:8181/scripinfo/dispname={stock_symbol}EQ"
