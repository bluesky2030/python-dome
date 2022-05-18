'''
程序注册成功后，保存cookies到本地
通过selenium模拟过滑块登录，通过元素.screenshot方法保存背景图片，通过拿到源代码后requests方式保存透明滑块
提交用户名密码用的加载js方式，因为密码元素的send.keys无法传递变量
'''



#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from PIL import Image
import time
import base64
import requests
from datetime import datetime
import os
import ddddocr
import json
from parsel import Selector


# 传入selenium方法得到的cookies列表（如果是文件读入是字符串形式，用list(eval(。。。))转换），转换成session字典dict
def s_cookies_to_session(seleniumcookie):
    cookielist1 = seleniumcookie
    cookielist2 = []
    for dict_i in cookielist1:
        cookies_str1 = dict_i['name'] + '=' + dict_i['value']
        cookielist2.append(cookies_str1)
    cookies = {}
    for i in cookielist2:
        cookies[i.split('=')[0]] = i.split('=')[1]
    # print(cookies)
    return cookies

# 传入浏览器对象，注册用户名，保存cookies到文件
def get_cookie(wd, name):
    wd.get('https://www.108pc.com')
    coo = wd.get_cookies()
    # print(coo)  # 打印出cookie以后，将cookie复制
    dict_coo = s_cookies_to_session(coo)
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
    with open(cookie_name, 'w', encoding='utf-8') as f:
        f.write(str(dict_coo))
    # -------注册成功保存cookies------
    print(f'{name}--cookie已保存')


def register():
    # 当前目录下创建img文件夹
    if os.path.isdir('img'):
        print("")
    else:
        print("当前目录下不存在 img 文件夹，调用 mkdir 创建该文件夹")
        os.mkdir('img')
    # 获取当前路径img文件夹的path
    path = os.path.dirname(__file__) + '\\' + 'img'
    pic_name1 = path + '\\' + '1.png'    # 元素截图保存路径
    pic_name2 = path + '\\' + '2.png'    # 裁剪后保存路径
    pic_name3 = path + '\\' + '3.png'    # 滑块保存路径



    # 设置对象
    options = webdriver.ChromeOptions()
    # 手机模式
    mobile_emulation = {"deviceName": "iPhone 6"}
    options.add_experimental_option("mobileEmulation", mobile_emulation)
    # options.add_argument('--disable-blink-features=AutomationControlled')
    # 设置对象
    wd = webdriver.Chrome(service=Service('chromedriver.exe'), chrome_options=options)
    wd.implicitly_wait(10)

    # 生成用户名列表
    items = []
    for i in range(28, 501):
        item = 'qwer63167' + str(i)
        items.append(item)
    # 打开注册页面，填表-----第一次打开慢先运行
    url_register = 'https://www.108pc.com/member.php?mod=register'
    wd.get(url_register)
    sleep(10)
	
	
    # 循环执行，知道用户名列表为空
    while items:
        name = items[0]
        wd.get('https://www.108pc.com/member.php?mod=register')
        sleep(1)
        # 密码输入，元素方式不能传入变量，使用执行js方式输入
        # 例子 js = 'document.getElementsByClassName("px p_fre")[1].value="123456";'
        js = 'document.getElementsByClassName("px p_fre")[0].value=' + '"' + str(name) + '"' + ';'
        wd.execute_script(js)  # 执行js
        sleep(1)
        js = 'document.getElementsByClassName("px p_fre")[1].value=' + '"' + str(name) + '"' + ';'
        wd.execute_script(js)  # 执行js
        sleep(1)
        js = 'document.getElementsByClassName("px p_fre")[2].value=' + '"' + str(name) + '"' + ';'
        wd.execute_script(js)  # 执行js
        sleep(1)
        js = 'document.getElementsByClassName("px p_fre")[3].value=' + '"' + str(name) + '@sina.com' + '"' + ';'
        wd.execute_script(js)  # 执行js
        sleep(1)
        # input()
        button_zhuce = wd.find_element(By.XPATH, '/html/body/div[2]/div[2]/button[2]').click()  # 点击立即注册
        sleep(3)
        # 找到验证码图片位置，获取坐标及高、宽
        img = wd.find_element(By.XPATH, '/html/body/div[2]/div[1]/form/div/table/tbody/tr/td/div/div/div[2]/div[2]/div[1]/div[2]/div[2]/canvas')
        img.screenshot(pic_name1)
        # 读取图片，抠图保存
        photo1 = Image.open(pic_name1)
        photo2 = photo1.crop((68, 0, 300, 150))  # 左边多切掉68,多次测试
        photo2.save(pic_name2)
        # 保存滑块，透明图片不能用截图方式，先拿到该页面源码，再拿到图片地址，requests下载
        # print(wd.page_source)
        selector = Selector(wd.page_source)
        url_huakuais = selector.xpath('/html/body/div[2]/div[1]/form/div/table/tbody/tr/td/div/div/div[2]/div[2]/div[1]/div[1]/img/@src').extract()[0]
        url_huakuai = str(url_huakuais).replace('.webp', '.png')  # 滑块地址中把webp文件换成png
        # print(url_huakuai)
        header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
        }
        res_imghk = requests.get(url=url_huakuai, headers=header)
        with open(pic_name3, 'wb') as f:
            f.write(res_imghk.content)
        # --------------------ddddocr图像识别------------------
        det = ddddocr.DdddOcr(det=False, ocr=False)
        with open(pic_name3, 'rb') as f:
            target_bytes = f.read()
        with open(pic_name2, 'rb') as f:
            background_bytes = f.read()
        res = det.slide_match(target_bytes, background_bytes)
        x1 = res['target'][0]
        x2 = res['target'][2]
        distance = x2
        print(res['target'])
        # print(distance)
        button_huakuai = wd.find_element(By.CSS_SELECTOR, '#dx_captcha_basic_slider_1')  # 滑块
        button_tiao = wd.find_element(By.CSS_SELECTOR, '#dx_captcha_basic_bar-inform_1')  # 滑块条
        ActionChains(wd).drag_and_drop_by_offset(button_huakuai, distance, 0).perform()   # 拖动滑块
        # 等待几秒刷新，自动跳到主页，判断是否注册成功
        sleep(10)
        input()
        wd.get('https://www.108pc.com/home.php?mod=space&do=profile&mycenter=1')  # 访问个人主页
        sleep(3)
        html1 = wd.page_source
        htm1_num = html1.find('我的资料')
        if htm1_num > 0:
            print(f'注册成功---------{name}')
            get_cookie(wd, name)
            items.remove(name)  # 登录成功，移除用户名
            # 退出登录状态
            wd.get('https://www.108pc.com/home.php?mod=space&do=profile&mycenter=1')  # 访问个人主页
            sleep(3)
            # 拿到退出链接
            # https://www.108pc.com/member.php?mod=logging&action=logout&formhash=de2f135b&mobile=2
            html2 = wd.page_source
            selector1 = Selector(wd.page_source)
            url_outs = selector1.xpath('/html/body/div[2]/div[2]/ul/li[2]/a/@href').extract()[0]
            url_out = 'https://www.108pc.com/' + url_outs
            # print(url_out)
            # input()
            wd.get(url_out)
            # input()
            # wd.find_element(By.XPATH, '/html/body/div[2]/div[2]/ul/li[2]/a/text()').click()  # 点退出登录
            print('退出登录状态')
            sleep(1)
        # input()
        wd.get(url_register)

    # 循环结束，关闭浏览器
    wd.quit()




if __name__ == '__main__':
    register()






























