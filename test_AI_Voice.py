# coding:utf-8
"""
Created on 2022年4月2日
@author: 黄秀平
Content：将文本内容转换为音频播放，遍历excel中的内容
"""

from time import sleep
import pytest
import uiautomator2 as u2
import xlrd
import pyttsx3

# paste_image_path = "D:\\AR_Glass_TestToolkit\\paste_image\\" #粘贴译文截图路径
d = u2.connect()  # 设备号


def __TextToSpeech(text):
    engine = pyttsx3.init()
    volume = engine.getProperty('volume')
    rate = engine.getProperty('rate')

    engine.setProperty('volume', 1)
    # engine.setProperty('rate',0.5)
    print("开始播报...")
    engine.say(text)
    engine.runAndWait()  # 等待播报完毕
    engine.stop()  # 结束引擎


# def test01_OpenAssistant():
#     d.app_start('activity',"activity",use_monkey=True) #写入包名.启动语音助手
#     d.click('x','y')  #如果想通过边上常驻的启动，也可以使用坐标或元素


def test_PlaySpeech():
    data = xlrd.open_workbook(r'D:\AR_Glass_TestToolkit\AI_Voice_Sample.xls')  # 打开excel文件，读取数据
    worksheet1 = data.sheet_by_name(u'Sheet1')  # 根据工作表的名称获取里面的行列内容
    colNum = worksheet1.ncols
    for i in range(1, colNum):  # col[1] 就是第二列
        try:
            list1 = [str(worksheet1.cell_value(i, 1))]  # 建List
            a1 = ''.join(list1)  # 将List中的内容转为str类型
            text01 = a1
            print(u'正在播放:', text01)

            __TextToSpeech(text01)
            sleep(3)
        except:
            continue
        # assert 断言设备操作是否正常


if __name__ == '__main__':
    pytest.main()
