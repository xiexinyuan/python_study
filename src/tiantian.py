

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

import adbutils

from veriCodeUtil import VeriCodeUtil
from LeiDianCMD import Dnconsole

from uiautomator import device as d

from PIL import  Image
adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
myAdb = adb.device();
serial = myAdb.serial;
class tiantianzhibo:

    user_name = None
    password = None
    phone = None
    verifCodeUtil = None
    ld:Dnconsole = None
    package = "com.topcavto.tqooclot"
    mysql = None

    #初始化信息
    def __init__(self):
        print("初始化程序")

        # self.verifCodeUtil = VeriCodeUtil()
        # self.mysql = utils.get_db_conn('localhost', 3306, 'root', 'root', 'test')

        self.ld = Dnconsole()
        #登录接码平台
        #utils.login_ssm();

    def reset_config(self):
        # self.ld.reboot(0)
        # print("退出模拟器")
        # self.ld.quit(0)
        # time.sleep(5)
        # print("配置新环境")
        # self.ld.config_new_player(0)
        # print("启动模拟器")
        # self.ld.launch(0)
        # #等待60秒
        # time.sleep(30)

        # #配置新环境
        #
        # #apk地址
        # apk_path = path.abspath('..') + '/apk/tiantianzhibo.apk'
        # apk_path = u""+apk_path.replace("\\","/")
        # print(apk_path)
        # print("卸载甜甜直播")
        # self.ld.uninstall(0,self.package);
        # time.sleep(5)
        # print("安装甜甜直播")
        # self.ld.install(0, apk_path)
        # time.sleep(10)
        self.start_app()
        # else:
        #     self.start_app()

    #启动APP
    def start_app(self):
        # 启动db.exe位置
        d.screen.on()
        # info = d(resourceId="com.netease.mail:id/tv_resend_msg_verify_code").info
        # print(info)
        # return
        #杀死163邮箱程序
        print("打开app")
        # self.adb.shell_command("pm clear " + self.package)
        #启动163邮箱程序  com.topcavto.tqooclot/com.aa.zz.cc.activity.MainActivity
        # self.ld.adb(0,"am start -n "+ self.package + "/com.aa.zz.cc.activity.MainActivity")
        adb.shell(serial, "am start -n "+ self.package + "/com.aa.zz.cc.activity.MainActivity")
        # d.screen.on()
        #等待10秒
        time.sleep(5)
        # #同意用户须知
        # self._agree_protocol()
        # #进入注册页面
        # self._click_register()
        # #执行输入用户名逻辑
        # self._input_user_name()
        # #输入密码
        # self._input_password()
        # #输入手机号
        # self._input_phone()

        self.homeHandler()

    # 填入数据
    def _input_text(self,text):
        adb.shell(serial,"input text " + text)

    def homeHandler(self):
        notice_sure_btn = d(resourceId=  self.package + ":id/sure_btn");
        if notice_sure_btn.exists:
            notice_sure_btn.click()

        time.sleep(2)
        # 点击直播菜单按钮
        print("点击直播菜单按钮")
        tab_buy_img = d(resourceId=  self.package + ":id/tab_buy_img");
        tab_buy_img.click();

        time.sleep(2)
        # 点击搜索按钮
        print("点击搜索按钮")
        live_search_iv = d(resourceId=  self.package + ":id/live_search_iv");
        live_search_iv.click();

        time.sleep(3)
        #输入搜索内容
        print("输入搜索内容")
        search_edit = d(resourceId=  self.package + ":id/search_edit");
        search_edit.click();
        self._input_text("61712495")
        time.sleep(1)
        d(resourceId=  self.package + ":id/search_tv").click()
        time.sleep(2)
        d(resourceId=  self.package + ":id/live_cover_linear").click();

        time.sleep(5)
        self.live_chat()

    #聊天室聊天
    def live_chat(self):
        print("开始发言")
        d(resourceId=  self.package + ":id/live_chat_tv").click();
        # 选中输入框
        time.sleep(2)
        print("选中输入框")
        d(resourceId=  self.package + ":id/live_chat_edit").click();

        #输入内容
        time.sleep(2)
        print("输入内容")
        self._input_text("在一分钟快三下注10元");

        # 发送
        time.sleep(2)
        print("发送")
        d(resourceId=  self.package + ":id/send_text_message_tv").click();

if __name__ == '__main__':
    reg = tiantianzhibo()
    try:
        print(1)
        reg.reset_config()
    except Exception as e:
        print('=========注册失败,执行下一个任务=========')
        print(e)
        reg.reset_config()