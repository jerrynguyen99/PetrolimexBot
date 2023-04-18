from unittest import result
import requests
import re

x = requests.get('https://webtygia.com/api/xang-dau')
data = re.findall('<td class="text-right">(.*?)</td>', str(x.content))
result = list(map(lambda x: x.replace('\\n',''),data))[:-1]
print(result[::2])
print(result[1::2])

