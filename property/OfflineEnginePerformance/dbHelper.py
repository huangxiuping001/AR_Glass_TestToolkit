# -*- coding: utf-8 -*-ePerf
import os

import numpy as np

from property.OfflineEnginormance.dbtools import DbTools

import pyecharts.options as opts
from pyecharts.charts import Bar
from pyecharts.charts import Line
from pyecharts.globals import ThemeType

from pyecharts.components import Table
from pyecharts.options import ComponentTitleOpts

class DbHelper(object):

    def __init__(self, user = 'zbdai'):
        self.db = DbTools(user)

    def readFileAndCache(self, fileName, product, rom_version, scene, process=[]):
        if not os.path.exists(fileName):
            print("File not exist!")
            return

        data_list = np.loadtxt(fileName, skiprows=1, unpack=True)

        if type(data_list[0]) is not np.ndarray:
            data_list = [data_list]

        i = 0
        for col_item in data_list:
            c_min = min(col_item)
            c_max = max(col_item)
            c_mid = np.mean(col_item)

            c_mid = np.around(c_mid, 2)

            self.db.insert(product, rom_version, scene,process[i], c_min, c_mid, c_max)
            i += 1

    def readFilesAndCache(self, dir, product, rom_version, process = []):
        if not os.path.isdir(dir):
            print("Path not a folder!")
            return

        for file in os.listdir(dir):
            scene = file.split('.')[0]

            self.readFileAndCache(dir + '/' + file, product, rom_version, scene, process)

    # arr: List[BaseParams] 需要比较的列表，可以是多项, type ：bar 柱状图 table：表格
    def compare(self, arr, title, subtext = "分别按最小值、均值、最大值进行对比",
                type = 'bar',  fileName = ''):
        if not arr:
            print("arr is empty!")
            return
        c_list = []

        for param in arr:
            result = self.db.query(param.product, param.rom_version, param.scene, param.process)
            print('result = ' + str(result))

            if result and result[0] != -1:
                result = (param.type, ) + result
                c_list.append(result)
            else:
                print('query data occur error!')

        if type == 'bar':
            self.drawBar(c_list, title, subtext, fileName)
        elif type == 'table':
            c_list = [('Scene', 'Min', 'Average', 'Max')] + c_list

            self.drawTable(c_list, title, fileName)

    # c_list 需要绘制的数据  第一行是列名非数据，数据的第一字段是行名
    def drawTable(self, c_list, title = '', fileName = ''):
        table = Table()

        headers = c_list[0]

        table.add(headers, c_list[1:])
        table.set_global_opts(
            title_opts=ComponentTitleOpts(title = title)
        )
        table.render(fileName)

    def drawBar(self, c_list, title = '',subtext = '',  fileName = '', x_xaxis = ['Min', 'Average', 'Max']):

        c = Bar({"theme": ThemeType.MACARONS})\
            .set_global_opts(
                title_opts={"text": title, "subtext": subtext},
                legend_opts=opts.LegendOpts(pos_bottom='bottom')
            )

        c.add_xaxis(x_xaxis)

        for item in c_list:
            if len(c_list) != 0:
                c.add_yaxis(item[0], item[1:])
            else:
                c.add_yaxis([])

        if not fileName.endswith('.html'):
            fileName += '.html'

        # 去除数据标签，某些场景下数据标签过多
        c.set_series_opts(label_opts=opts.LabelOpts(is_show=False))

        c.render(fileName)

    def drawingWithLine(self, srcFileName, title, htmlFileName = 'test_line.html', scene = []):
        if not os.path.exists(srcFileName):
            print("File not exist!")
            return

        data_list = np.loadtxt(srcFileName, skiprows=1, unpack=True)

        c = Line()\
            .set_global_opts(
                title_opts={"text": title, "type": "value"}
        )

        line_arr = [i for i in range(len(data_list[0]))]

        c.add_xaxis(line_arr)

        i = 0
        for col in data_list:
            c.add_yaxis(scene[i], col)

            i += 1

        if not htmlFileName.endswith('.html'):
            htmlFileName += '.html'

        # 去除数据标签，某些场景下数据标签过多
        c.set_series_opts(label_opts=opts.LabelOpts(is_show=False))

        c.render(htmlFileName)

    # todo 英文标题转中文
    def __title_En2Cn(self):
        en_cn = {
            'mem': 'PSS占用',
            'cpu': 'CPU占用',
            'voice_trans': '按键翻译',
        }

class BaseParams(object):

    def __init__(self, product, rom_version, scene, process, type = ''):
        self.product = product
        self.rom_version = rom_version
        self.scene = scene
        self.process = process
        self.type = type

class PropertyData(object):

    def __init__(self, c_title, c_min, c_mid, c_max):
        self.c_title = c_title
        self.c_min = c_min
        self.c_mid = c_mid
        self.c_max = c_max

if __name__ == '__main__':
    dbh = DbHelper()

    c_list = [
        ['LB-OTA1', '7430', '4098.69', '2395.45', '3181.81', '3957.65', '3832.81', '3803.85', '3723.62',
         '3769.88', '3689.23', '3467.08', '3357.25', '3550.25', '3241.5', '3234.17'],
        ['LB-2600', '7258.94', '3166.06', '2294.31', '3614.46', '3893.49', '3783.03', '3846.66', '3807.94', '3699.31',
         '3499.21', '0', '0', '0', '0', '0'],
        ['研究院', '4286', '4286', '0', '1880', '1890', '1880', '1902', '4088', '4096', '3803',
         '2845', '2846', '3545', '2900', '2912']
    ]

    dbh.drawBar(c_list, title='LB-OTA1对比2600资源加载耗时', subtext='子标题：分别按最小值、均值、最大值对比', fileName='compare_prepareRes.html',
                x_xaxis=['en', 'ja', 'ko', 'ru', 'fr', 'es', 'ar', 'de', 'vi', 'th', 'pt', 'it', 'hi', 'ug', 'za'])