# web爬虫学习 -- 分析
# 获取页面信息
# 输入：url
# 处理：request库获取页面信息，并从爬取到的内容中提取关键信息
# 输出：打印输出提取到的关键信息


import requests

from bs4 import BeautifulSoup
import time
import re


def getHTMLText(url):
    try:

        r = requests.get(url, timeout=30)

        r.raise_for_status()  # 如果状态码不是200，产生异常

        r.encoding = 'utf-8'  # 字符编码格式改成 utf-8

        return r.text

    except:

        # 异常处理

        return " error "


def findHTMLText(text):
    soup = BeautifulSoup(text, "html.parser")  # 返回BeautifulSoup对象

    return soup.find_all(string=re.compile('语音'))  # 结合正则表达式，实现字符串片段匹配


url = "https://tousu.sina.com.cn"

text = getHTMLText(url)  # 获取html文本内容

res = findHTMLText(text)  # 匹配结果

print(res)  # 打印输出