#!/usr/bin/env python
# -*- coding: utf-8 -*-


import datetime
from random import randrange


def datetime_to_timestamp(dt, epoch=datetime.datetime(1970,1,1)):
    td = dt - epoch
    return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 1e6


def get_random_date_from_1998_to_1950():
    d1 = datetime.datetime.strptime('1/1/1950', '%m/%d/%Y')
    d2 = datetime.datetime.strptime('1/1/1988', '%m/%d/%Y')
    return random_date(d1, d2)


def random_date(start, end):
    """
    This function will return a random datetime between two datetime 
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + datetime.timedelta(seconds=random_second)


def date_format_day_first(d):
    """
    >>> import datetime
    >>> d = datetime.datetime(year=2018, month=1, day=2)
    >>> date_format_day_first(d)
    '2 January 2018'

    >>> d = datetime.datetime(year=2018, month=1, day=3)
    >>> date_format_day_first(d)
    '3 January 2018'
    """
    return d.strftime('%-d %B %Y')

