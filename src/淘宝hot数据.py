#!/usr/bin/python
# -*- coding:utf8 -*-
# 生成资源编码和md5
import hashlib
from pathlib import Path
import datetime
import os
import shutil
import paramiko
from PIL import Image


from src.mysql import mysql

class tbHotData(object):

    mysql: None

    txtFilePath: []

    def __init__(self,txtFilePath: []):
        self.mysql = mysql()
        self.txtFilePath = txtFilePath;
        if len(txtFilePath) == 0:
            print("目录为空")
            exit(0)

        self.handlerData();

    def getValue(self,value,default=""):
        if value == "undefined" or value == None or value == "": return default
        return value

    def saveHotData(self,unionId,fkCount,sales,minPrice,maxPrice,title,link,hotTime):
        clickTime = datetime.datetime.strptime(hotTime.strip(), "%Y-%m-%d %H:%M:%S")  # 字符串转化为date形式
        # infoLog(clickTime)
        insert_sql = "INSERT INTO hot_data(hot_id,title,fk_count,min_price,max_price,link,hot_time) " \
                     "VALUES ('{0}', '{1}', '{2}', '{3}','{4}','{5}','{6}')".format(unionId, title,fkCount,minPrice,maxPrice,link,clickTime)
        self.mysql.update_sql(insert_sql)

    def handlerData(self):
        for file in self.txtFilePath:

            txtFile = Path(file);
            if txtFile.is_file():
                # 读取txt数据
                with open(txtFile,"r",encoding="utf-8") as f:
                    lineNumber = 0;
                    for line in f.readlines():
                        lineNumber += 1
                        if lineNumber == 1: continue
                        infos = line.split("|")
                        print(infos)
                        unionId = self.getValue(infos[0],"");# 商品ID
                        fkCount = self.getValue(infos[1],"0"); #付款人数
                        sales = self.getValue(infos[2],0); #销量
                        minPrice = self.getValue(infos[3],0); #最低价
                        maxPrice = self.getValue(infos[4],0); #最高价
                        title = self.getValue(infos[5],""); # 标题
                        link = self.getValue(infos[6],""); #连接
                        hotTime = self.getValue(infos[7],""); #采集时间

                        fkCount = fkCount.replace("万","");
                        if fkCount.find(".") != -1:
                            fkCount = float(fkCount) * 10000

                        print("{0},{1},{2},{3},{4},{5},{6},{7}".format(unionId,fkCount,sales,minPrice,maxPrice,title,link,hotTime))
                        self.saveHotData(unionId,fkCount,sales,minPrice,maxPrice,title,link,hotTime)

if __name__ == '__main__':
    hotD = tbHotData(["C:\\Users\\yuan\\Desktop\\小白鞋女.txt"]);