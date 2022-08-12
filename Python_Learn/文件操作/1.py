# 创建文件data.txt,文件共100000行，每行存放一个1～100之间的整数
import random

filename = "F:\AR_Glass_TestToolkit\data.txt" #目录下创建一个data.txt文件
with open(filename, 'w') as file:
    for i in range(10000):
        file.write(str(random.randint(1, 100)) + '\n')
