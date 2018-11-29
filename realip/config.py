#!/usr/bin/env python
# -*- coding:utf8 -*-

import os

## define app workplace
APPDIR = os.path.abspath(os.path.join(__file__, '../..'))
TMP_DIR = os.path.join(APPDIR, 'temp')

FLASK_HOST = "0.0.0.0"
FLASK_PORT = 8080

URI_REALIP = "/getip"

URL_OUI = 'http://standards-oui.ieee.org/oui/oui.txt'
