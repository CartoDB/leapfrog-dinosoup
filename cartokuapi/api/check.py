#!/usr/bin/env python3

import sys
import os.path
import json


def has_src(path):
    return os.path.exists(os.path.join(path, 'main')) or os.path.exists(os.path.join(path, 'main.py'))


def has_queue(path):
    return os.path.exists(os.path.join(path, 'run_queue.py'))


def has_backend(path):
    req = os.path.exists(os.path.join(path, 'requirements.txt'))
    src = has_src(path)
    queue = has_queue(path)
    return req and (src or queue)


def has_frontend(path):
    return os.path.exists(os.path.join(path, 'package.json'))


def check(path):
    back = has_backend(path)
    front = has_frontend(path)

    if not back and not front:
        raise RuntimeError('Pre-check failed')

    return (back, front)


if __name__ == '__main__':
    print(json.dumps(check(sys.argv[1])))
