# -*- coding: utf-8 -*-
import os

import numpy as np
from pyecharts import Line

class DataSchema():

    def __init__(self, chart_title):

        self.chart_title=chart_title
        self.chart_subtitle=u"统计如下"

    #根据传入的数组数量绘制折线图
    def line_chart(self,data_desc,*datalist):
        '''折线图1'''
        self.bar = Line(self.chart_title, self.chart_subtitle)  # 主副标题
        for data ,desc in zip(datalist,data_desc):
            if len(data)>0:
                t = np.linspace(1, len(data), len(data))
                self.bar.add(desc, t, data, mark_line=["average"], mark_point=["max"])
        self.bar.render(r"%s.html" % (self.chart_title))

    #计算最大值，平均数
    def average_max(self,datalist):
        '''数据计算'''
        average_value=np.mean(datalist)
        max_value=np.max(datalist)
        return average_value,max_value




