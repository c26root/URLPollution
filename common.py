#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import re
import requests
from config import COMMAND_INJECT_LOG


def load_log():
    with open(command_inject_log) as f:
        return [i.strip() for i in f]



