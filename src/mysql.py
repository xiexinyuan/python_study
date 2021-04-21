#!/usr/bin/python
# -*- coding:utf8 -*-
import os
import pymysql
from sshtunnel import SSHTunnelForwarder


class mysql():
    _conn = None

    server = None

    env = os.getenv("ENV")

    def __init__(self):
        self.connect()

    def connect(self):
        '''
        self.client = MySQLdb.connect(host=self.server, port=self.port, user=self.user,
                                      passwd=self.password, db=self.database,
                                      charset=self.charset)
        # log.info('Connect to MySQL Server: ' + self.server)
        '''
        # print(self.env)
        # if self.env != "DEV":
        # self._conn = pymysql.connect(host="127.0.0.1",
        #                              port=3306,
        #                              user=config.MYSQL.get("user"),
        #                              password=config.MYSQL.get("pwd"),
        #                              db=config.MYSQL.get("db"))

        self._conn = pymysql.connect(host="127.0.0.1",
                                     port=3306,
                                     user='root',
                                     password='root',
                                     db='amazon')

        # else:
        # self.server = SSHTunnelForwarder(
        #     ('47.103.57.77', 15022),  # 指定ssh登录的跳转机的address，端口号
        #     ssh_username="yuangenping",  # 跳转机的用户
        #     ssh_pkey="src/rsa/id_rsa_yuangenping",  # 私钥路径
        #     ssh_private_key_password="lol123456",  # 密码（电脑开机密码）
        #     remote_bind_address=('localhost', 3306))
        # self.server.start()
        # self._conn = pymysql.connect(host='127.0.0.1',  # 此处必须是是127.0.0.1
        #                              port=self.server.local_bind_port,
        #                              user='yuangenping',  # 数据库用户名
        #                              passwd='Ygp@2020..',  # 数据库密码
        #                              db='yd_cloud',  # 数据库名称
        #                              charset='utf8')

        # server.close()#最后一定要server.close()，不然程序不会结束

    def close(self):
        self._conn.close()
        if self.env == "pro":
            self.server.close()

    # 执行sql
    def update_sql(self, sql):
        if self._conn is not None:
            try:
                cursor = self._conn.cursor()
                cursor.execute(sql)

                # 提交到数据库执行
                self._conn.commit()
            except Exception as e:
                print(e)
                # 发生错误时回滚
                self._conn.rollback()
            finally:
                # 关闭游标，关闭数据库连接
                cursor.close()
        else:
            print('db self._conn is null, please check now!!!')
            return

    # 执行sql
    def select_all(self, sql):
        if self._conn is not None:
            try:
                cursor = self._conn.cursor()
                cursor.execute(sql)

                # 提交到数据库执行
                return cursor.fetchall()
            except Exception as e:
                print(e)
                # 发生错误时回滚
                self._conn.rollback()
            finally:
                # 关闭游标，关闭数据库连接
                cursor.close()
        else:
            print('db self._conn is null, please check now!!!')
            return

    # 执行sql
    def select_one(self, sql):
        if self._conn is not None:
            try:
                cursor = self._conn.cursor()
                cursor.execute(sql)

                # 提交到数据库执行
                return cursor.fetchone()
            except Exception as e:
                print(e)
                # 发生错误时回滚
                self._conn.rollback()
            finally:
                # 关闭游标，关闭数据库连接
                cursor.close()
        else:
            print('db self._conn is null, please check now!!!')
            return
