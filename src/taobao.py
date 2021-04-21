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

# from PIL import  Image


class taobao:


    startPkg = "com.taobao.taobao/com.taobao.tao.welcome.Welcome"

    #初始化信息
    def __init__(self):
        print("初始化程序")
        self.adb = ADB();
        self.adb.start_adb(r'D:\androidSDK\platform-tools\adb.exe')
        self.mysql = utils.get_db_conn('localhost', 3306, 'root', 'root', 'test');

    def lunchApp(self):
        self.adb.shell_command("am start -n {0}".format(self.startPkg))

    def killApp(self):
        self.adb.shell_command("pm clear {0}".format("com.taobao.taobao"))

    # 点击查询框
    def clickSearchInput(self):
        print("搜索")
        searchDom = d(resourceId="com.taobao.taobao:id/corner_icon")
        # print()
        searchDom.click()


    def start(self):
        # 启动淘宝
        # self.lunchApp();
        time.sleep(5);
        self.clickSearchInput()






if __name__ == '__main__':
    reg = taobao()
    try:
        reg.start()
    except Exception as e:
        print('=========注册失败,执行下一个任务=========')
        print(e)



