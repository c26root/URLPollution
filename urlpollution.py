#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import random
from utils import Url


class Pollution:

    def __init__(self, payloads):
        self.payloads = payloads

    def payload_generator(self, query, all_qs=False, append=True):

        ret = list()

        # 如果是url 进行分解
        if self._is_url(query):

            url = query
            self.parse = Url.url_parse(url)
            query = self.parse.query

            # 一次污染所有qs
            if all_qs:
                for payload in self.payloads:
                    qs = self._pollution_all(query, payload, append=append)
                    url = self._url_unparse(qs)
                    ret.append(url)
            else:
                for payload in self.payloads:
                    for qs in self._pollution(query, payload, append=append):
                        url = self._url_unparse(qs)
                        ret.append(url)

        else:
            # 参数处理

            if all_qs:
                for payload in self.payloads:
                    ret.append(self._pollution_all(query, payload, append=append))
            else:
                for payload in self.payloads:
                    for qs in self._pollution(query, payload, append=append):
                        ret.append(qs)

        return ret

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
    payloads = ['phpinfo();', 'echo 1;']
    qs = 'http://baidu.com/?a=1&b=2'
    p = Pollution(payloads)
    print p.payload_generator(qs)

