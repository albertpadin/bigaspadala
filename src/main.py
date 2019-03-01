#!/usr/bin/env python
# -*- coding: utf-8 -*-


import webapp2
import logging


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write("Hello")


app = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)
