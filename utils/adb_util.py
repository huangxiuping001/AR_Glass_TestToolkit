# coding:utf-8

import subprocess
import os
import time
import re
import io
import logging
from wsgiref.validate import validator

# 需预先配置adb命令运行环境
command = "adb"


class ADB:
    """
    单个设备，可不传入参数device_id
    """
    
    def __init__(self, device_id=""):
        if device_id == "":
            self.device_id = ""
        else:
            self.device_id = "-s {0}".format(device_id)
        
        self.check_devices(device_id)
        self.adb_stdout('root')
        self.adb_stdout('remount')
    
    def adb(self, args):
        cmd = "{0} {1} {2}".format(command, self.device_id, str(args))
        logging.debug('ADB Command: {0}'.format(cmd))
        return subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
    
    def adb_stdout(self, args):
        return self.adb(args).stdout.read().strip().decode('utf-8')
    
    def shell(self, args):
        cmd = "{0} {1} shell {2}".format(command, self.device_id, str(args))
        logging.debug('ADB Shell Command: {0}'.format(cmd))
        return subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
    
    def shell_stdout(self, args):
        return self.shell(args).stdout.read().strip().decode('utf-8')
    
    def _fastboot(self, args):
        cmd = "{0} {1} {2}".format("fastboot", self.device_id, str(args))
        logging.debug('Fastboot Command: {0}'.format(cmd))
        return subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
    
    def fastboot(self, args):
        p = self._fastboot(args)
        stdout, stderr = p.communicate()
        logging.info(stdout.strip().decode('utf-8'))
    
    def cmd(self, command, cwd=None):
        logging.debug('Command: {0}'.format(command))
        p = subprocess.Popen(
            command,
            shell=True,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        stdout, stderr = p.communicate()
        logging.info(stdout.strip().decode('utf-8'))
    
    def check_devices(self, device_id=""):
        # 判断设备是否在device列表中
        devices = re.findall('(.+)	device', self.adb_stdout("devices"))
        
        if not devices:
            assert False, 'No Device Connected!'
        else:
            if device_id:
                assert device_id in devices, 'Device_id Error!'
            else:
                if len(devices) > 1:
                    assert False, 'More Than One Device Connected! '
                else:
                    assert True
        
        # 判断设备是否正常启动
        while True:
            status = self.shell_stdout('getprop sys.boot_completed')
            if status == '1':
                logging.info('Device Boot completed.')
                break
            else:
                if status:
                    logging.error(status)
                time.sleep(1)
    
    def get_pid(self, package_name):
        while True:
            pid = self.shell_stdout("pidof {0}".format(package_name))
            if 'error' in pid:
                logging.warning('Get PID of {0} Error. Msg: {1}'.format(package_name, pid))
                time.sleep(1)
            else:
                logging.debug('PID of {0} is: {1}'.format(package_name, pid))
                return pid
    
    def get_window(self, pattern='mCurrentFocus=(.+)'):
        windows = self.shell_stdout("dumpsys window windows")
        curretWindow = re.findall(pattern, windows)
        logging.debug('Current window: {}'.format(curretWindow))
        if curretWindow:
            return curretWindow[0].strip()
        else:
            return ''
    
    def get_model(self):
        model = self.shell_stdout("getprop ro.product.model")
        logging.info('Current Device Model: {0}'.format(model))
        return model
    
    def get_size(self):
        size = self.shell_stdout("wm size").strip("Physical size: ").split('x')
        logging.info('Current Device Size: {}'.format(size))
        return size
    
    def get_status(self):
        # 当前设备状态 1 未激活；0 已激活
        status = self.shell_stdout("getprop runtime.ifl.banstatusbar")
        logging.info('Current Device status: {0}'.format(status))
        return status
    
    def take_scr(self, scr_file=''):
        # 进行截图
        if not scr_file:
            scr_path = 'log/scr'
            if not os.path.exists(scr_path):
                os.makedirs(scr_path)
            scr_file = os.path.join(scr_path, time.strftime('%y%m%d%H%M%S')) + '.jpg'
        
        p = self.shell("screencap -p /sdcard/tmp.jpg")
        p.communicate()
        
        p = self.adb("pull /sdcard/tmp.jpg {0}".format(scr_file))
        stdout, stderr = p.communicate()
        logging.info(stdout.strip().decode('utf-8'))
        
        logging.info(u'Take ScreenShot: {0}'.format(scr_file))
    
    def logcat(self, logfile='log/logcat.log', dmesgfile='log/dmesg.log'):
        # 获取旧的pid
        pids = self.get_pid('logcat').split(' ')
        
        # 先清空logcat缓冲期日志
        self.adb("logcat -c")
        
        # 开启logcat
        self.adb('logcat -b all -v time > {0}'.format(logfile))
        
        # 开启后台日志
        # self.shell('"nohup logcat -b all -v time  -f /sdcard/logcat.log &"')
        
        # 获取dmesg日志
        self.shell('dmesg > {0}'.format(dmesgfile))
        
        # 获取新的pid
        new_pids = self.get_pid('logcat').split(' ')
        
        # 处理返回pid
        logcat_pid = ' '.join(list(set(new_pids) - set(pids)))
        logging.info('Logcat Pid: {0}'.format(logcat_pid))
        return logcat_pid
    
    def stop_logcat(self, logcat_pid=''):
        if not logcat_pid:
            logcat_pid = self.get_pid('logcat')
        
        self.shell('kill -9 {0}'.format(logcat_pid))
        logging.info('Kill Logcat Pid: {0}.'.format(logcat_pid))
    
    def wait_for_device(self):
        self.adb_stdout("wait-for-device")
        
        self.adb_stdout("root")
        time.sleep(1)
        
        # remount，并循环检测是否成功
        while True:
            p = self.adb("remount")
            stdout, stderr = p.communicate()
            logging.info(stdout.strip().decode('utf-8'))
            if stdout.strip().decode('utf-8') == 'remount succeeded':
                time.sleep(1)
                break
            elif stdout.strip().decode('utf-8') == 'Not running as root. Try "adb root" first.':
                self.adb_stdout("root")
                time.sleep(1)
            else:
                time.sleep(2)
    
    def wait_for_fastboot(self, device_id=""):
        # 判断设备是否在device列表中
        while True:
            devices = re.findall('(.+)	fastboot', self._fastboot("devices").stdout.read())
            
            if not devices:
                logging.debug('No Device Connected! Waiting for fastboot devices...')
                time.sleep(1)
            else:
                if device_id:
                    if device_id in devices:
                        logging.info("Device Connected! Device Id: {}".format(device_id))
                        break
                    else:
                        logging.debug('Device_id Error! Waiting for fastboot devices...')
                        time.sleep(1)
                else:
                    if len(devices) > 1:
                        assert False, 'More Than One Device Connected! '
                    else:
                        logging.info("Device Connected!")
                        break
    
    def kill_pkg(self, package_name):
        pid = self.get_pid(package_name)
        if pid:
            self.shell("kill -9 {}".format(pid))
    
    def get_cpu(self):
        # dumpsys cpuinfo
        p = self.shell("dumpsys cpuinfo")
        stdout, stderr = p.communicate()
        logging.debug(stdout.decode("utf-8"))
        out = io.StringIO(stdout.decode("utf-8"))
        for line in iter(out.readline, ''):
            line = line.strip()
            if 'TOTAL' in line:
                return float(line.split("%")[0])
    
    def get_ram(self):
        # cat /proc/meminfo
        import re
        meminfo = self.shell_stdout("cat /proc/meminfo")
        logging.debug(meminfo)
        memTotal = int(re.search("MemTotal:(.*)kB", meminfo).groups()[0].strip())
        memAvailable = int(re.search("MemAvailable:(.*)kB", meminfo).groups()[0].strip())
        memUsed = memTotal - memAvailable
        
        return memTotal, memUsed, memAvailable
    
    def get_rom(self):
        """
        计算底包ROM占用空间大小
        使用df获取 /dev 分区下，除 /data 及 /useretc 外其他分区总大小，指标为<6GB
        :return:
        """
        import re
        total_rom = {}
        used_rom = {}
        
        p = self.shell("df")
        stdout, stderr = p.communicate()
        logging.debug(stdout.decode("utf-8"))
        out = io.StringIO(stdout.decode("utf-8"))
        
        for line in iter(out.readline, ''):
            if '/dev' in line:
                line = line.strip()
                line = re.sub(" +", " ", line)
                if line.split(" ")[5] not in ['/data', '/useretc']:
                    total_rom[line.split(" ")[0]] = line.split(" ")[1]
                    used_rom[line.split(" ")[0]] = line.split(" ")[2]
        
        totalRom = sum([int(v) for v in total_rom.values()])
        usedRom = sum([int(v) for v in used_rom.values()])
        
        return totalRom, usedRom
    
    def get_fps(self, pkg_name='com.android.launcher3'):
        """
        根据dumpsys gfxinfo命令，计算fps
        :param pkg_name: 测试apk package name
        若在开发者模式中开启 Developer options -> Profile GPU rendering - > In adb shell dumpsys gfxinfo，则使用使用profile data计算fps;
        否则使用Janky frames rate计算
        :return:
        """
        results = self.shell_stdout("dumpsys gfxinfo {}".format(pkg_name))
        logging.debug("dumpsys gfxinfo:\n{}".format(results))
        
        frames = [x for x in results.split('\n') if validator(x)]
        frame_time = 16.67
        frame_count = 0
        janky_count = 0
        vsync_overtime = 0
        render_time = 0
        janky_rate = 0.0
        for frame in frames:
            if 'Janky frames' in frame:
                janky_rate = float(re.search("\((.*)\%\)", frame.strip()).groups()[0])
            
            time_block = re.split(r'\s+', frame.strip())
            if len(time_block) == 4:
                try:
                    render_time = float(time_block[0]) + float(time_block[1]) \
                                  + float(time_block[2]) + float(time_block[3])
                    frame_count += 1
                except Exception as e:
                    render_time = 0
            
            '''
            当渲染时间大于16.67，按照垂直同步机制，该帧就已经渲染超时
            那么，如果它正好是16.67的整数倍，比如66.68，则它花费了4个垂直同步脉冲，减去本身需要一个，则超时3个
            如果它不是16.67的整数倍，比如67，那么它花费的垂直同步脉冲应向上取整，即5个，减去本身需要一个，即超时4个，可直接算向下取整

            最后的计算方法思路：
            执行一次命令，总共收集到了m帧（理想情况下m=128），但是这m帧里面有些帧渲染超过了16.67毫秒，算一次jank，一旦jank，
            需要用掉额外的垂直同步脉冲。其他的就算没有超过16.67，也按一个脉冲时间来算（理想情况下，一个脉冲就可以渲染完一帧）

            所以FPS的算法可以变为：
            m / （m + 额外的垂直同步脉冲） * 60
            '''
            if render_time > frame_time:
                janky_count += 1
                if render_time % frame_time == 0:
                    vsync_overtime += int(render_time / frame_time) - 1
                else:
                    vsync_overtime += int(render_time / frame_time)
        
        if frame_count:
            fps = int(frame_count * 60 / (frame_count + vsync_overtime))
        else:
            fps = round(60 * (1 - janky_rate / 100.0), 2)
        
        logging.info("FPS: {}, Janky Rate: {}%".format(fps, janky_rate))
        return fps, janky_rate
    
    def get_version(self):
        version = self.shell_stdout("cat /proc/version").split("SMP PREEMPT")[-1].strip()
        logging.info("Get Kernel version: {}".format(version))
        return version
