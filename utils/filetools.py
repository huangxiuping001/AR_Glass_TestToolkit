# coding:utf-8
import codecs
import os

class fileUtils:

    @staticmethod
    def write_file(path, value):
        if os.path.exists(path):
            f = codecs.open(path, 'a', 'utf8')  # a:追加  w:重写
        else:
            f = open(path, "w")

        if not value.endswith('\n'):
            value = value + '\n'
        f.writelines(value)

        f.close()

    @staticmethod
    def clean_file(path):
        if os.path.exists(path):
            with open(path, "r+") as f:
                f.truncate()  # 清空文件
                f.close()

    @staticmethod
    def get_data_from_file(filepath=''):

        database = {}

        file = open(filepath)

        for line in file:

            # todo : 分割符，可以自定义
            data = line.split()

            print("line = " + line)

            if len(data) == 2:
                database[data[0]] = data[1]
            else:
                database[data[0]] = 'Null'

        file.close()

        return database

if __name__ == "__main__":

   pass
