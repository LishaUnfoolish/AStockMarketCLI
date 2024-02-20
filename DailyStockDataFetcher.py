from urllib import request
import re
from tabulate import tabulate
import time
import logging
import os

try :
    from pynput import keyboard
except ImportError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'pynput'])
    from pynput import keyboard

try :
    from tabulate import tabulate
except ImportError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'tabulate'])
    from tabulate import tabulate



logging.basicConfig(filename='/tmp/stock.log', level=logging.INFO)
def extract_stock_data(url, encoding="gb2312"):
    """
    抽取股票数据
    :param url:
    :param encoding: 默认gb2312
    :return: list(list)
    """
    # 发起请求
    req = request.Request(url)
    # 获取响应
    rsp = request.urlopen(req)
    res = rsp.read().decode("gb2312")
    stock_arr = res.split(";")
    stock_arr.pop()
    return stock_arr


def process_stock_data(stock_arr, index_dict):
    """
    对股票数据进行预处理，获取指定下标的数据
    :param stock_arr:
    :param index_dict:
    :return: list(dict)
    """
    result_list = []
    for stock in stock_arr:
        inner_map = {}
        start = stock.find("\"")
        end = stock.rfind("\"")
        rest = stock[start + 1:end]
        arr = rest.split("~")
        for x in range(len(arr)):
            if x in index_dict.keys():
                inner_map[index_dict[x]] = arr[x]
        result_list.append(inner_map)
    return result_list


def concat_code(*codes, prefix="", suffix=","):
    """
    根据前后缀拼接股票代码
    :param codes: 可变参数
    :param prefix: 默认”“
    :param suffix: 默认”,"
    :return: str
    """
    result = ""
    for index in range(len(codes)):
        exchange=determine_exchange(codes[index])
        result += (prefix + exchange+codes[index] + suffix)
    if len(suffix) > 0:
        result = result[0:-1]
    return result

def print_as_table(data):
    headers = data[0].keys()
    rows = [x.values() for x in data]
    info = tabulate(rows, headers, tablefmt="grid")
    logging.info(info)
    return info
     

def determine_exchange(stock_code):
    if stock_code.startswith('60'):
        return 'sh'
    elif stock_code.startswith('00') or stock_code.startswith('300'):
        return 'sz'
    else:
        return ''

def get_stock_real_time_data(*codes):
    #在codes添加上证指数
    codes = list(codes) 
    codes.append("sh000001") 
    detail_url = "http://qt.gtimg.cn/q=" + concat_code(*codes)
    detail_index_to_values = {
        1: '名称',
        # 2: '股票代码',
        3: '现价',
        # 4: '昨收',
        # 5: '开盘价',
        # 6: '成交量',
        # 7: '外盘（不准）',
        # 8: '内盘（不准）',
        # 9: '买一',
        # 10: '买一量(手)',
        # 11: '买二',
        # 12: '买二量(手)',
        # 13: '买三',
        # 14: '买三量(手)',
        # 15: '买四',
        # 16: '买四量(手)',
        # 17: '买五',
        # 18: '买五量(手)',
        # 19: '卖一',
        # 20: '卖一量(手)',
        # 21: '卖二',
        # 22: '卖二量(手)',
        # 23: '卖三',
        # 24: '卖三量(手)',
        # 25: '卖四',
        # 26: '卖四量(手)',
        # 27: '卖五',
        # 28: '卖五量(手)',
        # 29: '最近逐笔成交',
        30: '时间',
        # 31: '涨跌',
        32: '涨跌(%)',
        # 33: '最高价',
        # 34: '最低价',
        # 35: '价格/成交量(手)/成交额',
        # 36: '成交量(手)',
        # 37: '成交额(万)',
        38: '换手率(%)',
        # 39: '市盈率',
        # 40: '',  # 这里没有提供对应的值，所以留空
        # 41: '最高价',  # 注意这里重复了，可能是因为数据错误或者需要合并
        42: '最低价',
        43: '振幅(%)',
        # 44: '流通市值',
        # 45: '总市值',
        # 46: '市净率',
        # 47: '涨停价',
        # 48: '跌停价',
    }
    detail_data = extract_stock_data(detail_url)
    detail_list = process_stock_data(detail_data, detail_index_to_values)
    return print_as_table(detail_list)

    # fund_url = 'http://qt.gtimg.cn/q=' + concat_code(*codes, prefix="ff_")
    # fund_comment_to_index = {
    #     0: '代码',
    #     1: '主力流入',
    #     2: '主力流出',
    #     3: '主力净流入',
    #     # 4: '主力流入百分比(主力净流入/资金流入流出总和)',
    #     5: '散户流入',
    #     6: '散户流出',
    #     7: '散户净流入',
    #     # 8: '散户流入百分比(散户净流入/资金流入流出总和)',
    #     # 9: '资金流入或流出总和 1+2 or 5+6',
    #     13: '日期',
    # }
    # fund_data = extract_stock_data(fund_url)
    # fund_list = process_stock_data(fund_data, fund_comment_to_index)
    # print_as_table(fund_list)




paused = False
def on_press(key):
    global paused
    if key == keyboard.Key.alt_r:
        paused = not paused
        os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == '__main__':
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    try:
        while True:
            if not paused:
                os.system('cls' if os.name == 'nt' else 'clear')
                print(get_stock_real_time_data("000429","600900","600066","601088","600482","600178","000625","603259","002506","002689","002609"))
                # print(get_stock_real_time_data("002415","002230","000938","002472"))
                
            time.sleep(1)
    except KeyboardInterrupt:
        os.system('cls' if os.name == 'nt' else 'clear')


        
