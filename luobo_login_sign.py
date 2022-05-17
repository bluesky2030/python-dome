'''
程序可以实现自动登录---成功登录生成cookies文件保存---再签到
post地址通过字符串查找方法找到的，chrome复制的xpath含有tbody，去掉就可以了，懒得改成xpath了
'''

#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import requests
from parsel import Selector
from datetime import datetime
from time import sleep
import os


def login():
    # 生成用户名列表，逐一登录，成功从列表删除
    items = []
    for i in range(311, 312):
        item = 'adsf8650' + str(i)
        items.append(item)
    while items:
        name = items[0]
        print('开始登录---' + name)
        # 打开登录页面，获取form表单数据
        login_url1 = 'https://bbs.6994.cn/member.php?mod=logging&action=login&infloat=yes&handlekey=login&inajax=1&ajaxtarget=fwin_content_login'
        login_header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
            'referer': 'https://bbs.6994.cn/'
        }
        session = requests.session()
        res1 = session.get(url=login_url1, headers=login_header)
        # print(session.cookies)
        # print(res1.text)
        # with open('1.html', 'w', encoding='utf-8') as f:
        #     f.write(res1.text)
        # file = open('1.html', encoding='utf-8')
        # print(file.read())
        # selector = Selector(res1.text)
        # print(selector)
        # formhash = selector.xpath('/html/body/div[1]/div[1]/table/tbody/tr[2]/td[2]/div[1]/div[2]/form/div/input[1]/@value').extract()[0]
        # print(formhash)
        # file.close()
        # 拿到登录地址login_url2
        login_num = res1.text.find('loginhash')
        loginhash = res1.text[(login_num+10):(login_num + 15)]
        login_url2 = 'https://bbs.6994.cn/member.php?mod=logging&action=login&loginsubmit=yes&handlekey=login&loginhash=' + loginhash + '&inajax=1'
        # print(login_url2)
        login_num2 = res1.text.find('formhash')
        formhash = res1.text[(login_num2 + 17):(login_num2 + 25)]
        # print(formhash)
        post_data = {
            'formhash': formhash,
            'referer': 'https://bbs.6994.cn/',
            'username': name,
            'password': name,
            'questionid': 0,
            'answer':''
        }
        res2 = session.post(url=login_url2, data=post_data, headers=login_header)
        # print(res2.text)
        # print(session.cookies)
        # print(res2.cookies)
        # with open('2.html', 'w', encoding='utf-8') as f:
        #     f.write(res2.text)
        check_num = res2.text.find('欢迎您回来')
        if check_num > 0:
            print('登录成功，开始签到--' + name)
            # 当前目录下创建cookies文件夹
            if os.path.isdir('cookies'):
                pass
            else:
                print("当前目录下不存在 cookies文件夹，调用 mkdir 创建该文件夹")
                os.mkdir('cookies')
            path = os.path.dirname(__file__) + '\\' + 'cookies'
            cookie_name = path + '\\' + f'{name}.txt'
            # 写文件
            cookies11 = requests.utils.dict_from_cookiejar(session.cookies)  # 将CookieJar转为字典：
            with open(cookie_name, 'w', encoding='utf-8') as f:
                f.write(str(cookies11))
            items.remove(name)  # 登录成功把成功的name删除
            sign_header = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
            }
            # 访问首页，拿到签到url
            res3 = session.get(url='https://bbs.6994.cn/', headers=sign_header)
            selector3 = Selector(res3.text)
            gold_url = 'https://bbs.6994.cn/home.php?mod=spacecp&ac=credit'
            try:
                items_sign = selector3.xpath('/html/body/div[4]/div/div[2]/div/li/div/p/i/a/@href').extract()[0]
                sign_url = 'https://bbs.6994.cn/' + items_sign
                # print(sign_url)
                session.get(url=sign_url, headers=sign_header)
                res_gold = session.get(url=gold_url, headers=sign_header)
                # print(res_gold)
                selector_gold = Selector(res_gold.text)
                gold_num = selector_gold.xpath('/html/body/div[8]/div[4]/div[1]/div/ul[2]/li[1]/text()').extract()[0]
                print('------签到完成------金币是:' + str(gold_num))
                print(datetime.now())
            except BaseException as e:
                res_gold = session.get(url=gold_url, headers=sign_header)
                # print(res_gold)
                selector_gold = Selector(res_gold.text)
                gold_num = selector_gold.xpath('/html/body/div[8]/div[4]/div[1]/div/ul[2]/li[1]/text()').extract()[0]
                print('已经签到，金币是：' + str(gold_num))
                print(datetime.now())
        else:
            print('登录失败--' + name)
        sleep(3)
        print('')
        session.close()

if __name__ == '__main__':
    login()