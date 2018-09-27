import requests

port = 8000
url = "http://127.0.0.1:%d/luisico/apps/myapp/deploy" % port

deploy_status = 'pushed'
deploy_status = 'failed_validation'

post_data = {'status': deploy_status}

r = requests.post(url, data = post_data)
print r.status_code
print r.text
