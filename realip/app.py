#!/usr/bin/env python
# -*- coding:utf8 -*-

import requests
from flask import Flask
from flask import request, Response, abort, jsonify
import config
from realip.utils.logger import logger

## init logger https://github.com/senko/python-logger/blob/master/logger.py
logger.basicConfig()

app = Flask(__name__)

@app.route(config.FLASK_URI, methods=['GET'])
def realip_resolver():
    if not request.method == 'GET':
        abort(400)
        return
    ## get params
    logger.debug("user input request.args %r" % (request.args))
    ## get headers dict
    real_ip = request.headers.get('X-Real-IP')
    logger.info("GET header X-Real-IP %r" % (real_ip))
    if not real_ip:
        abort(400)
        return
    results = {"ip": real_ip}
    return (jsonify(results), 200)
