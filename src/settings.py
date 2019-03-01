#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Add all the settings here
import os
from google.appengine.api import app_identity


def app_id():
    return app_identity.get_application_id()


def dev_server():
    if os.environ['SERVER_SOFTWARE'].find('Development') == 0:
        return True
    else:
        return False


def test_server():
    return app_id().endswith('-test') or dev_server()


def prod_server():
    return not test_server()


APPENGINE_SERVICE_ACCOUNT = "{}@appspot.gserviceaccount.com".format(app_id())
