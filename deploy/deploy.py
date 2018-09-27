#!/usr/bin/env python3

import sys
import subprocess

from os import path


# Supported node stuff
NODE_VERSIONS = ['10', '8', '6']
NODE_MANAGERS = ['npm', 'yarn']


# Supported app types and its listening port inside Docker
APP_TYPES = {
    'wsgi-python': 8080,
    'static': 80
}


# Path stuff
BASE_PATH = f"{path.abspath(path.dirname(__file__))}"
DOCKERFILE = f"{path.join(path.join(BASE_PATH, 'dockerfiles'), 'Dockerfile')}"


def clean_sting(string):
    """
    Clean an string by removing all non-ascii characters and all
    the spaces.

    :param string: string to clean
    :type string: str
    :rtype: str
    """

    return ''.join([c for c in string if ord(c) < 128]).replace(' ', '')


def run_command(command, cwd=None):
    """
    Runs a command and returns its return code.

    :param command: command to run
    :type command: str
    :param cwd: working directory
    :type cwd: str
    :rtype: int
    """

    p = subprocess.run(command, shell=True, capture_output=True, cwd=cwd)

    return (p.returncode, p.stdout.decode('utf-8'), p.stderr.decode('utf-8'))


def build_node_app(path, version, manager):
    """
    Builds a node frontend app using the specified node version and
    node manager.

    :param path: path to the app source code
    :type path: str
    :param version: node version (6, 8, 10, ...)
    :type version: str
    :param manager: node manager (npm, yarn, ...)
    :type manager: str
    :rtype: None
    """

    # Value checks
    if version not in NODE_VERSIONS:
        raise ValueError((f"Node version `{version}` not supported. "
                          f"Versions: {', '.join(NODE_VERSIONS)}"))

    if manager not in NODE_MANAGERS:
        raise ValueError((f"Node manager `{manager}` not supported. "
                          f"Managers: {', '.join(NODE_MANAGERS)}"))

    # Base node command
    node_cmd = f"docker run -it --rm -v {path}:/tmp/app -w /tmp/app node:{version}"

    # Run install
    rc, stdout, stderr = run_command(f"{node_cmd} {manager} install")

    print(f"{stdout}")

    if rc != 0:
        print(f"{stderr}", file=sys.stderr)
        raise RuntimeError(f"Error running `{manager} install`")

    # Run build
    rc, stdout, stderr = run_command(f"{node_cmd} {manager} run build")

    print(f"{stdout}")

    if rc != 0:
        print(f"{stderr}", file=sys.stderr)
        raise RuntimeError(f"Error running `{manager} run build`")


def build_docker_image(path, app_type, app_name, version=None):
    """
    Builds a docker image using different Dockerfile based on the app type.
    If a previous version of the image exist it will be owerwritten if version
    is None.

    Returns the image name.

    :param path: path to the source code
    :type manager: str
    :param app_type: type of the app (static, wsgi-python, ...)
    :type app_type: str
    :param app_name: name of the app
    :type app_name: str
    :param version: version of the app (arbitrary string)
    :type version: str
    :rtype: str
    """

    # Value checks
    if app_type not in APP_TYPES:
        raise ValueError((f"App type `{app_type}` not supported. "
                          f"Types: {', '.join(APP_TYPES)}"))

    # Build the image name
    image_name = f"cartoku-{app_name}"

    if version:
        image_name += f"-{version}"

    # Build the image
    rc, stdout, stderr = run_command(f"docker build -f {DOCKERFILE}.{app_type} -t {image_name} {path}")

    print(f"{stdout}")

    if rc != 0:
        print(f"{stderr}", file=sys.stderr)
        raise RuntimeError(f"Error building docker image")

    # Return the image name
    return image_name


def run_app(image, app_type, port, env_vars={}):
    """
    Runs an an app using the docker image.

    :param image: image to run
    :type image: str
    :param app_type: type of the app (static, wsgi-python, ...)
    :type app_type: str
    :param port: port where the app should listen
    :type port: str
    :param env_vars: envars to pass to the container
    :type env_vars: dict
    :rtype: str
    """

    # Value checks
    if app_type not in APP_TYPES:
        raise ValueError((f"App type `{app_type}` not supported. "
                          f"Types: {', '.join(APP_TYPES)}"))

    # Run the image
    env_params = ''
    for var, value in env_vars.keys():
        env_vars += f" -e {var}='{value}'"

    rc, stdout, stderr = run_command(f"docker run --rm -d -p {port}:{APP_TYPES[app_type]}{env_params} {image}")

    print(f"{stdout}")

    if rc != 0:
        print(f"{stderr}", file=sys.stderr)
        raise RuntimeError("Error running app")


if __name__ == "__main__":
    build_node_app(f"{path.abspath(path.dirname(__file__))}/dummy-app",
                   "10", "yarn")

    i = build_docker_image(f"{path.abspath(path.dirname(__file__))}/dummy-app",
                           "wsgi-python", "dummy", "1.0.0")

    run_app(i, "wsgi-python", 8080)
