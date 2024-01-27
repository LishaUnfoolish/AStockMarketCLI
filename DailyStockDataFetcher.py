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

def create_data(stock_dict):
    stock_list = [{'code': code, 'market': 'ab', 'type': 'stock'} for code, stock_info in stock_dict.items()]
    return {
        'stock': json.dumps(stock_list),
        'finClientType': 'pc'
    }

stock_dict = {
    '603333': {'name': '尚纬', 'init': 5.55},
    '600066': {'name': '宇通', 'init': 15.50},
    '603099': {'name': '长白山', 'init': 33.10}
}
data = create_data(stock_dict)
response = requests.post('https://finance.pae.baidu.com/selfselect/gettrenddata', headers=headers, data=data)
response_data = json.loads(response.text)

while True:
    data = create_data(stock_dict)
    response = requests.post('https://finance.pae.baidu.com/selfselect/gettrenddata', headers=headers, data=data)
    response_data = json.loads(response.text)

    # Extract the lastPrice for each stock
    for stock_id, stock_data in response_data['Result']['trend'].items():
        # Extract the stock code from the stock_id
        stock_code = stock_id.split('_')[-1]
        # Get the stock info from the stock_dict
        stock_info = stock_dict.get(stock_code, {"name": "Unknown Stock", "init": 0})
        # Get the stock name and initial price from the stock info
        stock_name = stock_info['name']
        initial_price = stock_info['init']
        # Get the last price from the response data and convert it to float
        last_price = float(stock_data['lastPrice'])
        # Calculate the increase rate
        if initial_price != 0:
            increase_rate = (last_price - initial_price) / initial_price * 100
        else:
            increase_rate = 0
        print(f"{stock_name}, Last Price: {last_price}, Increase Rate: {increase_rate}%")

    # Pause for 1 second
    time.sleep(1)
