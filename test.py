# -*- coding: UTF-8 -*-

from requests_noblock import requests_noblock

_url = "https://www.baidu.com"    
                
obj = requests_noblock()
response = obj.get(url = _url)

print(response)
print(response["data"].text)
print("*"*100)











