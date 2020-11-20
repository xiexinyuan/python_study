#!/usr/bin/python
# -*- coding:utf8 -*-
import utils
import errno
import logging
import random
import string
from os import path
from os import getcwd
from os import mkdir
from os.path import basename
from sys import stdin, exit
import time
import re

from adbUtil import ADB
from veriCodeUtil import VeriCodeUtil
from LeiDianCMD import Dnconsole

from uiautomator import device as d
from PIL import  Image

#抖音注册程序
class  douyin_reg:
    user_name = None
    password = None
    phone = None
    adb = None
    verifCodeUtil = None
    ld:Dnconsole = None
    package = "com.ss.android.ugc.aweme"

    #初始化信息
    def __init__(self):
        print("初始化程序")
        self.adb = ADB()
        self.verifCodeUtil = VeriCodeUtil()
        self.mysql = utils.get_db_conn('localhost', 3306, 'root', 'root', 'test')
        self.ld = Dnconsole()
        #登录接码平台
        #utils.login_ssm();

    #保存注册信息
    def _save_msg(self):
        curr_time = utils.get_curr_time()
        insert_sql = "INSERT INTO email_163(user_name, pass_word, phone, create_time) " \
                     "VALUES ('{0}', '{1}', '{2}', '{3}')".format(self.user_name + '@163.com', self.pass_word, self.phone, curr_time)
        utils.execute_sql(self.mysql, insert_sql)
        self.start_app()


    #开始注册
    def start(self):
        #apk地址
        apk_path = path.abspath('..') + '/apk/douyin.apk'
        apk_path = u""+apk_path.replace("\\","/")
        # 启动db.exe位置
        self.adb.start_adb(r'D:\ChangZhi\dnplayer2\adb.exe')
        #杀死1程序
        self.adb.shell_command("pm clear " + self.package)
        print("卸载抖音")
        self.ld.uninstall(0,self.package);
        time.sleep(5)
        self.ld.config_new_player(0)
        time.sleep(3)
        print("安装抖音")
        self.ld.install(0, apk_path)

        time.sleep(20)
        print("启动抖音")
        #启动app
        self.adb.shell_command("am start -n "+ self.package + "/.account.business.login.DYLoginActivity")


if __name__ == '__main__':
    dy = douyin_reg()
    dy.start()