# -*- coding: UTF-8 -*-
"""
Created on 2022年4月12日
@author: Monica
"""
import pymysql
from time import sleep

#数据库，创建连接
Connection = pymysql.connect(database='arglass', host='localhost', user='root', password='monica001.')

cursor = Connection.cursor()
#在数据库中建立image表格
sql_create_table= '''
CREATE TABLE images (
  id int (10), 
  data MediumBlob
) '''  # 字段有id和data两个字段
cursor.execute(sql_create_table)  #执行sql语句，创建pictures表

#读取图片
fp = open(r'D:\AR_Glass_TestToolkit\ai_text_pic\ArithmeticOCR2.jpg','rb')
img = fp.read() #读取图片
sleep(2)
fp.close() #关闭图片

sql = "INSERT INTO images VALUES  (%s,%s);"
args = ('1',img)
cursor.execute(sql,args) #执行插入图片的sql语句

Connection.commit()#提交
#断开链接

Connection.close()
print("表建立成功")
print("图片上传成功")






# try:
# 	fin = open("../ArithmeticOCR1.jpg")#用读文件模式打开图片
# 	#将文本读入img对象中
#
# 	img = fin.read()#关闭文件
# 	fin.close()
#
# 		except IOError, 	e:
#
# #如果出错，打印错误信息
#
# print ("Error %d: %s" % (e.args[0],e.args[1]))
#
# sys.exit(1)
#
# 	try: #链接mysql，获取对象
#
# 		conn = mdb.connect(host='localhost',user='root',passwd='monica001.', db='arglass')
#
# #获取执行cursor
#
# 		cursor = conn.cursor()
#
# #直接将数据作为字符串，插入数据库
#
# 		cursor.execute("INSERT INTO Images SET Data='%s'" % mdb.escape_string(img))
#
# #提交数据
#
# 		conn.commit()
#
# #提交之后，再关闭cursor和链接
#
# 		cursor.close()
#
# 		conn.close()
#
# 		#若出现异常，打印信息
#
# 		print ("Error %d: %s" % (e.args[0],e.args[1]))