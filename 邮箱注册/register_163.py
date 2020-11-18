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
from ElementUtil import Element, Event
from PIL import  Image

# 将用户密码插入mysql
def save_email(conn, name, pwd, phone):
    curr_time = utils.get_curr_time()
    insert_sql = "INSERT INTO email_163(user_name, pass_word, phone, create_time) " \
                 "VALUES ('{0}', '{1}', '{2}', '{3}')".format(name + '@163.com', pwd, phone, curr_time)
    utils.execute_sql(conn, insert_sql)


# 注册163邮箱
def register_163():
    try:
        driver = utils.init_chrome()
        # driver = utils.init_IE()
        # 发送请求 打开注册页面
        driver.get('https://mail.163.com/register/index.htm?from=163mail')
        # 随机生成用户名和密码
        user_name = utils.get_one_letters() + utils.random_str(11)
        pass_word = utils.get_one_letters() + utils.random_str(6) + utils.get_one_number()

        # 定位元素框 填写用户名密码
        driver.find_element_by_id('username').send_keys(user_name)
        # 用户名是否有效
        user_name_tip_div = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/div[2]/div[1]/div[3]')
        tip_display = user_name_tip_div.is_displayed()
        if tip_display:
            return None, None, None

        # 填写密码
        driver.find_element_by_id('password').send_keys(pass_word)
        # 密码是否有效
        pwd_tip_div = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/div[2]/div[2]/div')
        pwd_tip = pwd_tip_div.get_attribute('innerText')
        err_msg = '密码过于简单，请尝试“字母+数字”的组合'
        if pwd_tip == err_msg:
            return None, None, None

        # 对接接码平台 获取电话和验证码
        phone = utils.get_phone_no('简书')
        driver.find_element_by_id("phone").send_keys(phone)
        time.sleep(3)
        # 电话是否有效
        phone_tip_div = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/div[2]/div[3]/div[2]')
        phone_tip = phone_tip_div.get_attribute('innerText')
        err_msg = '该手机号关联帐号太多'
        if phone_tip == err_msg:
            # 拉黑当前手机号并退出
            utils.block_phone_no(phone)
            return None, None, None

        # 点击同意服务条款
        driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/div[2]/div[4]/span').click()
        time.sleep(2)

        # 点击手动发送
        driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/div[2]/div[3]/div[1]/div[1]/div[2]/a').click()
        time.sleep(3)
        show = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/div[2]/div[3]/div[1]/div[2]').is_displayed()
        if show:
            # 获取收信人号码
            to_phone_span = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/div[2]/div[3]/div[1]/div[2]/div[2]/p[2]/span')
            to_phone = to_phone_span.get_attribute('innerText')
            # 获取要发送的内容
            send_msg_span = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/div[2]/div[3]/div[1]/div[2]/div[2]/p[1]/span')
            send_msg = send_msg_span.get_attribute('innerText')
            # 发送验证短信
            utils.send_msg(phone, to_phone, send_msg)
        else:
            return None, None, None
        time.sleep(5)
        # 点击立即注册按钮
        driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/div[2]/div[5]/a[1]').click()
        time.sleep(3)
        ssm_tip_div = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/div[2]/div[3]/div[2]')
        ssm_tip = ssm_tip_div.get_attribute('innerText')
        err_msg = '系统未收到短信，请检查手机号是否正确或重新发送短信'
        if ssm_tip == err_msg:
            print(err_msg)
            return None, None, None

        return user_name, pass_word, phone

    except Exception as e:
        print('=========注册失败,执行下一个任务=========')
        print(e)
    finally:
        driver.close()


def register_app_163(adb):
    codeUtil = VeriCodeUtil()
    eleUtil = Element()
    evevt = Event()
    adb.shell_command("am start -n com.netease.mail/com.netease.mobimail.activity.LaunchActivity")
    # 随机生成用户名和密码
    user_name = utils.get_one_letters() + utils.random_str(11)
    pass_word = utils.get_one_letters() + utils.random_str(6) + utils.get_one_number()
    time.sleep(10)
    print("点击注册")
    #点击注册
    regBtn = eleUtil.findElementByName(u"注册新邮箱")
    # adb.shell_command("input tap " + regBtn[0] + " " + regBtn[1])
    evevt.touch(regBtn[0],regBtn[1])
    return
    time.sleep(2)
    #输入账号
    print("输入账号")
    adb.shell_command("input text " + user_name)
    print("账号输入完毕,点击下一步")
    adb.shell_command("input tap 538 660")

    #密码
    time.sleep(2)
    print("密码输入")
    adb.shell_command("input text " + pass_word)
    print("再次输入密码")
    adb.shell_command("input tap 285 615")
    adb.shell_command("input text " + pass_word)
    print("密码输入完毕，点击下一步")
    adb.shell_command("input tap 542 822")

    #手机号输入
    time.sleep(2)
    #点击输入框
    print("点击手机号码输入框")
    adb.shell_command("input tap 575 747")
    # 对接接码平台 获取电话和验证码
    phone = utils.get_phone_no('网易')
    print("获取到手机号码: "+ phone)
    adb.shell_command("input text " + phone)
    adb.shell_command("input tap 516 930")
    # time.sleep(10)
    # input("input: ")

    time.sleep(1)
    print("更换一次验证码")
    adb.shell_command("input tap 796 979")

    print("输入动态验证码")
    time.sleep(2)
    adb.shell_command("screencap -p /sdcard/screen.png")
    adb.run_cmd("pull /sdcard/screen.png")
    im = Image.open("screen.png")
    print(im)
    #663,936,1026,918
    im = im.crop((663,936,918,1026))
    im.save("b.png")
    vcode = codeUtil.base64_api("b.png")
    print(vcode)
    adb.shell_command("input tap 356 981")
    adb.shell_command("input text " + vcode)
    adb.shell_command("input tap 766 1190")

    # checkCode = 1
    # while checkCode == 1:
    e = eleUtil.findElementById("alert_dialog_content_msg")
    print(e)


    print("下一步")
    print("点击输入验证码框")
    time.sleep(10)
    adb.shell_command("input tap 203 451")
    ver_code_str = utils.get_message("网易",phone)
    var_code_arr = re.findall(r'\d+',ver_code_str)
    print(var_code_arr)
    ver_code = " ".join(var_code_arr)
    print("获取到的验证码：" + ver_code)
    adb.shell_command("input text "+ ver_code)
    print("点击同意协议")
    adb.shell_command("input tap 116 776")
    print("点击完成注册")
    adb.shell_command("input tap 577 644")


def  register_app_1632(adb):
    codeUtil = VeriCodeUtil()
    # codeUtil.base64_api
    # e1 = eleUtil.findElementById("iv_verify_code")
    # print(e1)
    # dirver
    adb.shell_command("screencap -p /sdcard/screen.png")
    adb.run_cmd("pull /sdcard/screen.png")
    im = Image.open("screen.png")
    print(im)
    #663,936,1026,918
    im = im.crop((663,936,918,1026))
    im.save("b.png")
    vcode = codeUtil.base64_api("b.png")
    print(vcode)

def main():
    adb = ADB()

    # eleUtil = Element()

    # check_code(codeUtil)
    # set ADB path, using a couple of popular addresses.
    # 设置adb。exe位置
    adb.set_adb_path(r'D:\androidSDK\platform-tools\adb.exe')

    print("[+] Using PyADB version %s" % adb.pyadb_version())

    # verity ADB path
    if not adb.check_path():
        print("ERROR")
        exit(-2)
    print("OK")

    # print ADB Version
    print("[+] ADB Version: %s" % adb.get_version())

    print("")

    # restart server (may be other instances running)
    print("[+] Restarting ADB server...")
    try:
        adb.restart_server()
    except Exception as err:
        print("\t- ERROR\n", err)
        exit(-3)

    # get detected devices
    while True:
        try:
            devices = adb.get_devices()
        except adb.PermissionsError:
            devices = None
            print("You haven't enough permissions!")
            exit(-3)

        if devices:
            print("OK")
            break

        # no devices connected
        print("No devices connected")
        print("[+] Waiting for devices...")
        adb.wait_for_device()

    # this should never be reached
    if len(devices) == 0:
        print("[+] No devices detected!")
        exit(-4)

    # show detected devices
    i = 0
    for dev in devices:
        print("\t%d: %s" % (i, dev))
        i += 1

    # if there are more than one devices, ask to the user to choose one of them
    if i > 1:
        dev = i + 1
        while dev < 0 or dev > int(i - 1):
            # print("\n[+] Select target device [0-%d]: " % int(i - 1), end=' ')
            dev = int(stdin.readline())
    else:
        dev = 0

    # set target device
    try:
        adb.set_target_device(devices[dev])
    except Exception as e:
        print("\n[!] Error: " % e)
        exit(-5)

    print("\n[+] Using \"%s\" as target device" % devices[dev])

    # check if 'su' binary is available

    try:
        supath = adb.find_binary("su")
    except ADB.AdbException as err:
        if str(err) != "'su' was not found":
            print("Error: %s" % err)
            exit(-6)
        supath = None

    if supath is not None:
        # 'su' binary has been found

        print("[+] Checking if 'su' binary can give root access:")
        print(supath)
        try:
            rootid = adb.shell_command('%s -c id' % supath)
            print(rootid)
            # if 'root' in rootid.replace('(', ')').split(')'):
            #     # it can provide root privileges
            #     print("\t- Yes")
            #     register_app_163(adb)
            # else:
            #     print("\t- No: %s" % rootid)
            register_app_163(adb)
        except adb.AdbException as err:
            print("\t- No: %s" % err)
            register_app_163(adb)
    else:
        print("Not found.")
        # get_whatsapp_nonroot(adb)
    exit(0)

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
    main();