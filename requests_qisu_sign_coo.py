#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import requests
import os
from datetime import datetime
import ast
from parsel import Selector
from time import sleep

def gold(session):
    gold_url = 'https://www.108pc.com/'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
    }
    res_gold = session.get(url=gold_url, headers=header)
    # print(res_gold.text)
    # with open('gold.html', 'w', encoding='utf-8') as f:
    #     f.write(res_gold.text)
    selector_gold = Selector(res_gold.text)
    # 拿到个人空间地址
    url_spaces = selector_gold.xpath('/html/body/div[6]/div/div[1]/div/p[1]/strong/a/@href').extract()[0]
    url_space = url_spaces
    # print(url_space)
    res = requests.get(url=url_space, headers=header)
    str_num = res.text.find('金币</em>')
    str_gold = res.text[str_num:(str_num + 14)]
    str_golds = "".join(list(filter(str.isdigit, str_gold)))
    # print(str_golds)
    return str_golds


def sign():
    # 生成用户名列表，逐一签到，成功从列表删除
    items = []
    for i in range(1, 28):
        item = 'qwer63167' + str(i)
        items.append(item)
    # print(items)
    # 循环把列表中的都签到，知道列表为空报错
    while items:         #列表为空 就是false
        # 读文件(先运行获取cookie文件)
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
            res = sign_session.get(url='https://www.108pc.com/', headers=sign_header)
            selector = Selector(res.text)
            # with open('login.html', 'w', encoding='utf-8') as f:
            #     f.write(res.text)
            items_sign = selector.xpath('/html/body/div[3]/div/div[2]/a[2]/@href').extract()[0]
            #https://www.108pc.com/study_daily_attendance-daily_attendance.html?fhash=3c66fdf5
            sign_url = 'https://www.108pc.com/' + items_sign
            # print(sign_url)
            sign_session.get(url=sign_url, headers=sign_header)
            print(f'{name}-------签到完成------金币是:' + str(gold(sign_session)))
            print(datetime.now())
            items.remove(name)  # 登录成功把成功的name删除
            sign_session.close()
            sleep(30)
        except BaseException as e:
            print('连接错误')


    # input()




if __name__ == '__main__':
    sign()

