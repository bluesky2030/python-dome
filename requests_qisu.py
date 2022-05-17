#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import requests
from parsel import Selector
import ddddocr
from datetime import datetime
import time
import os
from time import sleep
import sys

# 控制台输出保存至文件
class Logger(object):
    def __init__(self, filename='default.log', stream=sys.stdout):
        self.terminal = stream
        self.log = open(filename, 'w')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass

# 传入文件夹字符名称，识别本地图片
def dddd_ocr(img_uid):
    print(datetime.now())
    start = time.time()
    ocr = ddddocr.DdddOcr()
    # 获取当前路径img文件夹的path
    path = os.path.dirname(__file__) + '\\' + img_uid
    pic_name2 = path + '\\' + '2.png'
    with open(pic_name2, 'rb') as f:
        img_bytes = f.read()
    res = ocr.classification(img_bytes)
    try:
        # 可能识别不出来报错
        # 去掉空格
        result = str(res).replace(" ", "")
        end = time.time()
        print(f"Running time: {(end - start):.2f} Seconds")
        return result
    except BaseException as e:
        # 出现错误之后需要执行的程序
        print("验证码无法识别")
        return 'none'

# 把浏览器复制的字符串cookie转换成字典dict
def cookies_to_dict(str_cookie):
    cookie_list = str_cookie.split('; ')
    # print(cookie_list)
    cookies = {}
    for i in cookie_list:
        cookies[i.split('=')[0]] = i.split('=')[1]
    # print(cookies)
    return cookies

# 下载验证码，同时返回加入返回cookies的新session，传入请求会话、验证码地址、帖子地址、用户UID
def download_img(reply_session, misc_url, reply_url, reply_uid):
    src_header1 = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Mobile Safari/537.36',
        'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'accept-language': 'zh-CN,zh;q=0.9',
        'referer': reply_url
    }
    res_misc = reply_session.get(url=misc_url, headers=src_header1)
    # -------------------------下面此处需要加入返回的cookies----------------------
    # 将CookieJar转为字典：
    cookies11 = requests.utils.dict_from_cookiejar(res_misc.cookies)
    # 会话加入cookies
    for kk2, vv2 in cookies11.items():
        # print(kk, vv)
        reply_session.cookies.set(kk2, vv2)
    # --------------------------上面此处需要加入返回的cookies---------------------
    # 当前目录下创建img文件夹
    if os.path.isdir(reply_uid):
        print("")
    else:
        print("当前目录下不存在 img 文件夹，调用 mkdir 创建该文件夹")
        os.mkdir(reply_uid)
    path = os.path.dirname(__file__) + '\\' + reply_uid
    pic_name2 = path + '\\' + '2.png'
    with open(pic_name2, 'wb') as f:
        f.write(res_misc.content)
    print('验证码图片已下载')

    return reply_session   # 返回新的带验证码cookies的session

# 传入用户uid，拿到用户金币个数
def gold(UID):
    gold_url = 'https://www.108pc.com/space-uid-' + str(UID) + '.html'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)'
    }
    res = requests.get(url=gold_url, headers=header)
    str_num = res.text.find('金币</em>')
    str_gold = res.text[str_num:(str_num + 14)]
    str_golds = "".join(list(filter(str.isdigit, str_gold)))
    # print(str_golds)
    return str_golds

# 请求帖子地址、html页面获取post所需data数据、构建data回帖
def reply_post(reply_url, reply_cookie, reply_uid, reply_counter):
    sys.stdout = Logger(f'{reply_uid}.log', sys.stdout)              # 函数开头调用，控制台print保存至文件
    sys.stderr = Logger(f'{reply_uid}_debug.log', sys.stderr)        # 函数开头调用，控制台错误信息保存至文件
    print(reply_url)
    counter = 0  # 用来计数
    while counter < reply_counter:    # 小于指定次数就循环
        counter = counter + 1
        # 第一次请求帖子地址，用浏览器F12获取的cookies登录
        header = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Mobile Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'zh-CN,zh;q=0.9'
        }
        reply_session = requests.session()
        # -------------------以下为session加入第一次cookies----------------------
        login_cookie = cookies_to_dict(reply_cookie)
        # 会话加入cookies
        for kk, vv in login_cookie.items():
            # print(kk, vv)
            reply_session.cookies.set(kk, vv)
        # -------------------以上为session加入第一次cookies----------------------
        res = reply_session.get(url=reply_url, headers=header)
        page_text = res.text
        # -------------------以下为session加入第二次返回的cookies----------------------
        # print(seesion_all.cookies.get_dict())
        cookies11 = requests.utils.dict_from_cookiejar(res.cookies)   # 将CookieJar转为字典：
        # 会话加入cookies
        for kk2, vv2 in cookies11.items():
            reply_session.cookies.set(kk2, vv2)
        # -------------------以上为session加入第二次返回的cookies----------------------
        selector = Selector(page_text)
        items = selector.xpath('/html/body/div[2]/div[5]/form/div/ul/li[2]/div/img/@src').extract()[0]
        misc_url = 'https://www.108pc.com/' + items
        # 下载验证码图片,启用新的session1
        reply_session1 = download_img(reply_session, misc_url, reply_url, reply_uid)
        # 验证码识别
        misc_str = dddd_ocr(reply_uid)
        print('验证码是:' + misc_str)
        # -----------------------------------提交回复post-------------------------------------
        post_header = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Mobile Safari/537.36',
            'accept': 'application/xml, text/xml, */*; q=0.01',
            'accept-language': 'zh-CN,zh;q=0.9',
            'referer': reply_url
        }
        post_url1 = selector.xpath('/html/body/div[2]/div[5]/form/@action').extract()[0]
        post_url = 'https://www.108pc.com/' + post_url1 + '&handlekey=fastpost&loc=1&inajax=1'
        # ---------构建提交表单form，验证码上面已经拿到-------
        data_formhash = selector.xpath('/html/body/div[2]/div[5]/form/input/@value').extract()[0]      # 拿到formhash
        print(data_formhash)
        data_seccodehash = selector.xpath('/html/body/div[2]/div[5]/form/div/ul/li[2]/div/input[1]/@value').extract()[0]      # 拿到seccodehash
        # print(data_seccodehash)
        reply_data = {
            'formhash': data_formhash,
            'message': '这东西我收了！谢谢楼主！[color=blue]奇速论坛[/color]真好！',
            'seccodehash': data_seccodehash,
            'seccodeverify': misc_str
        }
        # ---------构建提交表单form，验证码上面已经拿到-------
        gold_num1 = int(gold(reply_uid))  #回复之前先看看有多少金币
        # print(gold_num1)
        content = reply_session1.post(url=post_url, data=reply_data, headers=post_header)       # 提交post数据
        # print(content.text)
        # 检查是否有用户组回帖限制，如果有就暂停40分钟
        tip = content.text.find('用户组每小时限制')  # -1就是没找到，>0就是找到了
        str_num = content.text.find('非常感谢，回复发布成功')
        str_num2 = content.text.find('抱歉，验证码填写错误')
        # 如果含有用户组
        if tip > 0:
            print(datetime.now())
            print('---------达到用户组回帖上限------------')
            input()
            break
        elif str_num > 0:
            # 如果回复成功，判断是否金币上限
            print('回复成功')
            gold_num2 = int(gold(reply_uid))
            print('------金币是' + str(gold_num2) + '------')
            if (gold_num2 != (gold_num1 + 1)):
                # 跳出循环，结束
                print('回复上限，不增加金币了')
                break
        elif str_num2 > 0:
            print('验证码错误')

        sleep(15)
        reply_session1.close()

def main():

    # 牛逼宝宝
    reply_uid1 = '42681'
    reply_cookie1 = '_dx_captcha_cid=19645000; _dx_uzZo5y=a9f282e8a8e47e11e0904f3c8df98d942cf2f2cada32_pc_size_c=0; AzOC_2132_saltkey=AR6b5Btt; AzOC_2132_lastvisit=1651225112; _dx_app_78f14b4be40b334e7a349358d815974d=626bc029VHo349KBRjQTumMDIl6LGfM9LIChlC01; _dx_captcha_vid=27BC64C39D0DCEE6F508048C95801BF85D10B43D535409BEE4DC681C2CAD816B6AA18563421854FE077814DF08B9A46C2C0040FC6FC7DE6AC5F95375A4A1A646BCAD863299E34F9E61AAD2EEF24A902F; AzOC_2132_auth=b73a56jj7oTftJuuREJl0FbYnQaOcbxx4J49wYHcFUgRL9rSLD5h2%2BbF45m0qhI3uW0O5Di64RqSRNuK1rxy4aB6jw; AzOC_2132_lastcheckfeed=42681%7C1651228725; AzOC_2132_sid=0; AzOC_2132_connect_is_bind=0; AzOC_2132_editormode_e=1; AzOC_2132_smile=1D1; AzOC_2132_nofavfid=1; Hm_lvt_a3980460ddca888011c6777eda40da3e=1651135728,1651227522,1651245280,1651287914; AzOC_2132_atarget=1; AzOC_2132_visitedfid=2D37; AzOC_2132_st_t=42681%7C1651288256%7C422fc92d04d41efc3175046e701f61b8; AzOC_2132_forum_lastvisit=D_37_1651288189D_2_1651288256; AzOC_2132_viewid=tid_13052; AzOC_2132_clearUserdata=forum; AzOC_2132_creditnotice=0D0D1D0D0D0D0D0D0D42681; AzOC_2132_creditbase=0D0D69D0D0D0D0D0D0; AzOC_2132_creditrule=%E5%8F%91%E8%A1%A8%E5%9B%9E%E5%A4%8D; AzOC_2132_st_p=42681%7C1651297847%7C81084385e4d89a00398d98cc279593c0; AzOC_2132_ulastactivity=1651297847%7C0; AzOC_2132_seccode=2811.4a91459b7c2fd90533; bygsjw=1; AzOC_2132_sendmail=1; AzOC_2132_home_diymode=1; AzOC_2132_checkpm=1; AzOC_2132_lastact=1651298067%09index.php%09; Hm_lpvt_a3980460ddca888011c6777eda40da3e=1651298066'
    # 华西口腔
    reply_uid2 = '42823'
    reply_cookie2 = '_dx_captcha_cid=73297233; _dx_uzZo5y=416f6493935c2298c5000db36c1d05fe3534420f444237b4be40b334e7a349358d815974d=6268ef80I8huGEswUTIn484EGEhfswd1pmWxskv1; Hm_lvt_a3980460ddca888011c6777eda40da3e=1651039007,1651039077,1651044350,1651045673; AzOC_2132_pc_size_c=0; AzOC_2132_saltkey=nhwqChFy; AzOC_2132_lastvisit=1651042493; AzOC_2132_sendmail=1; _dx_captcha_vid=AC6948392E972EEC83F3AC1C07FCCBB39822E5E2075CF40E8EFDF07F8991102CA502110EDF4B4E71F013A0AB4478D50ACB077318369C36547C13CE9574E221B61064F20FF735A7064472B2A954A1A272; AzOC_2132_ulastactivity=1651046113%7C0; AzOC_2132_auth=4c1b2DM71NZCMaPi7vU5O%2BgCQwdojcBlqwK4J6JICdHFPkbvwC84hhqD3zrbHwyd8hnBaDMlL%2BBcZU2eMJgjp4yk5w; AzOC_2132_lastcheckfeed=42823%7C1651046113; AzOC_2132_lip=58.218.43.118%2C1651046113; AzOC_2132_sid=0; AzOC_2132_connect_is_bind=0; AzOC_2132_nofavfid=1; AzOC_2132_st_t=42823%7C1651046353%7C3d3c3185d5089cf1f15f9fb085d52fe1; AzOC_2132_atarget=1; AzOC_2132_forum_lastvisit=D_2_1651046353; AzOC_2132_visitedfid=2; AzOC_2132_checkpm=1; AzOC_2132_st_p=42823%7C1651046357%7C8b2bc5a48714abe81f1099ce81bcb101; AzOC_2132_viewid=tid_12986; Hm_lpvt_a3980460ddca888011c6777eda40da3e=1651046491; AzOC_2132_smile=1D1; AzOC_2132_seccodecS0=4064.3b60114ab46bcb81e6; AzOC_2132_nofocus_forum=1; AzOC_2132_lastact=1651046378%09misc.php%09seccode'
    # 传奇一哥
    reply_uid3 = '42920'
    reply_cookie3 = '_dx_captcha_cid=73297233; _dx_uzZo5y=416f6493935c2298c5000db36c1d05fe3980460ddca888011c6777eda40da3e=1651029952,1651039007,1651039077,1651044350; _dx_app_78f14b4be40b334e7a349358d815974d=6268ef80I8huGEswUTIn484EGEhfswd1pmWxskv1; AzOC_2132_pc_size_c=0; AzOC_2132_saltkey=r6TTN6uu; AzOC_2132_lastvisit=1651040932; AzOC_2132_sendmail=1; _dx_captcha_vid=319DD6AE82249ED032649D9AA3DFC7F73F20B413BD02D748A241026D56C6BD363ED13355987D2F048853C7892903B27B19187AC6D3CA55A68F24C79B0DFC36FF89B4D9988F271A8EB48521CB3409C89E; AzOC_2132_ulastactivity=1651044555%7C0; AzOC_2132_auth=5ad0mD28RKTkTw9okliwY0zIMDJ5vkAH2kOe3V32mAZ15XVmUzZG33Ny5GSIwVfnYDfGAJJXPoq0cR81%2F36YMMfpLA; AzOC_2132_lastcheckfeed=42920%7C1651044555; AzOC_2132_checkfollow=1; AzOC_2132_lip=58.218.43.118%2C1651044555; AzOC_2132_sid=0; AzOC_2132_connect_is_bind=0; AzOC_2132_nofavfid=1; AzOC_2132_checkpm=1; AzOC_2132_noticeTitle=1; Hm_lpvt_a3980460ddca888011c6777eda40da3e=1651044689; AzOC_2132_lastact=1651044557%09misc.php%09patch'

    reply_counter = 500
    # 回复帖子地址
    print('输入帖子地址')
    reply_url = input()
    if reply_url == '':
        reply_url = 'https://www.108pc.com/thread-11394-1-6.html'
        print(reply_url)
    print('请输入顶贴账号1、2、3')
    choice = int(input())
    if choice == 1:
        print('执行牛逼宝宝9')
        reply_post(reply_url, reply_cookie1, reply_uid1, reply_counter)
    if choice == 2:
        print('华西口腔')
        reply_post(reply_url, reply_cookie2, reply_uid2, reply_counter)
    if choice == 3:
        print('传奇一哥')
        reply_post(reply_url, reply_cookie3, reply_uid3, reply_counter)


if __name__ == '__main__':
    main()
















