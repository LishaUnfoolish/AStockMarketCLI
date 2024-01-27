import requests
import json
import time
headers = {
    'authority': 'finance.pae.baidu.com',
    'accept': 'application/vnd.finance-web.v1+json',
    'accept-language': 'en,zh-CN;q=0.9,zh;q=0.8',
    'acs-token': 'your_acs_token',
    'content-type': 'application/x-www-form-urlencoded',
    'cookie': 'your_cookies',
    'origin': 'https://gushitong.baidu.com',
    'referer': 'https://gushitong.baidu.com/',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
}


def fetch_stock_data(stock_code):
    # 新浪财经API的URL
    url = 'http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData'
    # [{'day': '2024-01-26', 'open': '5.480', 'high': '5.710', 'low': '5.420', 'close': '5.570', 'volume': '54359000'}]
    # 根据股票代码推断交易所
    if stock_code.startswith('60'):
        exchange = 'sh'
    elif stock_code.startswith('00') or stock_code.startswith('300'):
        exchange = 'sz'
    else:
        raise ValueError("股票代码格式不正确，应以'60'或'00'开头")

    # 构建请求参数
    params = {
        'symbol': f'{exchange}{stock_code}',  # 完整的股票代码
        'scale': '240',  # 时间间隔，240表示4小时
        'ma': 'no',  # 是否返回均线数据，no表示不返回
        'datalen': '1'  # 返回数据的数量，这里设置为1，因为我们只需要最新的数据
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Request failed with status {response.status_code}")
    return response.json()



# 通过fetch_stock_data接口返回的day判断当前时间是否在交易时间内
def is_trading_time(stock_code):
    data = fetch_stock_data(stock_code)
    if data:
        day = data[0]['day']
        if day == time.strftime("%Y-%m-%d", time.localtime()):
            return True
        else:
            return False
    else:
        return False
    
    
def create_data(stock_dict):
    for code in stock_dict.keys():
        data = fetch_stock_data(code)
        if data:
            stock_dict[code]['open'] = data[0]['open']
    stock_list = [{'code': code, 'market': 'ab', 'type': 'stock'} for code, stock_info in stock_dict.items()]
    return {
        'stock': json.dumps(stock_list),
        'finClientType': 'pc'
    }

stock_dict = {
    '603333': {'name': '尚', 'init': 6.505},
    '600066': {'name': '宇', 'init': 16.070},
    '603099': {'name': '长', 'init': 32.773}
}

create_data(stock_dict)
data = create_data(stock_dict)
response = requests.post('https://finance.pae.baidu.com/selfselect/gettrenddata', headers=headers, data=data)
response_data = json.loads(response.text)

try:
    # Extract the lastPrice for each stock
    if is_trading_time('600519') == False:
        print(f"非交易时间")
    while True:
        for stock_id, stock_data in response_data['Result']['trend'].items():
            # Extract the stock code from the stock_id
            stock_code = stock_id.split('_')[-1]
            # Get the stock info from the stock_dict
            stock_info = stock_dict.get(stock_code, {"name": "Unknown Stock", "init": 0, "open": 0})
            # Get the stock name, initial price, and open price from the stock info
            stock_name = stock_info['name']
            initial_price = stock_info['init']
            # Get the last price from the response data and convert it to float
            last_price = float(stock_data['lastPrice'])
            # Calculate the increase rate from initial price
            if initial_price != 0:
                increase_rate_init = round((last_price - initial_price) / initial_price * 100, 3)
            else:
                increase_rate_init = 0
            # Calculate the increase rate from open price
            open_price = stock_info.get('open')
            if open_price is not None:
                open_price = float(open_price)
                if open_price != 0:
                    increase_rate_open = round((last_price - open_price) / open_price * 100, 3)
                else:
                    increase_rate_open = 0
            else:
                increase_rate_open = 0
            print(f"{stock_name}|开:{open_price}|现:{last_price}|仓R:{increase_rate_init}%|开R:{increase_rate_open}%|")
        print(f"----------------------------------------------------")
        # Pause for 1 second
        time.sleep(1)
except KeyboardInterrupt:
    print("\nstop\n")
