#!/usr/bin/env python
# -*- coding:utf8 -*-

import os
import time
import requests
import shutil
import subprocess
from realip import config
from logger import logger

## init logger https://github.com/senko/python-logger/blob/master/logger.py
logger.basicConfig()


class MacQuery(object):
    """Using IEEE Data to Find OUI info
    http://standards-oui.ieee.org/oui/oui.txt
    """
    def __init__(self):
        ## define init data
        self.filepath_oui = os.path.join(getattr(config, "TMP_DIR"), "oui_formal.txt")
        self.filepath_oui_tmp = os.path.join(getattr(config, "TMP_DIR"), "oui_tmp.txt")
        ## get oui url
        self.url_oui = getattr(config, "URL_OUI")

    def info_grep(self):
        """info grep
        """
        cmd = "cat %s | grep 'base 16' > %s" %(self.filepath_oui_tmp, self.filepath_oui)
        return subprocess.call(cmd, shell=True)

    def downloader(self):
        """download and replace files
        """
        with requests.Session() as s:
            s.mount("http://", requests.adapters.HTTPAdapter(max_retries=5))
            s.mount("https://", requests.adapters.HTTPAdapter(max_retries=5))
            r = s.get(url = self.url_oui, stream = True)
            if r.status_code == 200:
                with open(self.filepath_oui_tmp, 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
                if self.info_grep() == 0:
                    return True
                else:
                    return False
            else:
                return False

    def update(self):
        """update oui file
        1. file not exist, update
        2. file exists but expired, update
        """
        if os.path.isfile(self.filepath_oui):
            logger.debug("oui file exist")
            ## check mtime
            if time.time() - os.path.getmtime(self.filepath_oui) > 86400.0:
                logger.debug("oui file expired")
                #TODO download and replace
                if self.downloader() == False:
                    logger.error("oui file update fail")
                    return False
                return True
            else:
                return False
        else:
            #TODO download
            if self.downloader() == False:
                logger.error("oui file update fail")
                return False
            return True

    def query(self, macaddr = None):
        """queryer
        """
        if macaddr == None:
            return None
        ## update file
        self.update()
        try:
            macaddr = macaddr.replace(":", "").replace("-", "").upper()[0:6]
            logger.debug("mac query is %s" %macaddr)
            with open(self.filepath_oui, 'r') as f:
                line = f.readline()
                while line:
                    line_list = line.split("(base 16)")
                    if line_list[0].strip() == macaddr:
                        logger.debug("hit record, line = %s" %line)
                        return line_list[1].strip()
                    line = f.readline()
                return None
        except:
            logger.error("oui file query fail")
            return None
