import requests

url = "http://127.0.0.1/luisico/apps/myapp/deploy"

deploy_status = 'pushed'
deploy_status = 'failed_validation'

post_data = {'status': deploy_status}

r = requests.post(url, data = post_data)
