#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import re
import time
import urlparse
import requests
import urlpollution
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
hash_regex = re.compile(r'(\w){32}')

def is_static_file(p):
    extenstion = os.path.splitext(p.path)[1]
    return extenstion in static_ext

def in_pool(item):
    return item in pool


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
            # query = int_regex.sub('<int>', query)

            # verify static resource
            if scheme == 'http' and query and not is_static_file(o):
                # 匹配path中的整型
                print '[test]', path,
                path = hash_regex.sub('<hash>', path)
                path = int_regex.sub('<int>', path)

                qs = dict(urlparse.parse_qsl(query, keep_blank_values=True))

                # 匹配querystring中的整型
                for k, v in qs.iteritems():
                    # 如果值为空 补充为<int>
                    if v == '':
                        v = '1'
                    _k = hash_regex.sub('<hash>', v)
                    qs[k] = int_regex.sub('<int>', _k)
                    
                item = {
                    'host': host, 'path': path[1:].split('/'), 'query': qs}

                if in_pool(item):
                    continue

                # add url pool
                pool.append(item)
                buf.append(line)

                # print item
                # print url, item

        print '-' * 50
        for i in buf:
            print i.strip()
        fo.writelines(buf)

url_filter()
