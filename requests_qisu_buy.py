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
    space_url = 'https://www.108pc.com/home.php?mod=space&uid=41236&do=thread&view=me&from=space'  # 天地清霜的空间
    space_header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
        'cookie': '_dx_captcha_cid=19645000; _dx_uzZo5y=a9f282e8a8e47e11e0904f3c8df98d942cf2f2cadae7b5fd86ea6c647990f4aa58f92f5f; _dx_app_78f14b4be40b334e7a349358d815974d=62778e690GfgxJuy3zI1f3IZytfC559VkIvXX5i1; _dx_captcha_vid=961E17C54E001F270AB15DD9B72E754058A6A3627AFAEEE665531D22A44BF33E44B222FA4152DC7C89AA7ABADAEC5D863E68CD1E7D2A8993B3FA6247B942111620C0DDA1C1EE12FB09278F6EC43F0DD4; AzOC_2132_pc_size_c=0; AzOC_2132_saltkey=RP8z26JP; AzOC_2132_lastvisit=1652445563; AzOC_2132_sendmail=1; Hm_lvt_a3980460ddca888011c6777eda40da3e=1652262491,1652437986,1652445748,1652525081; AzOC_2132_atarget=1; AzOC_2132_visitedfid=2; AzOC_2132_st_p=0%7C1652525100%7C63912f94bcfeae340afd6132a78b7309; AzOC_2132_viewid=tid_13448; AzOC_2132_home_diymode=1; AzOC_2132_ulastactivity=1652525139%7C0; AzOC_2132_auth=aa8cF%2BPGZSP25Elw4V%2BqblClWJttT0YXDe7RMUeHMdCtSMpfar9wDBy9c7a7Gy%2B%2FjOGZbqFe0wgsM%2Fwg%2FRxtxnGZJQ; AzOC_2132_lastcheckfeed=41236%7C1652525139; AzOC_2132_lip=183.209.180.139%2C1652525139; AzOC_2132_sid=0; AzOC_2132_connect_is_bind=0; AzOC_2132_st_t=41236%7C1652525139%7Cc3d64a1b95a9491a07e2a5a87c8293cc; AzOC_2132_forum_lastvisit=D_2_1652525139; AzOC_2132_noticeTitle=1; AzOC_2132_nofavfid=1; AzOC_2132_checkpm=1; Hm_lpvt_a3980460ddca888011c6777eda40da3e=1652525254; AzOC_2132_lastact=1652525257%09misc.php%09patch'
    }
    res_space = requests.get(url=space_url, headers=space_header)
    # with open('res_space.html', 'w', encoding='utf-8') as f:
    #     f.write(res_space.text)
    selector_space = Selector(res_space.text)
    urls = selector_space.xpath('//*[@id="delform"]/table/tr/th/a/@href').extract()
    print(urls)
    titles = selector_space.xpath('//*[@id="delform"]/table/tr/th/a/text()').extract()
    for title in titles:
        print(str(titles.index(title)) + ' 、' + str(title))
    print('请选择需要购买的帖子序号；')
    tie_num = int(input())
    # tie_num = 0
    tid_url = urls[tie_num]
    print(tid_url)
    # -------先输出所有需要购买的帖子地址---------
    # 1、登录访问购买帖子地址。判断金币个数，登录成功后移除name
    # 生成用户名列表，逐一购买，成功从列表删除
    items = []
    for i in range(1, 28):
        item = 'qwer63167' + str(i)
        items.append(item)

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
        tid = tid_url.split('-')[1]
        tid_header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
        }
        # 访问帖子地址
        res_tid = buy_session.get(url=tid_url, headers=tid_header)
        with open('tid.html', 'w', encoding='utf-8') as f:
            f.write(res_tid.text)
        # 2、从帖子页面拿到购买地址url
        try:
            selector = Selector(res_tid.text)
            download_url = selector.xpath('//*[@class="tattl"]/dd/p[3]/a[2]/@href').extract()[0]
            print(download_url)
            download_header = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
                'referer': tid_url,
                'origin': 'https://www.108pc.com'
            }
            res_download = buy_session.get(url=download_url, headers=download_header)
            # with open('tid.html', 'w', encoding='utf-8') as f:
            #     f.write(res_download.text)
            buy_url = f'https://www.108pc.com/forum.php?mod=misc&action=attachpay&tid={tid}&paysubmit=yes&infloat=yes&inajax=1'
            print(buy_url)
            # 3、构建表单数据
            selector1 = Selector(res_download.text)
            formhash = selector1.xpath('//*[@class="f_c"]/input[1]/@value').extract()[0]
            print(formhash)
            aid = selector1.xpath('//*[@class="f_c"]/input[3]/@value').extract()[0]
            print(aid)
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
            buy_num1 = res_buy.text.find('附件购买成功')
            buy_num2 = res_buy.text.find('金币不足')
            if buy_num1 > 0:
                print(f'附件购买成功---------{name}')
            elif buy_num2 > 0:
                print(f'购买金币不足---------{name}')
            items.remove(name)
            print(datetime.now())
        except BaseException as e:
            print(f'已经购买过了----------{name}')
            items.remove(name)
            print(datetime.now())
        sleep(30)
        print('')
        buy_session.close()

if __name__ == '__main__':
    buy()