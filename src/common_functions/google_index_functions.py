#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import json
import httplib2

from google.appengine.api import memcache
from google.appengine.api import urlfetch
from oauth2client.contrib.appengine import AppAssertionCredentials


class IndexAPI():
    def __init__(self):
        logging.debug('calling google index api')
        urlfetch.set_default_fetch_deadline(60)
        self.service = self.get_service()
        self.endpoint = "https://indexing.googleapis.com/v3/urlNotifications:publish"


    def get_service(self):
        # Authorise access to Index API using the user's credentials
        scopes = [ "https://www.googleapis.com/auth/indexing"]
        credentials = AppAssertionCredentials(scope=scopes)
        http = credentials.authorize(httplib2.Http(memcache))
        # The service object is the gateway to your API functions
        return http


    def update_url(self, url):
        content = {}
        content['url'] = url
        content['type'] = 'URL_UPDATED'
        logging.debug(json.dumps(content))
        headers = {"Content-type": "application/json", "Accept": "application/json"}
        response, content = self.service.request(self.endpoint, method="POST", body=json.dumps(content), headers=headers)
        try:
            logging.debug(response)
            logging.debug(content)
        except:
            logging.exception('error with update_url')


    def delete_url(self, url):
        content = {}
        content['url'] = url
        content['type'] = 'URL_DELETED'
        logging.debug(json.dumps(content))
        headers = {"Content-type": "application/json", "Accept": "application/json"}
        response, content = self.service.request(self.endpoint, method="POST", body=json.dumps(content), headers=headers)
        try:
            logging.debug(response)
            logging.debug(content)
        except:
            logging.exception('error with delete_url')
