#!/usr/bin/env python3

import logging
import subprocess

from os import path
from logging import StreamHandler

# Supported node stuff
NODE_VERSIONS = ['10', '8', '6']
NODE_MANAGERS = ['npm', 'yarn']


# Supported app types and its listening port inside Docker
APP_TYPES = {
    'wsgi-python': 8080,
    'static': 80
}


# Path stuff
BASE_PATH = path.abspath(path.dirname(__file__))
DOCKERFILE = path.join(path.join(BASE_PATH, 'dockerfiles'), 'Dockerfile')


def clean_sting(string):
    """
    Clean an string by removing all non-ascii characters and all
    the spaces.

    :param string: string to clean
    :type string: str
    :rtype: str
    """

    return ''.join([c for c in string if ord(c) < 128]).replace(' ', '')


def run_command(command, logger, cwd=None):
    """
    Runs a command and returns its return code.

    :param command: command to run
    :type command: str
    :param cwd: working directory
    :type cwd: str
    :rtype: int
    """

    logger.info(command)

    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, cwd=cwd)

    while p.poll() is None:
        line = p.stdout.readline()
        logger.debug(line.decode('utf-8').strip())

    return p.returncode


class Deployer:
    def __init__(self, logger):
        self.logger = logger

    def build_node_app(self, path, version, manager):
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
            raise ValueError("Node version `{}` not supported. Versions: {}".format(version, ', '.join(NODE_VERSIONS)))

        if manager not in NODE_MANAGERS:
            raise ValueError("Node manager `{}` not supported. Managers: {}".format(manager, ', '.join(NODE_MANAGERS)))

        # Base node command
        node_cmd = "docker run -it --rm -v {}:/tmp/app -w /tmp/app node:{} {}".format(path, version, manager)

        # Run install
        self.logger.info("Installing node dependencies")
        rc = run_command("{} install".format(node_cmd), self.logger)

        if rc != 0:
            self.logger.error("Failed to install node dependencies")
            raise RuntimeError("Error running `{} install`".format(manager))

        # Run build
        self.logger.info("Compiling node application")
        rc = run_command("{} run build".format(node_cmd), self.logger)

        if rc != 0:
            self.logger.error("Failed to build node application")
            raise RuntimeError("Error running `{} run build`".format(manager))

    def build_docker_image(self, path, app_type, app_name, version=None):
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
            raise ValueError("App type `{}` not supported. Types: {}".format(app_type, ', '.join(APP_TYPES)))

        # Build the image name
        image_name = "cartoku-{}".format(app_name)

        if version:
            image_name += "-{}".format(version)

        # Build the image
        self.logger.info("Building docker image")
        rc = run_command("docker build -f {}.{} -t {} {}".format(DOCKERFILE, app_type, image_name, path), self.logger)

        if rc != 0:
            self.logger.error("Failed to build docker image")
            raise RuntimeError("Error building docker image")

        # Return the image name
        return image_name

    def run_app(self, image, app_type, port, env_vars={}):
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
            raise ValueError("App type `{}` not supported. Types: {}".format(app_type, ', '.join(APP_TYPES)))

        # Run the image
        env_params = ''
        for var, value in env_vars.keys():
            env_vars += " -e {}='{}'".format(var, value)

        self.logger.info("Running docker image")
        rc = run_command("docker run --rm -d -p {}:{}{} {}".format(port, APP_TYPES[app_type], env_params, image), self.logger)

        if rc != 0:
            self.logger.error("Failed to run docker image")
            raise RuntimeError("Error running app")
