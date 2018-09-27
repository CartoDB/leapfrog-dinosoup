#!/usr/bin/env python3

import sys
import os.path
import json


def has_src(path):
    return os.path.exists(os.path.join(path, 'src')) or os.path.exists(os.path.join(path, 'src.py'))


def has_queue(path):
    return os.path.exists(os.path.join(path, 'run_queue.py'))


def has_backend(path):
    req = os.path.exists(os.path.join(path, 'requirements.txt'))
    src = has_src(path)
    queue = has_queue(path)
    return req and (src or queue)


def has_frontend(path):
    return os.path.exists(os.path.join(path, 'www'))


path = sys.argv[1]
back = has_backend(path)
front = has_frontend(path)

if not back and not front:
    print('[ERR] Could not find backend nor frontend')
    sys.exit(1)

print(json.dumps({
    'backend': {
        'web': has_src(path),
        'queue': has_queue(path)
    },
    'frontend': front
}))
