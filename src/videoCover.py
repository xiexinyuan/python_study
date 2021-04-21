#!/usr/bin/python
# -*- coding:utf8 -*-
import os
# import fnmatch
import re
import subprocess


gl_file_list = []
gl_failed_list = []
originPath = 'D:/dyVideo/origin'
targetPath = 'D:/dyVideo/cover'


def getFilesPath():
    # 获得指定目录中的内容
    file_list = os.listdir(originPath)
    for file_name in file_list:
        new_path = os.path.join(originPath, file_name)
        if os.path.isdir(new_path):
            getFilesPath(new_path)
        elif os.path.isfile(new_path):
            # 文件处理
            # if fnmatch.fnmatch(new_path, '*.(mp4|avi)'): # 匹配mp4格式
            #     # 视频处理
            #     fileProcessing(new_path)
            result = re.match(r".+\.(mp4|avi|mpeg|mov|flv|mpg|f4v|rmvb|mkv|ogg|asf|3gp|m4a)$", new_path)
            if result:
                gl_file_list.append(new_path)
                # fileProcessing(new_path)
        else:
            print("It's not a directory or a file.")


def fileProcessing(file_list):
    print("start----------------")
    codePre = "ffmpeg -threads 2 -i "
    # codeMid = " -vcodec h264 "
    # codeMid = " -vcodec libx264 -acodec aac -preset fast -b:v 2000k "
    codeMid = " -vcodec libx264 -acodec aac "
    for file_path in file_list:
        subname = file_path.split('.')
        print(subname)
        videoName = subname[0].split('\\');
        videoName = videoName[1]
        # print(videoName)
        # return
        output_path =   "{0}/{1}.mp4".format(targetPath,videoName)   # 处理后的文件路径
        command = codePre + file_path + codeMid + output_path
        print(command)
        file_name = os.path.basename(file_path).split('.')
        # result = os.system(command)
        # if(result != 0):
        #     gl_failed_list.append(file_path)
        #     print(file_name[0], "is failed-----", "result = ", result)
        # else:
        #     print("end------", file_name[0], "result = ", result)

        try:
            retcode = subprocess.call(command, shell=True)
            # retcode = os.system(command)
            if retcode == 0:
                print(file_name[0], "successed------")
            else:
                print(file_name[0], "is failed--------")
        except Exception as e:
            print("111")
            # print("Error:", e)

    print("---------------End all-----------------")
    print("failed:", gl_failed_list)


if __name__ =='__main__':
    getFilesPath()
    fileProcessing(gl_file_list)