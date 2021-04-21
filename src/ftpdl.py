#!/usr/bin/python
# -*- coding:utf8 -*-


#！python3
#import scikit-image
from ftplib import FTP
import ftplib
import sys
import os
import socket
import logging
import datetime
import time

logFileName = '.\\Log\\' + datetime.datetime.now().strftime('%Y%m%d') + 'downloadFtpLog.txt'
logging.basicConfig(filename=logFileName, level=logging.DEBUG, format='%(asctime)s-%(levelname)s-%(message)s')
logging.info('===============ftp_download_the_files程序开始===============')

class Ftp:
    host1 = 'ftp.csindex.com.cn'
    host2 = 'ftp.csindex.cn'
    host3 = 'ftp.csindex.hk'
    username = 'csiaxzq'
    password = '56483256'

    def __init__(self):
        self.ftp = None

    def ftp_connect(self, host, username, password):
        '''连接ftp'''
        f = FTP()
        # 设置(被动 主动)模式
        # self.ftp.set_pasv(False)
        # 打开调试信息,0关闭
        f.set_debuglevel(2)
        try:
            # 连接ftp
            f.connect(host=host, port=20021)
        except BaseException as e:
            return None, '无法访问' + host + '的FTP服务:' + str(e)
        try:
            # 登录ftp
            f.login(username, password)
        except BaseException as e:
            # 退出
            f.quit()
            return None, '登录失败，请检查用户名和密码:' + str(e)
        return f, 'ftp登录' + host + '成功.'

    def get_ftp_object(self):
        ''''''
        ftp, msg = self.ftp_connect(Ftp.host1, Ftp.username, Ftp.password)

        if ftp is None:
            logging.info(msg + "\nNow, try to connect ftp server2.")
            ftp, msg = self.ftp_connect(Ftp.host2, Ftp.username, Ftp.password)
        #if ftp is None:
        #logging.info(msg + "\nNow, try to connect ftp server3.")
        #ftp, msg = self.ftp_connect(Ftp.host3, Ftp.username, Ftp.password)
        return ftp, msg

    def ftp_download_the_file(self, ftp, ftp_file_path, file_name, local_file_path):
        bufsize = 1024
        try:
            # 切换到服务器文件目录
            ftp.cwd(ftp_file_path)
            logging.info(f'{file_name}大小为: {ftp.size(file_name)}')
            if not os.path.isdir(local_file_path):
                os.mkdir(local_file_path)
            with open(local_file_path + '\\' + file_name, 'wb') as fp:
                # 使用二进制下载文件
                ftp.retrbinary('RETR ' + file_name, fp.write, bufsize)
            # 判断下载文件是否为0kb
            if self.is_file_size(local_file_path, file_name) == 0:
                return self.overload(ftp, ftp_file_path, file_name, local_file_path)
            if self.is_file_size(local_file_path, file_name) == 1:
                return True, '文件' + file_name + '下载成功.'
        except BaseException as e:
            logging.exception(f'第一次下载失败报错: {e}')
            ftp.close()
            return self.overload(ftp_file_path, file_name, local_file_path)

    def is_file_size(self,local_file_path, file_name):
        '''检查文件大小'''
        local_file = local_file_path + '\\' + file_name
        byte = os.path.getsize(local_file)
        if byte == 0:
            return 0
        return 1

    def overload(self, ftp_file_path, file_name, local_file_path):
        '''重新下载'''
        for _ in range(10):
            bufsize = 8192
            try:
                self.ftp, msg = self.get_ftp_object()
                if self.ftp is None:
                    logging.error('重试连接失败...')
                    continue
                self.ftp.cwd(ftp_file_path)
                logging.info(f'{file_name}大小为: {self.ftp.size(file_name)}')
                if not os.path.isdir(local_file_path):
                    os.mkdir(local_file_path)
                with open(local_file_path + '\\' + file_name, 'wb') as fp:
                    self.ftp.retrbinary('RETR ' + file_name, fp.write, bufsize)
                # self.ftp.set_debuglevel(0)
                # 判断下载文件是否为0kb
                if self.is_file_size(local_file_path, file_name) == 1:
                    return True, '文件' + file_name + '下载成功.'
            except BaseException as e:
                logging.exception(f'overload下载失败报错:{e} <<<2')
                # self.ftp.close()
            time.sleep(2)
        logging.info('下载文件大小: 0kb')
        return False, '文件' + file_name + '下载失败:'

    def ftp_download_the_files(self):
        '''业务下载逻辑'''
        self.ftp, msg = self.get_ftp_object()
        if self.ftp is None:
            logging.error('===============3个地址连接失败，程序退出===============')
            return '3个地址连接失败，程序退出,休眠后重试...'
        logging.info(f'{msg}')



if __name__ == '__main__':
    while 1:
        sleepTime = 10
        curTime = time.localtime()
        curHour = curTime.tm_hour
        if curHour >= 14 and curHour <= 20:
            try:
                result = Ftp().ftp_download_the_files()
                logging.error(f'{result} 2')
            except BaseException as e:
                logging.exception(e)
                continue
        logging.info('%s:%d秒', '现在开始睡眠', sleepTime)
        time.sleep(sleepTime)
        logging.shutdown()
        logging.info('=====================================')
