from django.shortcuts import render

def push_deploy(username, app_name):
    status = request.form['status']
    deploy = Deploy(app_name, status)
    import pdb; pdb.set_trace()
    return jsonify(
                {'status': 'ok'}
            )

def list_deploys(username):
    pass
