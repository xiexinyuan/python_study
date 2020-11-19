#!/usr/bin/python
# -*- coding:utf8 -*-
import utils
import errno
import logging
import random
import string
from os import getcwd
from os import mkdir
from os.path import basename
from sys import stdin, exit
import time
import re

from adbUtil import ADB
from veriCodeUtil import VeriCodeUtil
from uiautomator import device as d

from PIL import  Image



class register_163:

    user_name = None
    password = None
    phone = None
    adb = None
    verifCodeUtil = None

    mysql = None

    #初始化信息
    def __init__(self):
        print("初始化程序")
        self.adb = ADB()
        self.verifCodeUtil = VeriCodeUtil()
        self.mysql = utils.get_db_conn('localhost', 3306, 'root', 'root', 'test')
        #登录接码平台
        #utils.login_ssm();
    #同意用户须知
    def _agree_protocol(self):
        d(resourceId="com.netease.mail:id/alert_dialog_btnOK").click()

    #注册页面点击注册
    def _click_register(self):
        print("点击注册新邮箱，进入注册页面")
        d(text="注册新邮箱").click()


    # 填入数据
    def _input_text(self,text):
        self.adb.shell_command("input text " + text)

    #开始填入账号
    def _input_user_name(self):
        time.sleep(2)
        #随机生成用户名和密码
        user_name = utils.get_one_letters() + utils.random_str(11)
        print("生成用户名: " + user_name)
        #填入用户名
        self._input_text(user_name)
        #点击下一步
        # d.screen.on()
        d(text="下一步").click()
        time.sleep(2)
        #检查用户名是否已被占用
        # d.screen.on()
        um_is_has = d(text="该邮箱地址已被注册")
        # print(um_is_has)
        # 邮箱已被注册
        if um_is_has.exists:
            #点击确定
            d(text="确定").click()
            #清空用户名
            for num in range(0,20):
                d.press("delete")

            #重新执行注册逻辑
            self._input_user_name()

        else:
            #邮箱可以被注册
            self.user_name = user_name
            #点击下一步
            d(text="下一步").click()


    #输入密码页面
    def _input_password(self):
        time.sleep(2)
        print("输入密码")
        #随机生成密码
        self.pass_word = utils.get_one_letters() + utils.random_str(6) + utils.get_one_number()
        #点击第一行密码输入框
        d(resourceId="com.netease.mail:id/first_password").click()
        #键入密码
        self._input_text(self.pass_word)
        #点击第二行密码输入框
        d(resourceId="com.netease.mail:id/second_password").click()
        #键入密码
        self._input_text(self.pass_word)
        #点击下一步
        d(text="下一步").click()


    #输入手机号码
    def _input_phone(self):
        time.sleep(2)
        print("输入手机号")
        #获取手机号
        self.phone = utils.get_phone_no('网易')
        #输入手机号
        self._input_text(self.phone)
        #点击下一步
        d(text="下一步").click()
        time.sleep(2)
        if d(text="请填写图形验证码").exists:
            self._deal_veri_code()
            self._input_msg_code()
        else:
            #重新开始
            return

    #处理图形验证码
    def _deal_veri_code(self):
        time.sleep(2)
        #获取验证码
        verify_code = d(resourceId="com.netease.mail:id/iv_verify_code")
        #点击一次
        verify_code.click()
        time.sleep(5)
        #获取验证码坐标
        bounds = verify_code.info["bounds"]
        print(bounds)

        #截图保存
        self.adb.shell_command("screencap -p /sdcard/screen.png")
        self.adb.run_cmd("pull /sdcard/screen.png")
        im = Image.open("screen.png")
        #663,936,1026,918
        im = im.crop((bounds["left"],bounds["top"],bounds["right"],bounds["bottom"]))
        im.save("b.png")
        vcode = self.verifCodeUtil.base64_api("b.png")
        print(vcode)
        time.sleep(5)
        #输入验证码
        self._input_text(vcode)
        #点击确定
        d(text="确定").click()
        time.sleep(2)
        #验证码是否正确
        if d(text="验证码不正确，请重新填写").exists:
            #验证码不正确
            #点击确定
            d(text="确定").click()
            #重新输入验证码
            self._deal_veri_code()

    #短信验证码
    def _input_msg_code(self):
        time.sleep(5)
        #获取短信
        ver_code_str = utils.get_message("网易",self.phone)
        print("验证码内容：" + ver_code_str)
        var_code_arr = re.findall(r'\d+',ver_code_str)
        msg_code = " ".join(var_code_arr)
        print("获取到的验证码数字：" + msg_code)
        if len(msg_code) != 6:
            #5秒后重新获取验证码
            # time.sleep(5)
            self._input_msg_code()
        else:
            #输入验证码
            self._input_text(msg_code)
            #勾选同意协议
            d(resourceId="com.netease.mail:id/agree_check").click()
            #完成注册
            d(text="完成注册").click()
            self._save_msg()
    #保存注册信息
    def _save_msg(self):
        curr_time = utils.get_curr_time()
        insert_sql = "INSERT INTO email_163(user_name, pass_word, phone, create_time) " \
                     "VALUES ('{0}', '{1}', '{2}', '{3}')".format(self.user_name + '@163.com', self.pass_word, self.phone, curr_time)
        utils.execute_sql(self.mysql, insert_sql)
        self.start_app()

    #启动APP
    def start_app(self):
        # 启动db.exe位置
        self.adb.start_adb(r'D:\ChangZhi\dnplayer2\adb.exe')

        #杀死163邮箱程序
        self.adb.shell_command("pm clear com.netease.mail")
        #启动163邮箱程序
        self.adb.shell_command("am start -n com.netease.mail/com.netease.mobimail.activity.LaunchActivity")
        d.screen.on()
        #等待10秒
        time.sleep(10)
        #同意用户须知
        self._agree_protocol()
        #进入注册页面
        self._click_register()
        #执行输入用户名逻辑
        self._input_user_name()
        #输入密码
        self._input_password()
        #输入手机号
        self._input_phone()
        #self._deal_veri_code()
if __name__ == '__main__':
    # connect mysql
    # conn = utils.get_db_conn('localhost', 3306, 'root', 'root', 'test')
    # # login ssm
    # utils.login_ssm()
    # time.sleep(3)
    # # register begin
    # for i in range(1):
    #     user_name, pass_word, phone = register_163()
    #     if user_name is not None and pass_word is not None and phone is not None:
    #         save_email(conn, user_name, pass_word, phone)
    # # close mysql connect
    # conn.close()
    # utils.login_ssm_out()
    # register_app_163()
    # main();
    reg = register_163()
    reg.start_app()