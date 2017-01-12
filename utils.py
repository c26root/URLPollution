#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import sys
import uuid
import string
import random
import urllib
import hashlib
import urlparse


class Hash:

    @staticmethod
    # MD5
    def md5(str):
        return hashlib.md5(str).hexdigest()

    # SHA1
    @staticmethod
    def sha1(str):
        return hashlib.sha1(str).hexdigest()

    # SHA224
    @staticmethod
    def sha224(str):
        return hashlib.sha224(str).hexdigest()

    # SHA256
    @staticmethod
    def sha256(str):
        return hashlib.sha256(str).hexdigest()

    # SHA384
    @staticmethod
    def sha384(str):
        return hashlib.sha384(str).hexdigest()

    # SHA512
    @staticmethod
    def sha512(str):
        return hashlib.sha512(str).hexdigest()


class Random:

    @staticmethod
    def id_generator(size=8, chars=string.ascii_letters + string.digits):
        return ''.join(random.choice(chars) for _ in xrange(size)).lower()

    @staticmethod
    def uuid_generator():
        return uuid.uuid1()


class Url:

    @staticmethod
    def url_parse(url):
        return urlparse.urlparse(url)

    @staticmethod
    def url_unparse(data):
        scheme, netloc, url, params, query, fragment = data
        if params:
            url = "%s;%s" % (url, params)
        return urlparse.urlunsplit((scheme, netloc, url, query, fragment))

    @staticmethod
    def qs_parse(qs):
        return dict(urlparse.parse_qsl(qs, keep_blank_values=True))

    @staticmethod
    def build_qs(qs):
        return urllib.urlencode(qs)

    @staticmethod
    def urldecode(qs):
        return urllib.unquote(qs)

    @staticmethod
    def urlencode(qs):
        return urllib.quote(qs)


class File:

    @staticmethod
    def load_file(filename):
        with open(filename) as f:
            return [i.strip() for i in f]

    @staticmethod
    def file2hex(fn):
        import binascii
        with open(fn) as f:
            print binascii.hexlify(f.read()).upper()

    @staticmethod
    def file_md5(fn):
        with open(fn, 'rb') as f:
            return md5(f.read())
