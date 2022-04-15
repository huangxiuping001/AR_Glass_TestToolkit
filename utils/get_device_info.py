import os
import re
import socket
import warnings
import uiautomator2 as u2


def get_device_Id(device_Id=""):

    if not (device_Id==""):
        return device_Id
    else:
        readDevice_Id = list(os.popen('adb devices'))

        try:
            device_Id = re.findall(r'^\w*\b', readDevice_Id[1])[0]
        except (RuntimeError,IndexError) as e:
            print(e)
        else:
            return device_Id

def init_uiautomator2(device_Id):
    cmd = "python -m uiautomator2 init --serial %s"%(device_Id)
    os.system(cmd)

def get_device_connect(device):
    device_Id = get_device_Id (device)
    device_connect = u2.connect(device_Id)
    if not device_connect.alive:
        warnings.warn ( "atx-agent is not alive, start again ...", RuntimeWarning )
        init_uiautomator2(device_Id)
    device_connect.healthcheck ()
    return device_connect

def get_wifi_state():
    """
    获取WiFi连接状态
    :return:0关闭，1开启，2飞行模式下关闭后开启，3开启状态由飞行模式关闭
    """
    cmd = 'adb shell settings get global wifi_on'
    message  = os.popen(cmd)
    wifi_state = message.readline().strip('\n')
    return wifi_state

def restore_wifi_state():
    """

    :return:
    """
    cmd = 'adb shell settings put global wifi_on 0'
    os.popen(cmd)

def get_bluetooth_state():
    """
    获取bluetooth连接状态
    :return:state,状态：1开启，0关闭
    """
    cmd = 'adb shell settings get global bluetooth_on'
    message  = os.popen(cmd)
    bluetooth_state = message.readline().strip('\n')
    return bluetooth_state

def get_Cont_bluetooth_list():
    '''

    :return:count 已配对设备数（待完善），判断值-1已取消保存，100已断开连接，1000已连接
    '''
    cmd = 'adb shell settings list global |findstr bluetooth_a2dp_sink_priority_1C'
    result = os.popen(cmd)
    count = len(result.readlines())
    return count


def get_mobile_state():
    '''
    获取移动网络连接状态
    :return: 1开启，0关闭
    '''
    cmd = "adb shell dumpsys telephony.registry | findstr mDataConnectionState"
    rerult = os.popen(cmd)
    mobile_state = rerult.readlines()
    state_list = [x.strip() for x in mobile_state]
    if state_list[0]==state_list[1]:
        return 0
    else:
        return 1


def get_SIMCard_state():
    '''
    返回SIM移动数据开启状态
    :return: 0未开启，1开启
    '''
    cmd = "adb shell settings get global mobile_data1"
    rerult = os.popen(cmd)
    SIMCard_state = rerult.readline().strip('\n')
    return SIMCard_state

def get_SoftCard_state():
    '''
    返回软卡流量开启状态
    :return: 0未开启，1开启
    '''
    cmd = "adb shell settings get global mobile_data2"
    rerult = os.popen(cmd)
    SoftCard_state = rerult.readline().strip('\n')
    return SoftCard_state


def get_airplan_state():
    '''

    :return:string 0未开启，1开启
    '''
    cmd= "adb shell settings get global airplane_mode_on"
    rerult = os.popen(cmd)
    airplan_state = rerult.readline().strip('\n')
    return airplan_state

def restore_airplan_state():
    """

    :return:
    """
    cmd= "adb shell settings put global airplane_mode_on 0"
    os.popen(cmd)

def get_voice_value():
    '''
    获取设备音量值
    :return:
    '''
    cmd ="adb shell settings get system volume_music_speaker"
    result = os.popen(cmd)
    voice_value = result.readlines()[0]
    return int(voice_value)

def set_voice_value(value):
    '''
    设置设备音量值
    :param value: （0~15）
    :return:
    '''
    cmd ="adb shell settings put system volume_music_speaker %s" %value
    os.popen(cmd)

def get_Bluetooth_voice_value():
    '''
    获取蓝牙音量值
    :return:
    '''
    cmd ="adb shell settings get system volume_music_bt_a2dp"
    result = os.popen(cmd)
    Bluetooth_voice_value = result.readlines()[0]
    return int(Bluetooth_voice_value)

def get_screen_value():
    '''
    获取屏幕亮度值
    :return:
    '''
    cmd ="adb shell settings get system screen_brightness"
    # cmd ="adb shell cat /sys/class/leds/lcd-backlight/brightness"
    result = os.popen(cmd)
    screen_value = result.readlines()[0]
    return int(screen_value)

def set_screen_value(value):
    '''
    设置屏幕亮度值
    :param value:（10~255）
    :return:
    '''
    cmd ="adb shell settings put system screen_brightness %s" %value
    os.popen(cmd)

def is_NetWork_OK(testserver):
    s=socket.socket()
    s.settimeout(3)
    try:
        status = s.connect_ex(testserver)
        if status == 0:
            s.close()
            return True
        else:
            return False
    except Exception as e:
        return False

if __name__ == '__main__':
   a = is_NetWork_OK(("www.baidu.com",443))
   print(a)