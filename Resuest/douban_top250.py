import requests
import re
import csv
domain = "https://movie.douban.com/top250"

for i in range(0,11):
    j = i*25
    # print(j)
    url = domain+'?'+'start={}'.format(j)
    # url="https://movie.douban.com/top250?start=50"
    # print(url)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0"}
    resp = requests.get(url, headers=headers)
    resp.encoding ='utf-8'
    page_context = resp.text

# print(page_context)

# 对获取的数据进行解析
    obj1 = re.compile(r'<li>.*? <div class="item">.*?<span class="title">(?P<name>.*?)</span>.*?'
                  r'<p class="">.*?<br>(?P<year>.*?)&nbsp.*?'
                  r'<span>(?P<num>.*?)人评价</span>', re.S) # 对电影的名称进行解析

# 开始进行匹配
    result1= obj1.finditer(page_context)
    f = open("data.csv",mode="a+",newline='',encoding='utf-8') #打开data.csv
    csvwrite = csv.writer(f)
    for it in result1:
        # print(it.group("name"))
        # print(it.group("year").strip())  #strip()消除空格
        # print(it.group("num"))
        dic = it.groupdict()
        dic['year']=dic['year'].strip()
        print(dic.values())
        csvwrite.writerow(dic.values())
    f.close()







