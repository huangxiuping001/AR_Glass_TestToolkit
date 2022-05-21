import time

import requests
from bs4 import BeautifulSoup

url="https://umei.cc/bizhitupian/weimeibizhi/"

headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"}

# 拿到主页面的源代码，然后提取子页面的下载link
#2. 通过
resp = requests.get(url,headers=headers)
resp.encoding="utf-8"
# print(resp.text)

main_page = BeautifulSoup(resp.text,"html.parser")
alist=main_page.find("ul",class_="pic-list after").find_all('a')
# print(alist)
#循环取出a标签中的herf
for a in alist:
    # print(a.get("href")) #直接通过geit就可以拿到属性
    #拿到子页面的源代码，获取到子页面的link和子页面的源代码
    link="https://umei.cc"
    hrefs=link+a.get("href")  #将<a href=xxx.htm 和https://umei.cc 进行拼接，因为当前不是实际的link>
    # print(hrefs)
    child_page_resp=requests.get(hrefs)
    child_page_resp.encoding="utf-8"
    # print(child_page_resp.text)
    #再从子页面中拿到下载的link
    chlid_page=BeautifulSoup(child_page_resp.text,"html.parser")
    S=chlid_page.find("section",class_="img-content")
    # print(S)
    img=S.find("img")
    # print(img)
    src=img.get("src") #拿到img标签，需要拿到img标签下的属性src
    # print(src)

    #下载图片
    img_resp=requests.get(src) #响应图片
    img_resp.content #这里拿到的字节
    image_name =src.split("/")[-1]
    with open("img/"+image_name,mode="wb")as f:
        f.write(img_resp.content)

        print("下载完成",image_name)
        time.sleep(1)








