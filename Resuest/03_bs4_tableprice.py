import csv
import html.parser

import requests
from bs4 import BeautifulSoup

url = 'https://wap.21food.cn/price/market/828.html'
header = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"
}

resp = requests.get(url,header=header)

f=open("caijia.csv",mode="w",newline='',encoding="gbk")
csvwrite=csv.writer(f)
# print(resp)

#解析数据
#1. 将源代码交给BeautifulSoup进行处理，生成bs的对象
page = BeautifulSoup(resp.text,"html.parser")
#2. 从bs4的对象中查找数据
#find() 找到一个就停止 和 find_all() 全部找出

table=page.find("div",class_="p_to_list_m") #因为class是关键字，所以使用class_
# print(table)
trs = table.find_all("tr")[1:] #tr是表格的行，td是表格的列,[1:]从第二个tr开始找
for tr in trs:
    tds = tr.find_all("td")
    name=tds[1].text
    guige=tds[2].text
    price = tds[3].text
    time = tds[4].text
    qushi = tds[5].text
    print(name,guige,price,time,qushi)
    csvwrite.writerow([name,guige,price,time,qushi])
print("已完成")



