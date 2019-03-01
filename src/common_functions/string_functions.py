#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import string
import re
from collections import defaultdict


def check_if_string_only_contains_allowed(mystring, allowed):
    return all(c in allowed for c in mystring)


def generate_random_string(length=12):
    return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(length))


def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""


def find_between_r( s, first, last ):
    try:
        start = s.rindex( first ) + len( first )
        end = s.rindex( last, start )
        return s[start:end]
    except ValueError:
        return ""
        

def convert_to_string_properly(raw):
    try:
        return str(raw)
    except UnicodeEncodeError:
        return raw.encode('utf-8')


def slugify(s):
    """
    Simplifies ugly strings into something URL-friendly.
    >>> print slugify("[Some] _ Article's Title--")
    some-articles-title
    """

    # "[Some] _ Article's Title--"
    # "[some] _ article's title--"
    s = s.lower()

    # "[some] _ article's_title--"
    # "[some]___article's_title__"
    for c in [' ', '-', '.', '/']:
        s = s.replace(c, '_')

    # "[some]___article's_title__"
    # "some___articles_title__"
    s = re.sub('\W', '', s)

    # "some___articles_title__"
    # "some   articles title  "
    s = s.replace('_', ' ')

    # "some   articles title  "
    # "some articles title "
    s = re.sub('\s+', ' ', s)

    # "some articles title "
    # "some articles title"
    s = s.strip()

    # "some articles title"
    # "some-articles-title"
    s = s.replace(' ', '-')

    return s


def replace_parameters(s, parameters):
    return string.Formatter().vformat(s, (), defaultdict(unicode, **parameters))


def number_to_google_sheet_column_name(input_column_number):
    out_put_column_name = ""
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    temp_number = input_column_number
    while (temp_number > 0):
       position = temp_number % len(chars)
       out_put_column_name = ('Z' if position == 0 else chars[position - 1 if position > 0 else 0]) + out_put_column_name
       temp_number = (temp_number - 1) / len(chars)

    return out_put_column_name
