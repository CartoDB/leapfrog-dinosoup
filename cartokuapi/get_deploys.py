import requests

port = 8000
url = "http://127.0.0.1:%d/luisico/apps/myapp/deploys" % port

r = requests.get(url)
print r.status_code
print r.text
