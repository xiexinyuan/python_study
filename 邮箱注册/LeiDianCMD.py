import os
import shutil
import time
from xml.dom.minidom import parseString


class Dnconsole:
    # 请根据自己电脑配置
    console = 'D:\\ChangZhi\\dnplayer2\\dnconsole.exe  '
    ld = 'D:\\ChangZhi\\dnplayer2\\ld.exe '
    share_path = 'D:\\'

    # 获取模拟器列表
    @staticmethod
    def get_list():
        cmd = os.popen(Dnconsole.console + ' list2 ')
        text = cmd.read()
        cmd.close()
        info = text.split('\n')
        result = list()
        for line in info:
            if len(line) > 1:
                dnplayer = line.split(',')
                result.append(DnPlayer(dnplayer))
        return result

    # 获取正在运行的模拟器列表
    @staticmethod
    def list_running() -> list:
        result = list()
        all = Dnconsole.get_list()
        for dn in all:
            if dn.is_running() is True:
                result.append(dn)
        return result

    # 检测指定序号的模拟器是否正在运行
    @staticmethod
    def is_running(index: int) -> bool:
        all = Dnconsole.get_list()
        if index >= len(all):
            raise IndexError('%d is not exist' % index)
        return all[index].is_running()

    # 执行shell命令
    @staticmethod
    def dnld(index: int, command: str, silence: bool = True):
        cmd = Dnconsole.ld + '-s %d %s' % (index, command)
        cmd = u"" + cmd
        if silence:
            os.system(cmd)
            return ''
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 执行adb命令,不建议使用,容易失控
    @staticmethod
    def adb(index: int, command: str, silence: bool = False) -> str:
        cmd = Dnconsole.console + 'adb --index %d --command "%s"' % (index, command)
        if silence:
            os.system(cmd)
            return ''
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 安装apk 指定模拟器必须已经启动
    @staticmethod
    def install(index: int, path: str):
        # shutil.copy(path, Dnconsole.share_path + str(index) + '/update.apk')
        # time.sleep(1)
        # Dnconsole.dnld(index, 'pm install ' + path)
        cmd = Dnconsole.console + 'installapp --index %d --filename "%s"' % (index, path)
        process = os.popen(cmd)
    # 卸载apk 指定模拟器必须已经启动
    @staticmethod
    def uninstall(index: int, package: str):
        cmd = Dnconsole.console + 'uninstallapp  --index %d --packagename "%s"' % (index, package)
        process = os.popen(cmd)
        # return result

    # 启动App  指定模拟器必须已经启动
    @staticmethod
    def invokeapp(index: int, package: str):
        cmd = Dnconsole.console + 'runapp --index %d --packagename %s' % (index, package)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        print(result)
        return result

    # 停止App  指定模拟器必须已经启动
    @staticmethod
    def stopapp(index: int, package: str):
        cmd = Dnconsole.console + 'killapp --index %d --packagename %s' % (index, package)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 输入文字
    @staticmethod
    def input_text(index: int, text: str):
        cmd = Dnconsole.console + 'action --index %d --key call.input --value %s' % (index, text)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 获取安装包列表
    @staticmethod
    def get_package_list(index: int) -> list:
        result = list()
        text = Dnconsole.dnld(index, 'pm list packages')
        info = text.split('\n')
        for i in info:
            if len(i) > 1:
                result.append(i[8:])
        return result

    # 检测是否安装指定的应用
    @staticmethod
    def has_install(index: int, package: str):
        if Dnconsole.is_running(index) is False:
            return False
        return package in Dnconsole.get_package_list(index)

    # 启动模拟器
    @staticmethod
    def launch(index: int):
        cmd = Dnconsole.console + 'launch --index ' + str(index)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 启动模拟器
    @staticmethod
    def launchByName(name: str):
        cmd = Dnconsole.console + 'launch --name ' + name
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 关闭模拟器
    @staticmethod
    def quit(index: int):
        cmd = Dnconsole.console + 'quit --index ' + str(index)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 设置屏幕分辨率为1080×1920 下次启动时生效
    @staticmethod
    def set_screen_size(index: int):
        cmd = Dnconsole.console + 'modify --index %d --resolution 1920,1080' \
                                  ' ,480' % index
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 点击或者长按某点
    @staticmethod
    def touch(index: int, x: int, y: int, delay: int = 0):
        if delay == 0:
            Dnconsole.dnld(index, 'input tap %d %d' % (x, y))
        else:
            Dnconsole.dnld(index, 'input touch %d %d %d' % (x, y, delay))

    # 滑动
    @staticmethod
    def swipe(index, coordinate_leftup: tuple, coordinate_rightdown: tuple, delay: int = 0):
        x0 = coordinate_leftup[0]
        y0 = coordinate_leftup[1]
        x1 = coordinate_rightdown[0]
        y1 = coordinate_rightdown[1]
        if delay == 0:
            Dnconsole.dnld(index, 'input swipe %d %d %d %d' % (x0, y0, x1, y1))
        else:
            Dnconsole.dnld(index, 'input swipe %d %d %d %d %d' % (x0, y0, x1, y1, delay))

    # 复制模拟器,被复制的模拟器不能启动
    @staticmethod
    def copy(name: str, index: int = 0):
        cmd = Dnconsole.console + 'copy --name %s --from %d' % (name, index)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 添加模拟器
    @staticmethod
    def add(name: str):
        cmd = Dnconsole.console + 'add --name %s' % name
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 设置自动旋转
    @staticmethod
    def auto_rate(index: int, auto_rate: bool = False):
        rate = 1 if auto_rate else 0
        cmd = Dnconsole.console + 'modify --index %d --autorotate %d' % (index, rate)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 改变设备信息 imei imsi simserial androidid mac值
    @staticmethod
    def change_device_data(index: int):
        # 改变设备信息
        cmd = Dnconsole.console + 'modify --index %d --imei auto --imsi auto --simserial auto --androidid auto --mac auto' % index
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 改变CPU数量
    @staticmethod
    def change_cpu_count(index: int, number: int):
        # 修改cpu数量
        cmd = Dnconsole.console + 'modify --index %d --cpu %d' % (index, number)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    @staticmethod
    def get_cur_activity_xml(index: int):
        # 获取当前activity的xml信息
        Dnconsole.dnld(index, 'uiautomator dump /sdcard/Pictures/activity.xml')
        time.sleep(1)
        f = open(Dnconsole.share_path + '/activity.xml', 'r', encoding='utf-8')
        result = f.read()
        f.close()
        return result

    @staticmethod
    def get_user_info(index: int):
        xml = Dnconsole.get_cur_activity_xml(index)
        usr = UserInfo(xml)
        if 'id' not in usr.info:
            return UserInfo()
        return usr

    # 获取当前activity名称
    @staticmethod
    def get_activity_name(index: int):
        text = Dnconsole.dnld(index, '"dumpsys activity top | grep ACTIVITY"', False)
        text = text.split(' ')
        for i, s in enumerate(text):
            if len(s) == 0:
                continue
            if s == 'ACTIVITY':
                return text[i + 1]
        return ''

    # 等待某个activity出现
    @staticmethod
    def wait_activity(index: int, activity: str, timeout: int) -> bool:
        for i in range(timeout):
            if Dnconsole.get_activity_name(index) == activity:
                return True
            time.sleep(1)
        return False

    # 等待某个图片出现
    @staticmethod
    def wait_picture(index: int, timeout: int, template: str) -> bool:
        count = 0
        while count < timeout:
            Dnconsole.dnld(index, 'screencap -p /sdcard/Pictures/apk_scr.png')
            time.sleep(2)
            ret, loc = Dnconsole.find_pic(Dnconsole.share_path + '/apk_scr.png', template, 0.001)
            if ret is False:
                print(loc)
                time.sleep(2)
                count += 2
                continue
            print(loc)
            return True
        return False

    # 在当前屏幕查看模板列表是否存在,是返回存在的模板,如果多个存在,返回找到的第一个模板
    @staticmethod
    def check_picture(index: int, templates: list):
        Dnconsole.dnld(index, 'screencap -p /sdcard/Pictures/apk_scr.png')
        time.sleep(1)
        for i, t in enumerate(templates):
            ret, loc = Dnconsole.find_pic(Dnconsole.share_path + '/apk_scr.png', t, 0.001)
            if ret is True:
                return i, loc
        return -1, None

    def reboot(self,index: int):
        os.popen(Dnconsole.console + 'reboot --index ' + str(index))

    #配置一个新的模拟器
    def config_new_player(self,index: int):
        # result = os.popen(Dnconsole.console + ' getprop --index --key "phone.mac"' + str(index))
        # process = os.popen(Dnconsole.console + ' getprop --index --key "phone.mac"' + str(index))
        # result = process.read()
        # print(result)
        os.popen(Dnconsole.console + ' setprop --index ' + str(index) + ' --key "phone.imei" --value "auto" ')
        os.popen(Dnconsole.console + ' setprop --index ' + str(index) + ' --key "phone.imsi" --value "auto" ')
        os.popen(Dnconsole.console + ' setprop --index ' + str(index) + ' --key "phone.simserial" --value "auto" ')
        # os.popen(Dnconsole.console + ' setprop --index ' + str(index) + ' --key "phone.manufacturer" --value "asus" ')
        # os.popen(Dnconsole.console + ' setprop --index ' + str(index) + ' --key "phone.model" --value "ASUS_Z00DUO" ')
        # os.popen(Dnconsole.console + ' setprop --index ' + str(index) + ' --key "phone.pnumber" --value "13812345678" ')
        os.popen(Dnconsole.console + ' setprop --index ' + str(index) + ' --key "phone.androidid" --value "auto" ')
        os.popen(Dnconsole.console + ' setprop --index ' + str(index) + ' --key "phone.mac" --value "auto" ')


        os.popen(Dnconsole.console + ' modify --index ' + str(index) + ' --resolution 720,1280,320 --cpu 4 --memory 2048')



class DnPlayer(object):
    def __init__(self, info: list):
        super(DnPlayer, self).__init__()
        # 索引，标题，顶层窗口句柄，绑定窗口句柄，是否进入android，进程PID，VBox进程PID
        self.index = int(info[0])
        self.name = info[1]
        self.top_win_handler = int(info[2])
        self.bind_win_handler = int(info[3])
        self.is_in_android = True if int(info[4]) == 1 else False
        self.pid = int(info[5])
        self.vbox_pid = int(info[6])

    def is_running(self) -> bool:
        return self.is_in_android

    def __str__(self):
        index = self.index
        name = self.name
        r = str(self.is_in_android)
        twh = self.top_win_handler
        bwh = self.bind_win_handler
        pid = self.pid
        vpid = self.vbox_pid
        return "\nindex:%d name:%s top:%08X bind:%08X running:%s pid:%d vbox_pid:%d\n" % (
            index, name, twh, bwh, r, pid, vpid)

    def __repr__(self):
        index = self.index
        name = self.name
        r = str(self.is_in_android)
        twh = self.top_win_handler
        bwh = self.bind_win_handler
        pid = self.pid
        vpid = self.vbox_pid
        return "\nindex:%d name:%s top:%08X bind:%08X running:%s pid:%d vbox_pid:%d\n" % (
            index, name, twh, bwh, r, pid, vpid)


class UserInfo(object):
    def __init__(self, text: str = ""):
        super(UserInfo, self).__init__()
        self.info = dict()
        if len(text) == 0:
            return
        self.__xml = parseString(text)
        nodes = self.__xml.getElementsByTagName('node')
        res_set = [
            # 用户信息节点
        ]
        name_set = [
            'id', 'id', 'following', 'fans', 'all_like', 'rank', 'flex',
            'signature', 'location', 'video', 'name'
        ]
        number_item = ['following', 'fans', 'all_like', 'video', 'videolike']
        for n in nodes:
            name = n.getAttribute('resource-id')
            if len(name) == 0:
                continue
            if name in res_set:
                idx = res_set.index(name)
                text = n.getAttribute('text')
                if name_set[idx] not in self.info:
                    self.info[name_set[idx]] = text
                    print(name_set[idx], text)
                elif idx == 9:
                    self.info['videolike'] = text
                elif idx < 2:
                    if len(text) == 0:
                        continue
                    if self.info['id'] != text:
                        self.info['id'] = text
        for item in number_item:
            if item in self.info:
                self.info[item] = int(self.info[item].replace('w', '0000').replace('.', ''))

    def __str__(self):
        return str(self.info)

    def __repr__(self):
        return str(self.info)





if __name__ == '__main__':
    ld = Dnconsole()
    result = ld.get_list()
    print(result)