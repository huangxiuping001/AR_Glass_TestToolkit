import requests
import hashlib
r = requests.get('http://wthrcdn.etouch.cn/weather_mini')
print(r.text)

data ={}
data['city']='北京'
r = requests.get('http://wthrcdn.etouch.cn/weather_mini',params=data)
print(r.text)

data ={}
data['city']='合肥'
auth=hashlib.md5(data['city'].encode(encoding='utf-8')).hexdigest()
headers = {'Authorization': auth}
r = requests.get('http://wthrcdn.etouch.cn/weather_mini',params=data,headers=headers)
print(r.text)