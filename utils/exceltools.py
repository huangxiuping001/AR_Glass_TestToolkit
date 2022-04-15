import os
import re

import xlsxwriter
import xlrd
from utils.filetools import fileUtils
import logging
import numpy as np

# 将 文本文档中的性能数据整理到excel表格中并生成折线图  但python 可以操作的excel版本有点老 生成的折线图不太好看
class excletools(object):

    def gacao_deal_data(self, xlsxFileName, sourceFileName):
        if not xlsxFileName.endswith(".xlsx"):
            xlsxFileName += ".xlsx"

        self.__del_file(xlsxFileName)
        self.xlsx_file = xlsxwriter.Workbook(xlsxFileName)

        datas = self.__gacao_get_data_from_file(sourceFileName)
        self._deal_single_file("CPU", "1", datas, True)
        self.xlsx_file.close()

    def __gacao_get_data_from_file(self, file_path):
            datasource = []

            file = open(file_path)

            for line in file:
                data = line.split("\n")
                real_data = data[0].split("--")
                int_line = []
                if len(real_data) == 3:
                    real_data_totalpss = real_data[2]
                print(real_data_totalpss)
                int_line.append(float(real_data_totalpss))
                datasource.append(int_line)
            return datasource

    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # 处理文件夹下的所有文件，生成一个excel中的多个sheet， 参数为生成的excel名称 和 文件夹路径 以及是否生成折线图
    def deal_data(self, filename='test', dir_path='E:\\python_home\\untitled\\data', has_chart=True):
        if not filename.endswith(".xlsx"):
            filename = filename + ".xlsx"

        # 先删除 xlsx 文件
        self.__del_file(filename)
        # 新建 xlsx 文件
        self.xlsx_file = xlsxwriter.Workbook(filename)

        for file in os.listdir(dir_path):

            print(file)

            try:
                title, database = self.__get_data_from_file(dir_path + "/" + file)

                print("title = " + str(title))
                print("database = " + str(database))

                self._deal_single_file(file.split(".")[0], title, database, has_chart)

            except Exception as e:
                logging.debug(e)
                print(e)

        self.xlsx_file.close()

    # 从txt文件中获取数据
    def __get_data_from_file(self, filename='', title=None):
        first_line = True

        database = []
        m_title = []

        file = open(filename)

        for line in file:

            if first_line:
                first_line = False

                if title is None:
                    m_title = line.split()
                    continue
                else:
                    m_title = title

            int_line = []

            # todo : 分割符，可以自定义
            data = line.split()

            try:
                # 转成浮点数，否则 str 无法绘图
                for i in range(len(data)):
                    int_line.append(float(data[i]))

            except Exception as e:
                logging.debug(e)
                continue

            database.append(int_line)

        file.close()

        return m_title, database

    # 处理单个文件
    def _deal_single_file(self, sheetname='sheet1', title=None, database=None, has_chart=True):

        if database is None:
            print("data is empty!")
            return

        # 新建一个 sheet
        sheet = self.xlsx_file.add_worksheet(name=sheetname)

        bold = self.xlsx_file.add_format({'bold': True})

        # 写入表头，加粗
        sheet.write_row('A1', title, bold)

        # 循环写文件
        for row in range(len(database)):
            sheet.write_row('A' + str(row + 2), database[row])

        if not has_chart:
            return

        temp = ['Min', 'Max', 'Average']

        sheet.write_row(self.__number2A_Z(len(title) + 4) + '1', temp, bold)

        sheet.write_column(self.__number2A_Z(len(title) + 3) + '2', title, bold)

        for i in range(len(title)):
            m_min = self.__calculateStr('MIN', self.__number2A_Z(i + 1), 2, len(database) + 1)
            m_average = self.__calculateStr('AVERAGE', self.__number2A_Z(i + 1), 2, len(database) + 1)
            m_max = self.__calculateStr('MAX', self.__number2A_Z(i + 1), 2, len(database) + 1)

            # 计算最小值
            sheet.write(self.__number2A_Z(len(title) + 4) + str(i + 2), m_min)

            # 计算最大值
            sheet.write(self.__number2A_Z(len(title) + 5) + str(i + 2), m_max)

            # 计算均值
            sheet.write(self.__number2A_Z(len(title) + 6) + str(i + 2), m_average)

            print('min = ' + str(m_min))

        # 插入折线图
        chart = self.xlsx_file.add_chart({'type': 'line'})

        for i in range(0, len(title)):
            chart.add_series({'values': '=%s!$%s$2:$%s$%s' % (
            sheetname.split(".")[0], self.__number2A_Z(i + 1), self.__number2A_Z(i + 1),
            str(len(database) + 1)),
                              'name': title[i]})

            print('=%s!$%s$2:$%s$%s' % (sheetname, self.__number2A_Z(i + 1), self.__number2A_Z(i + 1),
                                        str(len(database) + 1)))

        chart.set_title({'name': sheetname})

        # 折线图风格，不喜欢可以自己换其他值
        chart.set_style(21)

        sheet.insert_chart(self.__number2A_Z(len(title) + 4) + '6', chart)

    # 将数字转为大写字母
    def __number2A_Z(self, number=0):
        if number < 1 or number > 26:
            print("column is over high")
            return None

        return str(chr(64 + number))

    def __calculateStr(self, type='MIN', row='A', start_postion=2, end_position=1000):
        print('=%s(%s%s:%s%s)' % (type, row, str(start_postion), row, str(end_position)))
        return '=%s(%s%s:%s%s)' % (type, row, str(start_postion), row, str(end_position))

    def __del_file(self, filename):
        path = os.getcwd() + "\\" + filename

        if os.path.exists(path):
            os.remove(path)

    # 从excel中读取指定 target_head 前缀的数据  并写到 txt 文本中去，可以在不同列上 每一行只读取第一个
    def read_text(self, path = '', target_head = ''):
        excel_file = xlrd.open_workbook(path)
        sheet = excel_file.sheet_by_index(0)

        max_row_num = sheet.nrows
        max_col_num = sheet.ncols

        for i in range(0, max_row_num):
            sn = ''
            for j in range(0, max_col_num):
                cell = str(sheet.row(i)[j].value)
                if cell.startswith("sn~"):
                    sn = cell
                    continue

                if cell.startswith(target_head):
                    fileUtils.write_file("E:\\python_home\\translator__android__test_toolkit\data\\text.txt",
                                         sn + "\t" + cell)
                    break

    # 读取单个文件里的数据 计算每一列的最小值、均值、最大值并写到文件中
    def readFileAndCache(self, fileName, path):
        if not os.path.exists(path):
            print("File not exist!")
            return

        data_list = np.loadtxt(path, skiprows=1, unpack=True)

        print('dl_type = ' + str(type(data_list[0])))

        if type(data_list[0]) is not np.ndarray:
            data_list = [data_list]

        i = 0
        for col_item in data_list:
            c_min = min(col_item)
            c_max = max(col_item)
            c_mid = np.mean(col_item)

            c_mid = np.around(c_mid, 2)

            i += 1

            content = os.path.basename(path).split('.')[0] + str(i)
            content += '\t' + str(c_min)
            content += '\t' + str(c_mid)
            content += '\t' + str(c_max) + '\n'

            print('line = ' + content)
            content = content.expandtabs(8)

            fileUtils.write_file(fileName, content)

    # 读取文件夹下的每个文件里的数据 计算每一列的最小值、均值、最大值并写到文件中
    def readFilesAndCache(self, filename, dir, ifCover = True):
        if not os.path.isdir(dir):
            print("Path not a folder!")
            return

        filename = filename.split('.')[0] + '.txt'

        if ifCover:
            if os.path.exists(filename):
                fileUtils.clean_file(filename)

        for file in os.listdir(dir):

            self.readFileAndCache(filename, dir + file)

if __name__ == '__main__':
    # exe = excletools()

    # exe.readFilesAndCache(filename='test2',
    #                       dir='E:\python_home\\translator__android__test_toolkit\data\\')

    # exe.read_text("E:\\python_home\\translator__android__test_toolkit\\data\\textexcel.xls", "p_keydown~")

    print(re.findall(r'\d+', "12 34 56\n78\n90"))

