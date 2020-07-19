# -*- coding: utf-8 -*-
from selenium import webdriver
import time
import json
import os
import jsonlines

def list_to_json(list, json_file_name):
    """
    将list写入到json文件
    :param list:
    :param json_file_name: 写入的json文件名字
    :param json_file_save_path: json文件存储路径
    :return: null
    """
    with open(json_file_name, 'w', encoding='utf-8') as f:
        json.dump(list, f, ensure_ascii=False)

def json_to_jsonl(input_path, output_path):
    n = 0
    with open(input_path, 'r', encoding="utf-8") as rf:
        with jsonlines.open(output_path, 'w') as wf:
            data_list = json.load(rf)
            for data in data_list:
                print(data)
                n += 1
                wf.write(data)
    print("总数据：", n, '条')


class Sina:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        #self.login()

    # 模拟登陆
    def login(self):
        driver = webdriver.Firefox(executable_path="geckodriver.exe")
        #webdriver.Chrome(executable_path='chromedriver.exe')
        # wait 10 seconds if timeout this method will fail
        driver.get('https://s.weibo.com')
        time.sleep(5)

        print("开始模拟登陆登录")
        driver.find_element_by_css_selector('div.gn_login > ul > li:nth-child(3) > a').click()
        nowhandle = driver.current_window_handle
        driver.switch_to.window(nowhandle)
        
        print("输入用户名")
        driver.find_element_by_css_selector(#layer_15951705058081 > div.content > div.layer_login_register_v2.clearfix > div:nth-child(3) > div.item.username.input_wrap > input
            'div.layer_login_register_v2.clearfix > div:nth-child(3) > div.item.username.input_wrap > input').click()
        driver.find_element_by_css_selector(
            'div:nth-child(3) > div.item.username.input_wrap > input').send_keys(self.username)
        
        print('输入密码')
        driver.find_element_by_css_selector(
            'div:nth-child(3) > div.item.password.input_wrap > input').send_keys(self.password)
        driver.find_element_by_css_selector('div:nth-child(3) > div:nth-child(6) > a').click()
        
        # wait loginpage loading
        time.sleep(30)
        print('登陆成功')
        cookies = driver.get_cookies()
        cookie_dict = {}
        for cookie in cookies:
            if 'name' in cookie.keys() and 'value' in cookie.keys():
                cookie_dict[cookie['name']] = cookie['value']
        with open('./cookies.txt', 'w') as f:
            # 保存cookies到本地
            f.write(json.dumps(cookies))
            print("保存成功")
        driver.close()
        return cookie_dict

    # read cookie from location
    def get_cookie_cache(self):
        cookies_dict = {}
        if os.path.exists('cookies.txt'):
            # 如果本地有cookies文件，则读取本地cookies，否则返回空
            print('读取本地cookies')
            with open('./cookies.txt', 'r') as f:
                for i in json.loads(f.read()):
                    if 'name' in i.keys() and 'value' in i.keys():
                        cookies_dict[i['name']] = i['value']
        else:
            return cookies_dict
        return cookies_dict

    # get cookies,if not exit cookie ,will restart login
    def get_cookies(self):
        # 先从本地获取cookies
        cookie_dict = self.get_cookie_cache()
        if not cookie_dict:
            # 从本地返回的cookies为空则从网上获取cookies
            cookie_dict = self.login()
        return cookie_dict

    def open_all_text(self, driver, selector):
        """
        判断有没有展开全文
        :param node:
        :return:
        """
        # 如果需要展开全文，点击后提取文本
        if driver.find_element_by_css_selector(selector + '2)').text.endswith('展开全文c'):
            for i in range(2, 5):
                if driver.find_element_by_css_selector(selector + '2)') \
                        .find_element_by_css_selector('a:nth-child(' + str(i) + ')').text.endswith('展开全文c'):
                    driver.find_element_by_css_selector(selector + '2)'). \
                        find_element_by_css_selector('a:nth-child(' + str(i) + ')').click()
                    return True
        else:
            return False

    def search_content(self, content, total_page):
        news_list = []
        cookies = self.get_cookies()
        # 先访问一遍目标网站
        driver = webdriver.Firefox(executable_path="geckodriver.exe")
        driver.get('https://s.weibo.com/weibo/' + '%23' + content + '%23')

        #这一步非常重要，将用户登录的cookies写入session会话中
        for k, v in cookies.items():
            # 添加cookies
            driver.add_cookie({'name': k, 'value': v})
            # print(k + ":" + v)

        print("添加完成cookie……")
        print("开始访问……")
        # 再次访问目标网站，模拟登录成功
        driver.get('https://s.weibo.com/weibo/' + '%23' + content + '%23')
        time.sleep(10)
        for i in range(total_page):
            if i != 0:
                driver.get('https://s.weibo.com/weibo/' + '%23' + content + '%23&page=' + str(i + 1))
                print('当前page', i + 1, ';', '已有数据', len(news_list))
                time.sleep(10)

            for j in range(1, 24):# 下面的selector就是一种拼接方式，很随意，可以最大化的获取到页面信息，也可以做其他尝试
                selector = 'div:nth-child(' + \
                           str(j) + ') > div > div.card-feed > div.content > p:nth-child('
                try:
                    if self.open_all_text(driver, selector):
                        jq_text = driver.find_element_by_css_selector(selector + '3)').text.replace('收起全文d', '')
                    else:
                        jq_text = driver.find_element_by_css_selector(selector + '2)').text
                    news_list.append(jq_text)
                except:
                    pass

        json_file_name = 'news' + str(len(news_list)) + '.json'
        list_to_json(news_list, json_file_name)# 将获取到的信息保存到session文件中，命名规则为news+信息条数
        return json_file_name


if __name__ == "__main__":
    username = 'your_username'
    password = 'your_password'

    sina = Sina(username=username, password=password)
    #sina.login()
    json_file_name = sina.search_content('娱乐新闻', total_page=5)
    json_to_jsonl(json_file_name, json_file_name.strip('.json')+'.jsonl')
