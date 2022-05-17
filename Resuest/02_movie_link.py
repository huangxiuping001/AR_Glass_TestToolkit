#1 获取电影的全部信息
#2.获取2022必看电影
#3. 定位到2022必看电影中子页面的连接地址
#4. 请求子页面的地址，拿到我们需要下载的地址

import requests
import re
import csv


doamin = "https://dytt89.com/"
headers={
"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
}
resp = requests.get(doamin,headers=headers,verify=False) # verify=False 是去掉安全验证
# print(resp)
resp.encoding = 'gbk'  # 当前网站的编码是gbk
# print(resp.text)

#对获取的数据进行解析,拿到URL中的<li>xxxxx需要的内容</li>
obj1=re.compile(r"2022必看热片.*?<ul>(?P<URL>.*?) </ul>",re.S)
obj2=re.compile(r"<a href='(?P<html_url>.*?)'",re.S)
obj3=re.compile(r'◎译　　名(?P<movie_name>.*?)<br />.*?<td style="WORD-WRAP: break-word" bgcolor="#fdfddf"><a href="(?P<download_url>.*?)">',re.S)
#对解析的出来的数据进行匹配
result1 = obj1.finditer(resp.text)
child_herf_list = []  # 建立一个空的list

# print(result1)
for it1 in result1:

    URL=it1.group("URL") #这里一定要注意，有坑，获取到主页面的URL
    # print(URL)

    #提取子页面连接
    result2=obj2.finditer(URL) # 根据主页面获取的内容提取子页面的内容

    for it2 in result2:
        # print(it2.group("html_url"))
        child_herf = doamin+it2.group("html_url").strip("/") #strip("/") 是将拼接多余的/去掉
        child_herf_list.append(child_herf) #将子页面的link保存起来
        # print(child_herf_list)
    #提取子页面的内容
f = open(r"F:\AR_Glass_TestToolkit\Resuest\moivedata.csv", mode="a+", newline='', encoding='gbk')  # 打开data.csv
csvwrite = csv.writer(f)
for herf in child_herf_list:
    child_resp = requests.get(herf,verify=False)
    child_resp.encoding="gbk"
    # print(child_resp.text)
    result3 = obj3.search(child_resp.text) #这里如果有finiter又要用循环
    # print(result3.group("movie_name"))
    # print(result3.group("download_url"))

    dic = result3.groupdict() #将result3的内容放入字典中
    csvwrite.writerow(dic.values())







