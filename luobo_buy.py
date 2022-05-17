'''
程序依赖已经拿到登录后cookies的字典字符串文件----读取文件----登录成功校验----购买附件
chrome用xpath找不到，需要把 tbody 去掉
'''

#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import requests
from datetime import datetime
from parsel import Selector
import os
import ast
from time import sleep


def buy():
    # -------先输出所有需要购买的帖子地址---------
    space_url = 'https://bbs.6994.cn/home.php?mod=space&uid=29826&do=index'  # 天地清霜的空间  https://bbs.6994.cn/space-uid-29826.html
    space_header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
    }
    res_space = requests.get(url=space_url, headers=space_header)
    selector_space = Selector(res_space.text)
    urls = selector_space.xpath('//*[@class="xl"]/li/a/@href').extract()
    # print(urls)
    titles = selector_space.xpath('//*[@class="xl"]/li/a/text()').extract()
    # print(titles)
    for title in titles:
        print(str(titles.index(title)) + ' 、' + str(title))
    print('请选择需要购买的帖子序号；')
    tie_num = int(input())
    tid_url = 'https://bbs.6994.cn/' + urls[tie_num]
    print(tid_url)
    # -------先输出所有需要购买的帖子地址---------
    # 1、登录访问购买帖子地址。判断金币个数，登录成功后移除name
    # 生成用户名列表，逐一购买，成功从列表删除
    items = ['zzz35130', 'zzz35131', 'zzz35132', 'zzz35133', 'zzz35134', 'zzz35135']
    for i in range(1, 501):
        item = 'adsf8650' + str(i)
        items.append(item)
    # 循环把列表中的都购买，知道列表为空就是假
    while items:
        # 读取本地cookies数据
        name = items[0]
        path = os.path.dirname(__file__) + '\\' + 'cookies'
        cookie_name = path + '\\' + f'{name}.txt'
        with open(cookie_name, 'r') as f:
            read = f.read()
        buy_cookies = ast.literal_eval(read)
        # 建立会话
        buy_session = requests.session()
        # 会话加入cookies
        for kk2, vv2 in buy_cookies.items():
            buy_session.cookies.set(kk2, vv2)
        # 帖子地址
        # tid_url = 'https://bbs.6994.cn/thread-31551-1-1.html'
        # tid_url = 'https://bbs.6994.cn/thread-31547-1-1.html'
        tid = tid_url.split('-')[1]
        tid_header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
        }
        # 访问帖子地址
        res_tid = buy_session.get(url=tid_url, headers=tid_header)
        # print(res_tid.text)
        # with open('tid.html', 'w', encoding='utf-8') as f:
        #     f.write(res_tid.text)
        # 2、从帖子页面拿到购买地址url
        try:
            selector = Selector(res_tid.text)
            download_urls = selector.xpath('/html/body/div[8]/div[7]/div[3]/div[1]/table/tr[1]/td[2]/div[2]/div[2]/div/div[3]/div[3]/div[2]/ignore_js_op/dl/dd/p[1]/a/@href').extract()[0]
            # '/html/body/div[8]/div[7]/div[3]/div[1]/table/tbody/tr[1]/td[2]/div[2]/div[2]/div/div[3]/div[3]/div[2]/ignore_js_op/dl/dd/p[1]/a/@href
            download_url = 'https://bbs.6994.cn/' + download_urls + '&infloat=yes&handlekey=attachpay&inajax=1&ajaxtarget=fwin_content_attachpay'
            # https://bbs.6994.cn/forum.php?mod=misc&action=attachpay&aid=150830&tid=31547&infloat=yes&handlekey=attachpay&inajax=1&ajaxtarget=fwin_content_attachpay
            # print(download_url)
            # 访问下载地址，获取购买url，并返回cookies
            download_header ={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
                'referer': tid_url
            }
            res_download = buy_session.get(url=download_url, headers=download_header)
            # with open('tid.html', 'w', encoding='utf-8') as f:
            #     f.write(res_download.text)
            buy_url = f'https://bbs.6994.cn/forum.php?mod=misc&action=attachpay&tid={tid}&paysubmit=yes&infloat=yes&inajax=1'
            # print(buy_url)
            # 3、构建表单数据
            selector1 = Selector(res_download.text)
            formhash = selector1.xpath('/html/body/root/div/input[1]/@value').extract()[0]
            # print(formhash)
            aid = selector1.xpath('/html/body/root/div/input[3]/@value').extract()[0]
            # print(aid)
            post_data = {
                'formhash': formhash,
                'referer': tid_url,
                'aid': aid,
                'handlekey': 'attachpay'
            }
            # 4、提交post
            res_buy = buy_session.post(url=buy_url, data=post_data, headers=download_header)
            # print(res_buy.text)
            # with open('buy.html', 'w', encoding='utf-8') as f:
            #     f.write(res_buy.text)
            buy_num = res_buy.text.find('附件购买成功')
            if buy_num > 0:
                print(f'附件购买成功---------{name}')
            else:
                print(f'购买金币不足---------{name}')
            items.remove(name)
            print(datetime.now())
        except BaseException as e:
            print(f'已经购买过了----------{name}')
            items.remove(name)
            print(datetime.now())
        sleep(3)
        print('')
        buy_session.close()



def main():

    buy()


if __name__ == '__main__':
    main()