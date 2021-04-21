#!/usr/bin/python
# -*- coding:utf8 -*-

from moviepy.editor import *

if __name__ == '__main__':
    # 从本地载入视频myHolidays.mp4并截取00:00:50 - 00:00:60部分
    clip = VideoFileClip("D:\\dyVideo\\cover\\naruto.mp4").subclip(50, 60)
    clip.ipython_display(width=280)


