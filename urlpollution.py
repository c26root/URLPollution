#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import random
from utils import Url


class URLPollution:

    def __init__(self, payloads):
        self.payloads = payloads

    def payload_generator(self, query, all_qs=False, append=True):

        ret = list()
        ret2 = list()

        self.parse = Url.url_parse(query)
        self.query = self.parse.query

        # a=1&b=2
        if not self.parse.scheme or not self.parse.netloc:
            self.query = query

        if all_qs:
            for payload in self.payloads:
                ret.append(self._pollution_all(
                    self.query, payload, append=append))
        else:
            for payload in self.payloads:
                for qs in self._pollution(self.query, payload, append=append):
                    ret.append(qs)

        # 遍历组合url
        for i in ret:
            if self.parse.netloc:
                ret2.append(self._url_unparse(i))
            else:
                ret2.append(i)

        return ret2

    # 合并url
    def _url_unparse(self, qs):
        url = Url.url_unparse(
            (self.parse.scheme,
             self.parse.netloc,
             self.parse.path,
             self.parse.params,
             qs,
             self.parse.fragment)
        )
        return url

    # 检查是否url和 querystring
    def _is_url(self, url):
        return (url.startswith('http://') or url.startswith('https://')) and Url.url_parse(url).query

    # QueryString => Dict
    def _qs2dict(self, query):
        return Url.qs_parse(query)

    # 逐个参数污染
    def _pollution(self, query, payload, append=True):
        qs = self._qs2dict(query)
        if not isinstance(qs, dict):
            return False

        ret = list()
        for i in qs.keys():
            temp = qs.copy()
            if append:
                temp[i] += payload
            else:
                temp[i] = payload
            temp = Url.build_qs(temp)
            ret.append(temp)
        return ret

    # 一次污染全部参数
    def _pollution_all(self, query, payload, append=True):

        qs = self._qs2dict(query)
        if not isinstance(qs, dict):
            return False

        for i in qs:
            if append:
                qs[i] += payload
            else:
                qs[i] = payload
        qs = Url.build_qs(qs)
        return qs


if __name__ == '__main__':
    # Configuration Payload
    payloads = ['phpinfo();', 'echo 1;']

    # Configuration URL or QueryString
    url = 'a=1&b=2'

    p = URLPollution(payloads)
    print p.payload_generator(url, append=True)
    print p.payload_generator(url, append=False)

    url = 'http://baidu.com/?x=1&y=2'

    p = URLPollution(payloads)
    print p.payload_generator(url, append=True)
    print p.payload_generator(url, append=False)
