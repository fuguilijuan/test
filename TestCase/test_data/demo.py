import requests
import urllib.request
url = "http://192.168.6.201:8081"

try:
    r = urllib.request.urlopen(url,timeout=3).read()
    print(r)
except Exception as e:
    print('False:'+str(e))