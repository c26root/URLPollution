#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import re
import time
import urlparse
import requests
import urlpollution
from config import command_inject_log
from utils import Url
from pymongo import MongoClient
import tldextract

# from pybloomfilter import BloomFilter

static_ext = ('css', 'js', 'ico', 'svg', 'font', 'swf')
img_ext = ('jpg', 'gif', 'bmp', 'png', 'jpeg')
media_ext = ('mp3', 'mp4')
static_ext = ['.' + i for i in static_ext + img_ext + media_ext]

buf = []
pool = []

int_regex = re.compile(r'(\d+)')
def is_static_file(p):
    if p and p.path:
        for i in static_ext:
            if p.path.endswith(i):
                return True

def in_pool(item):
    for i in pool:
        if i == item:
            return True

def url_filter():
    with open('urls.txt') as fi, open('output.txt', 'w') as fo:
        
        for line in fi:
            url = line.strip()

            # parse url
            o = urlparse.urlparse(url)
            scheme = o.scheme
            host = o.netloc
            path = o.path
            query = o.query

            # schema item
            item = {
                'host': host,
                'path': path,
                'query': query
            }
            # qs = dict(urlparse.parse_qsl(query, keep_blank_values=True)
            qs = dict(urlparse.parse_qsl(query))

            # verify static resource
            if scheme == 'http' and query and not query.endswith('=') and not is_static_file(o):
                path = int_regex.sub('<int>', path)
                item = {'host': host, 'path': path[1:].split('/')[:-1], 'query': [i for i in qs.keys()]}

                if in_pool(item):
                    continue

                # add url pool
                pool.append(item)
                buf.append(line)
                # print item
                print url, item
        fo.writelines(buf)

url_filter()        


