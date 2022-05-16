import requests
import re


url="https://tousu.sina.com.cn/index/search/?keywords=%E8%AF%AD%E9%9F%B3%E5%8A%A9%E6%89%8B&t=0"
header={"User-Agent": 'https://tousu.sina.com.cn/index/search/?keywords=%E8%AF%AD%E9%9F%B3%E5%8A%A9%E6%89%8B&t=0'} #这里需要你自己填header
r=requests.get(url,headers=header)
r.encoding='utf-8'
# r.status_code
# print(r.text) #返回对应的html文本
#
from bs4 import BeautifulSoup

soup = BeautifulSoup(r.text,"html.parser")
# print(soup)
# soup.find_all(re.compile('p'))
soup.find_all(text=re.compile('语音'))

