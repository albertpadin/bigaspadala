#!/usr/bin/env python
# -*- coding: utf-8 -*-


import webapp2
import logging

from handlers.pages.front import FrontPage


app = webapp2.WSGIApplication([
    ('/', FrontPage)
], debug=True)
