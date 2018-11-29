#!/usr/bin/env python
# -*- coding:utf8 -*-

import requests
from flask import Flask
from flask import request, Response, abort, jsonify
import config
from realip.utils.logger import logger
from realip.utils.macquery import MacQuery

## init logger https://github.com/senko/python-logger/blob/master/logger.py
logger.basicConfig()

app = Flask(__name__)

@app.route(config.URI_REALIP, methods=['GET'])
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

@app.route('/mac/<macaddr>', methods=['GET'])
def mac_query(macaddr):
    if not request.method == 'GET':
        abort(400)
        return
    ## get params
    logger.debug("user input request.args %r" % (request.args))
    ## get headers dict
    real_ip = request.headers.get('X-Real-IP')
    logger.info("GET header X-Real-IP %r" % (real_ip))
    if not macaddr:
        abort(400)
        return
    macquery = MacQuery()
    results = {}
    query_result = macquery.query(macaddr)
    if query_result:
        results["Organization"] = query_result
        results["MAC_Address"] = macaddr.replace(":", "").replace("-", "").upper()[0:6]
        return (jsonify(results), 200)
    else:
        abort(404)
