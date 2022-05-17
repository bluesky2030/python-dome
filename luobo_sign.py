'''
程序依赖已经拿到登录后cookies的字典字符串文件----读取文件----登录成功校验----签到
'''

#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import requests
from datetime import datetime
from parsel import Selector
import os
import ast


def gold(session):
    gold_url = 'https://bbs.6994.cn/home.php?mod=spacecp&ac=credit'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
    }
    res_gold = session.get(url=gold_url, headers=header)
    # print(res_gold.text)
    # with open('gold.html', 'w', encoding='utf-8') as f:
    #     f.write(res_gold.text)
    selector_gold = Selector(res_gold.text)
    gold_num = selector_gold.xpath('/html/body/div[8]/div[4]/div[1]/div/ul[2]/li[1]/text()').extract()[0]
    return gold_num

def sign():
    # 生成用户名列表，逐一签到，成功从列表删除
    items = ['zzz35130', 'zzz35131', 'zzz35132', 'zzz35133', 'zzz35134', 'zzz35135']
    for i in range(1, 633):
        item = 'adsf8650' + str(i)
        items.append(item)
    # print(items)
    # 循环把列表中的都签到，知道列表为空报错
    while items:         #列表为空 就是false
        # 读文件(先运行登录py获取cookie文件)
        name = items[0]
        # print(items[-1])
        path = os.path.dirname(__file__) + '\\' + 'cookies'
        cookie_name = path + '\\' + f'{name}.txt'
        with open(cookie_name, 'r') as f:
            read = f.read()
        sign_cookies = ast.literal_eval(read)
        # print(type(sign_cookies))
        # print(sign_cookies)
        sign_header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
        }
        sign_session = requests.session()
        # 会话加入cookies
        for kk2, vv2 in sign_cookies.items():
            sign_session.cookies.set(kk2, vv2)
        try:
            # 没有报错，说明登录成功,移除name
            print('登录成功--金币:' + str(gold(sign_session)))
            # 访问首页，拿到签到url
            res = sign_session.get(url='https://bbs.6994.cn/', headers=sign_header)
            selector = Selector(res.text)
            # with open('login.html', 'w', encoding='utf-8') as f:
            #     f.write(res.text)
            try:
                items_sign = selector.xpath('/html/body/div[4]/div/div[2]/div/li/div/p/i/a/@href').extract()[0]
                sign_url = 'https://bbs.6994.cn/' + items_sign
                # print(sign_url)
                sign_session.get(url=sign_url, headers=sign_header)
                print(f'{name}-------签到完成------金币是:' + str(gold(sign_session)))
                print(datetime.now())
                items.remove(name)  # 登录成功把成功的name删除
            except BaseException as e:
                print(f'已经签到---------------{name}')
                print(datetime.now())
                items.remove(name)  # 登录成功把成功的name删除
        except BaseException as e:
            print('登录失败')
            with open(f'wrong_{name}.txt', 'w', encoding='utf-8') as f:
                f.write(f'{name}登录失败')
            items.remove(name)  # 防止无限失败，先剔除

        sign_session.close()
    # input()

if __name__ == '__main__':
    sign()

