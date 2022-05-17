'''
实现自动注册，验证码识别太低，需要训练
启用图灵本地识别，识别率较高。
'''

#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import requests
from parsel import Selector
import ddddocr
from datetime import datetime
import time
import os
import base64
from time import sleep


# 传入文件夹名称
def tuling_ocr(img_uid):
    start = time.time()
    # 获取当前路径img文件夹的path
    path = os.path.dirname(__file__) + '\\' + img_uid
    misc_name = path + '\\' + 'misc.png'
    with open(misc_name, 'rb') as f:
        image = base64.b64encode(f.read())
    image_base64 = str(image).split('\'')[1]
    try:
        url = 'http://127.0.0.1:33333/puxiuyssb?tu=' + image_base64  # 本地接口
        # url = 'http://114.116.115.78:33333/puxiuyssb?tu=' + image_base64  # 服务器接口
        result = requests.get(url=url)
        end = time.time()
        print(f"Running time: {(end - start):.2f} Seconds")
        return result.text
    except BaseException as e:
        print('接口连接失败')
        return '6666'

# 传入文件夹字符名称，识别本地图片
def dddd_ocr(img_uid):
    print(datetime.now())
    start = time.time()
    ocr = ddddocr.DdddOcr()
    # 获取当前路径img文件夹的path
    path = os.path.dirname(__file__) + '\\' + img_uid
    pic_name = path + '\\' + 'misc.png'
    with open(pic_name, 'rb') as f:
        img_bytes = f.read()
    res = ocr.classification(img_bytes)
    try:
        # 可能识别不出来报错
        # 去掉空格
        # print(res)
        result = str(res).replace(" ", "")
        end = time.time()
        print(f"Running time: {(end - start):.2f} Seconds")
        return result
    except BaseException as e:
        # 出现错误之后需要执行的程序
        print("验证码无法识别")
        return 'none'

# 传入文件夹名称
def baidu_ocr(img_uid):
    # img直接传本地图片
    print(datetime.now())
    start = time.time()
    # 获取access_token
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    appid = "25876326"
    client_id = "54lekuPfz0MAFmXLsFOGZhwS"
    client_secret = "28FD1UimtkaNhZOk6jwBA08X45s88TyG"
    print("appid:" + appid)
    print("client_id:" + client_id)
    print("client_secret:" + client_secret)
    token_url = "https://aip.baidubce.com/oauth/2.0/token"
    host = f"{token_url}?grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}"
    response = requests.get(host)
    access_token = response.json().get("access_token")
    # 调用通用文字识别高精度版接口
    # request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
    # 网络图片文字识别接口
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/webimage"
    # 以二进制方式打开图文件
    # 参数image：图像base64编码
    # 下面图片路径请自行切换为自己环境的绝对路径
    # 获取当前路径img文件夹的path
    path = os.path.dirname(__file__) + '\\' + img_uid
    pic_name = path + '\\' + 'misc.png'
    with open(pic_name, "rb") as f:
        image = base64.b64encode(f.read())
    body = {
        "image": image,
        "language_type": "auto_detect",
        "detect_direction": "true",
        "paragraph": "true",
        "probability": "true",
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    request_url = f"{request_url}?access_token={access_token}"
    response = requests.post(request_url, headers=headers, data=body)
    # content = response.content.decode("UTF-8")
    # 打印调用结果
    res = response.json()
    try:
        # 可能识别不出来报错
        results = res["words_result"][0]["words"]
        # result = res["words_result"][0]["words"]
        # 去掉空格
        result = str(results).replace(" ", "")
        # print(result)
        end = time.time()
        print(f"Running time: {(end - start):.2f} Seconds")
        return result
    except BaseException as e:
        # 出现错误之后需要执行的程序
        print("验证码无法识别")
        return '6'

def register():
    # 生成用户名列表，逐一注册，成功从列表删除
    # items = ['zzz35130', 'zzz35131', 'zzz35132', 'zzz35133', 'zzz35134', 'zzz35135']
    items = []
    for i in range(632, 1001):
        item = 'adsf8650' + str(i)
        items.append(item)

    while items:
        name = items[0]
        print('开始注册---' + name)
        # 循环,知道用户名列表为空，报错
        session = requests.session()
        register_url = 'https://bbs.6994.cn/member.php?mod=register'
        post_url = 'https://bbs.6994.cn/member.php?mod=register&inajax=1'
        register_header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
        }
        post_header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
            'referer': register_url
        }
        # 第一次访问注册页面，并记录cookies到session
        res1 = session.get(url=register_url, headers=register_header)
        # 拿到相关表单数据
        selector = Selector(res1.text)
        formhash = selector.xpath('/html/body/div[8]/div[3]/div[2]/div[1]/form/div[1]/input[2]/@value').extract()[0]
        referer = selector.xpath('/html/body/div[8]/div[3]/div[2]/div[1]/form/div[1]/input[3]/@value').extract()[0]
        activationauth = selector.xpath('/html/body/div[8]/div[3]/div[2]/div[1]/form/div[1]/input[4]/@value').extract()[0]
        seccodehashs = selector.xpath('/html/body/div[8]/div[3]/div[2]/div[1]/form/div[1]/div/div/span/@id').extract()[0]
        seccodehash = str(seccodehashs).split('_')[1]
        name_zd = selector.xpath('/html/body/div[8]/div[3]/div[2]/div[1]/form/div[1]/div/div/div[1]/table/tr/th/label/@for').extract()[0]
        # print(name_zd)
        password1_zd = selector.xpath('/html/body/div[8]/div[3]/div[2]/div[1]/form/div[1]/div/div/div[2]/table/tr/th/label/@for').extract()[0]
        password2_zd = selector.xpath('/html/body/div[8]/div[3]/div[2]/div[1]/form/div[1]/div/div/div[3]/table/tr/th/label/@for').extract()[0]
        post_email_zd = selector.xpath('/html/body/div[8]/div[3]/div[2]/div[1]/form/div[1]/div/div/div[4]/table/tr/th/label/@for').extract()[0]
        name = name
        password1 = name
        password2 = name
        post_email = name + '@sina.com'
        # 下载验证码图片
        misc_url = 'https://bbs.6994.cn/misc.php?mod=seccode&update=81288&idhash=' + seccodehash
        res_misc = session.get(url=misc_url, headers=post_header)
        # -------------------------下面此处需要加入返回的cookies----------------------
        # 将CookieJar转为字典：
        cookies11 = requests.utils.dict_from_cookiejar(res_misc.cookies)
        # 会话加入cookies
        for kk2, vv2 in cookies11.items():
            # print(kk, vv)
            session.cookies.set(kk2, vv2)
        # --------------------------上面此处需要加入返回的cookies---------------------
        # 当前目录下创建img文件夹
        if os.path.isdir('img'):
            pass
        else:
            print("当前目录下不存在 img 文件夹，调用 mkdir 创建该文件夹")
            os.mkdir('img')
        path = os.path.dirname(__file__) + '\\' + 'img'
        pic_name = path + '\\' + 'misc.png'
        with open(pic_name, 'wb') as f:
            f.write(res_misc.content)
        print('验证码图片已下载')
        # 验证码识别
        # misc_str = dddd_ocr('img')
        # misc_str = baidu_ocr('img')
        misc_str = tuling_ocr('img')
        print('验证码是' + misc_str)
        post_data = {
            'regsubmit': 'yes',
            'formhash': formhash,
            'referer': referer,
            'activationauth':activationauth,
            name_zd: name,
            password1_zd: password1,
            password2_zd: password2,
            post_email_zd: post_email,
            'seccodehash': seccodehash,
            'seccodemodid': 'member::register',
            'seccodeverify': misc_str
        }
        # print(post_data)
        res2 = session.post(url=post_url, data=post_data, headers=post_header)  # 提交post数据
        # print(res2.text)
        # with open('1.html', 'w', encoding='utf-8') as f:
        #     f.write(res2.text)
        res_num1 = res2.text.find('验证码填写错误')
        res_num2 = res2.text.find('地址无效')
        res_num3 = res2.text.find('感谢您注册')
        res_num4 = res2.text.find('地址已被注册')
        # print(res_num)
        if res_num1 > 0:
            print('验证码填写错误')
        elif res_num2 > 0:
            print('email地址无效')
        elif res_num3 > 0:
            print(f'注册成功----------{name}')
            # -------注册成功保存cookies------
            # 当前目录下创建cookies文件夹
            if os.path.isdir('cookies'):
                pass
            else:
                print("当前目录下不存在 cookies文件夹，调用 mkdir 创建该文件夹")
                os.mkdir('cookies')
            path = os.path.dirname(__file__) + '\\' + 'cookies'
            cookie_name = path + '\\' + f'{name}.txt'
            # 写文件
            res_home = session.get('https://bbs.6994.cn/', headers=register_header)
            # with open('1.html', 'w', encoding='utf-8') as f:
            #     f.write(res_home.text)
            cookies11 = requests.utils.dict_from_cookiejar(session.cookies)  # 将CookieJar转为字典：
            with open(cookie_name, 'w', encoding='utf-8') as f:
                f.write(str(cookies11))
            # -------注册成功保存cookies------
            items.remove(name)
        elif res_num4 > 0:
            print(f'已被注册-------{name}')
            items.remove(name)
        sleep(5)
        print('')
        session.close()

if __name__ == '__main__':
    register()














