#!/usr/bin/env python
# -*- coding: utf-8 -*-

from operator import itemgetter


def uniquify(seq, idfun=None):
    # order preserving
    if idfun is None:
        def idfun(x): return x
    seen = {}
    result = []
    for item in seq:
        marker = idfun(item)
        # in old Python versions:
        # if seen.has_key(marker)
        # but in new ones:
        if marker in seen: continue
        seen[marker] = 1
        result.append(item)
    return result


def string_to_list(raw_string, separator=',', lower=False):
    raw_string = raw_string.strip()
    raw_list = raw_string.split(separator)
    final_list = []
    for raw_list_item in raw_list:
        final_item = raw_list_item.strip()
        if final_item != '':
            if lower:
                final_item = final_item.lower()
            final_list.append(final_item)
    return final_list


def chunks(l, n):
    n = max(1, n)
    return (l[i:i+n] for i in xrange(0, len(l), n))


def sort_list_of_dicts(list_of_dicts, key_to_sort, reverse=False):
    return sorted(list_of_dicts, key=itemgetter(key_to_sort), reverse=reverse)
