#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import json
import logging
import requests
import grequests
from urlpollution import Pollution
from utils import File, Hash, Url
from config import request_timeout, headers, command_execute_log
from command_execution_payloads import payloads


class CommandExecution:

    def __init__(self, filename):
        self.filename = filename
        # 加载url列表
        self.target_urls = self._load_file(self.filename)
        # 初始化日志
        self._loggingConfig()

    # 加载文件
    def _load_file(self, filename):
        with open(filename) as f:
            return [i.strip() for i in f]

    # 日志记录配置
    def _loggingConfig(self):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                            datefmt='%m-%d %H:%M',
                            filename=command_execute_log)

        logging.getLogger("requests").setLevel(logging.WARNING)

    # 通过标记查找对应Payload
    def _get_name_by_sign(self, sign):
        for i in payloads:
            if i.get('sign') == sign:
                return i
        return ''

    def run(self):
        for url in self.target_urls:

            signs = [i.get('sign') for i in payloads]

            p = Pollution([payload.get('payload') for payload in payloads])

            # 分解url
            parse = Url.url_parse(url)
            query = parse.query

            urls = []
            for i in p.payload_generator(url, append=False):
                urls.append(i)
                print Url.urldecode(i)

            # Start
            print 'Payload Number:', len(urls)
            rs = (grequests.get(u, headers=headers, allow_redirects=False)
                  for u in urls)
            response = grequests.map(rs, gtimeout=request_timeout)
            for i in response:
                if i is not None:
                    for payload in payloads:
                        sign = payload.get('sign')
                        name = payload.get('name')
                        if sign in i.content:
                            print Url.urldecode(i.url), sign, name
                            logging.info(
                                '{0} => {1}'.format(Url.urldecode(i.url), name))


if __name__ == '__main__':
    filename = 'output.txt'
    cmd = CommandExecution(filename)
    cmd.run()
