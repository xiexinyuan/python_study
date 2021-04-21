#!/usr/bin/python
# -*- coding:utf8 -*-
import requests
import datetime
import random
import string
import pymysql

import time
# 导入自动化插件
from selenium import webdriver

u_phone_no = '19520697139'
u_pwd = 'lol12345'


# 初始化谷歌浏览器
def init_chrome():
    chromeOptions = webdriver.ChromeOptions()
    # 设置浏览器代理
    # chromeOptions.add_argument("--proxy-server=socks5://47.242.26.6:24000")
    # 生成谷歌浏览器
    driver = webdriver.Chrome(options=chromeOptions)
    return driver

# 初始化IE浏览器
def init_IE():
    chromeOptions = webdriver.Firefox()
    # 设置浏览器代理
    # chromeOptions.add_argument("--proxy-server=socks5://47.242.26.6:24000")
    # 生成谷歌浏览器
    driver = webdriver.Chrome(options=chromeOptions)
    return driver


# 生成指定长度的随机字符串
def random_str(length):
    return ''.join(random.sample(string.ascii_letters + string.digits, length))


# 获取a-z/A-Z中的任意一字符
def get_one_letters():
    return random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")


# 获取0-9中的任意一数字
def get_one_number():
    return random.choice("0123456789")


# 获取当前时间
def get_curr_time():
    return datetime.datetime.now()


# 获取数据库连接
def get_db_conn(host, port, user_name, password, db_name):
    return pymysql.connect(host=host,
                           port=port,
                           user=user_name,
                           password=password,
                           db=db_name)


# 执行sql
def execute_sql(conn, sql):
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            # 提交到数据库执行
            conn.commit()
        except Exception as e:
            print(e)
            # 发生错误时回滚
            conn.rollback()
        finally:
            # 关闭游标，关闭数据库连接
            cursor.close()
    else:
        print('db conn is null, please check now!!!')
        return


# 登录接码平台
def login_ssm():
    url = 'http://api.xunyaosoft.com/zc/zhicode/api.php?code=signIn&uPhoneNo=' \
          + u_phone_no + '&uPassword=' + u_pwd
    requests.get(url).text


# 获取可用短信余量
def get_ssm_count():
    url = 'http://api.xunyaosoft.com/zc/zhicode/api.php?code=getLeftNum&uPhoneNo=' + u_phone_no + '&uPassword=' + u_pwd
    return requests.get(url).text


# 获取一个号码
def get_phone_no(pro_name):
    url = 'http://api.xunyaosoft.com/zc/zhicode/api.php?code=getPhoneNo&projName=' \
          + pro_name + '&uPhoneNo=' + u_phone_no + '&uPassword=' + u_pwd
    return requests.get(url).text


# 获取短信
def get_message(pro_name, phone_no):
    url = 'http://api.xunyaosoft.com/zc/zhicode/api.php?code=getMsg&uPhoneNo=' \
          + u_phone_no + '&uPassword=' + u_pwd + '&projName=' + pro_name + '&phoneNo=' + phone_no
    return requests.get(url).text


# 发送短信
def send_msg(send_phone_no, to_phone_no, message):
    url = 'http://api.xunyaosoft.com/zc/zhicode/api.php?code=sendMsg&phoneNo=' \
          + send_phone_no + '&sendToPhoneNo=' + to_phone_no + '&sendMsg=' + message + '&uPhoneNo=' \
          + u_phone_no + '&uPassword=' + u_pwd
    return requests.get(url).text


# 把号码放入黑名单
def block_phone_no(phone_no):
    url = 'http://api.xunyaosoft.com/zc/zhicode/api.php?code=block&uPhoneNo=' \
          + u_phone_no + '&uPassword=' + u_pwd + '&phoneNo=' + phone_no
    return requests.get(url).text


# 接码平台登出
def login_ssm_out():
    url = 'http://api.xunyaosoft.com/zc/zhicode/api.php?code=signOut&uPhoneNo=' \
          + u_phone_no + '&uPassword=' + u_pwd
    return requests.get(url).text


# main方法  程序入口
if __name__ == '__main__':
    # user_name = get_on_letters() + random_str(11)
    # pass_word = get_on_letters() + random_str(11)
    # curr_time = get_curr_time()
    # # 插入语句
    # conn = get_db_conn('localhost', 3306, 'root', 'root', 'amazon')
    # insert_sql = "INSERT INTO email_163(user_name, pass_word, create_time) " \
    #              "VALUES ('{0}', '{1}', '{2}')".format(user_name + '@163.com', pass_word, curr_time)
    # execute_sql(conn, insert_sql)
    # conn.close()
    # print('insert success')

    login_ssm()
    time.sleep(5)
    count = get_ssm_count()
    print(count)
    time.sleep(5)
    pro_name = '简书'
    phone_no = get_phone_no(pro_name)
    print(phone_no)
    time.sleep(5)
    msg = '222'
    #to_phone = '106981630163222'
    to_phone = '15083560287'
    resp = send_msg(phone_no, to_phone, msg)
    print(resp)
    time.sleep(5)
    resp = login_ssm_out()
    print(resp)
