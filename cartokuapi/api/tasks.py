import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cartokuapi.settings')

from celery import Celery

app = Celery('tasks', broker='redis://localhost/10')


@app.task
def deploy(deploy_id):
    # God just killed a kitten
    import tempfile
    import subprocess
    from api.models import Deploy
    from api.deploy import Deployer
    from api.check import check

    d = Deploy.objects.get(pk=deploy_id)
    d.status = "checking"
    d.logger().info("Checking application")

    try:
        with tempfile.TemporaryDirectory() as tmp:
            print(tmp)
            subprocess.run(["git", "clone", d.app.repo_path, tmp])
            back, front = check(tmp)

            app_type = "wsgi-python" if back else "static"
            d.logger().info("Check suceeded. Application is {}".format(app_type))

            magic = Deployer(d.logger())
            if front:
                d.status = "compiling"
                d.save()
                magic.build_node_app(tmp, '10', 'yarn')

            d.status = "building_image"
            d.save()
            img = magic.build_docker_image(tmp, app_type, d.app.name, version=d.pk)

            d.status = "executing"
            d.save()
            magic.run_app(img, app_type, 8000 + d.pk)

            d.status = "success"
            d.logger().info("Deploy succeeded")

    except Exception as e:
        d.status = "failed"
        print(e)
        d.logger().error(str(e))
