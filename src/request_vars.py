#!/usr/bin/env python
# -*- coding: utf-8 -*-


import threading

global_vars = threading.local()


def get_global_variable(key, default=None):
    try:
        return global_vars.__getattribute__(key)
    except AttributeError:
        return default


def set_global_variable(key, value):
    global_vars.__setattr__(key, value)


def clear_global_variables():
    global_vars.__dict__.clear()
