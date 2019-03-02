#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import jinja2
import re
import webapp2
import datetime
import logging
import time
import json
import gc

from request_vars import clear_global_variables

from google.appengine.api import memcache
try:
    from google.appengine.api.runtime import runtime
except:
    logging.exception('error in importing runtime')

import settings


reg_b = re.compile(r"(android|bb\\d+|meego).+mobile|avantgo|bada\\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\\.(browser|link)|vodafone|wap|windows ce|xda|xiino", re.I|re.M)
reg_v = re.compile(r"1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\\-(n|u)|c55\\/|capi|ccwa|cdm\\-|cell|chtm|cldc|cmd\\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\\-s|devi|dica|dmob|do(c|p)o|ds(12|\\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\\-|_)|g1 u|g560|gene|gf\\-5|g\\-mo|go(\\.w|od)|gr(ad|un)|haie|hcit|hd\\-(m|p|t)|hei\\-|hi(pt|ta)|hp( i|ip)|hs\\-c|ht(c(\\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\\-(20|go|ma)|i230|iac( |\\-|\\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\\/)|klon|kpt |kwc\\-|kyo(c|k)|le(no|xi)|lg( g|\\/(k|l|u)|50|54|\\-[a-w])|libw|lynx|m1\\-w|m3ga|m50\\/|ma(te|ui|xo)|mc(01|21|ca)|m\\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\\-2|po(ck|rt|se)|prox|psio|pt\\-g|qa\\-a|qc(07|12|21|32|60|\\-[2-7]|i\\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\\-|oo|p\\-)|sdk\\/|se(c(\\-|0|1)|47|mc|nd|ri)|sgh\\-|shar|sie(\\-|m)|sk\\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\\-|v\\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\\-|tdg\\-|tel(i|m)|tim\\-|t\\-mo|to(pl|sh)|ts(70|m\\-|m3|m5)|tx\\-9|up(\\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\\-|your|zeto|zte\\-", re.I|re.M)


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader('public/templates/'), autoescape=True, trim_blocks=True)


def split_len(seq, length):
    return [seq[i:i+length] for i in range(0, len(seq), length)]


def long_log(label, msg):
    if len(msg) > 10000:
        texts = split_len(msg, 10000)
        for t in texts:
            logging.debug('{}: {}'.format(label, t))
    else:
        logging.debug('{}: {}'.format(label, msg))


class BaseHandler(webapp2.RequestHandler):
    def __init__(self, request=None, response=None):
        try:
            logging.info('memory consumption start : {}'.format(runtime.memory_usage()))
            self.mem_start = float(runtime.memory_usage().current())

            if self.mem_start >= 100:
                message = u'Request starting at already {} MB - {}'.format(self.mem_start, request.path_url)
                logging.warning(message)
        except:
            logging.exception('error in logging memory consumption')

        clear_global_variables()
        gc.collect()  # to prevent memory leak
        self.initialize(request, response)

        # Protect against duplicate transactions - respond with a special DUPLICATE REQUEST ERROR error
        # if received a second transaction after already processing a request with the same request id.
        request_id = self.get_arg('request_id')
        if request_id:
            logging.debug('request_id: ' + str(request_id))
            if memcache.get('request_id-{}'.format(request_id)):
                self.abort(409)
                return
            memcache.set('request_id-{}'.format(request_id), True)

        self.api_response = {}
        self.api_response = {
            'error_code': 'NONE'
        }

        self.custom_code = None

        self.is_bot = False

        self.user_agent = self.request.headers.get('User-Agent')

        self.user_agent_is_mobile = False
        self.user_agent_is_android = False
        if self.user_agent:
            if 'android' in self.user_agent.lower():
                self.user_agent_is_android = True
                logging.debug('User is using Android User Agent')

            try:
                b = reg_b.search(self.user_agent)
                v = reg_v.search(self.user_agent[0:4])

                if b or v:
                    self.user_agent_is_mobile = True
            except:
                logging.exception('error in detecting user_agent_is_mobile')

        if settings.test_server():
            logging.debug(self.request.headers)

        self.ip_country = self.request.headers["X-AppEngine-Country"].lower()
        try:
            self.ip_region = self.request.headers["X-AppEngine-Region"].lower()
        except:
            logging.exception('error in getting X-AppEngine-Region')
            self.ip_region = None
        try:
            self.ip_city = self.request.headers["X-AppEngine-City"].lower()
        except:
            logging.exception('error in getting X-AppEngine-City')
            self.ip_city = None
        try:
            self.ip_city_lat_long = self.request.headers["X-AppEngine-CityLatLong"]
        except:
            logging.exception('error in getting X-AppEngine-CityLatLong')
            self.ip_city_lat_long = None
        
        logging.debug('ip_country : {}'.format(self.ip_country))
        logging.debug('ip_region : {}'.format(self.ip_region))
        logging.debug('ip_city : {}'.format(self.ip_city))

        self.tv = {
            "current_uri": os.environ['PATH_INFO'],
            "version": os.environ.get('CURRENT_VERSION_ID')
        } # Global

        url_http = str(os.environ['wsgi.url_scheme'])
        url_next = "://" + str(os.environ['HTTP_HOST'])
        self.base_url = url_http + url_next
        self.tv["BASE_URL"] = self.base_url

        arguments = self.request.arguments()
        for argument in arguments:
            try:
                if not settings.test_server():
                    if argument in ['password'] or argument.startswith('do_not_log_'):
                        logging.debug(argument + ': <redacted>')
                    else:
                        long_log(argument, self.get_arg(argument))
                else:
                    long_log(argument, self.get_arg(argument))
            except:
                logging.debug(argument)
                logging.exception('error in logging argument')

        self.now = datetime.datetime.now()
        self.today = datetime.date(self.now.year, self.now.month, self.now.day)
        self.user = self.get_current_user()

        if self.flag_is_set('500'):
            self.abort(500)

        if self.flag_is_set('400'):
            self.abort(400)

        if self.flag_is_set('404'):
            self.abort(404)

        if self.flag_is_set('409'):
            self.abort(409)

        if self.flag_is_set('423'):
            self.abort(423)

        if self.flag_is_set('415'):
            self.abort(415)

        if self.flag_is_set('403'):
            self.abort(403)

        if self.flag_is_set('401'):
            self.abort(401)

        try:
            logging.info('memory consumption end of init : {}'.format(runtime.memory_usage()))
        except:
            logging.exception('error in logging memory consumption')


    def get_arg(self, arg, default=None):
        if default:
            result = self.request.get(arg, default)
        else:
            result = self.request.get(arg)

        try:
            if result.startswith('"') and result.endswith('"'):
                # Decode with unicode-escape to get Py2 unicode/Py3 str, but interpreted
                # incorrectly as latin-1
                result = result.encode('utf8')
                badlatin = result.decode('unicode-escape')

                # Encode back as latin-1 to get back the raw bytes (it's a 1-1 encoding),
                # then decode them properly as utf-8
                result = badlatin.encode('latin-1').decode('utf-8')
        except AttributeError:
            return None
        except:
            logging.exception('error in decoding argument')

        try:
            if result.startswith('"') and result.endswith('"'):
                result = result[1:-1]
        except AttributeError:
            return None
        except:
            logging.exception('error in retrieving argument 2')
        return result


    def flag_is_set(self, flag):
        if self.get_arg(flag) and self.get_arg(flag) == '1':
            return True
        return False


    def send_error_to_frontend(self, error_code, payload=None):
        logging.error('sending error to frontend: {}'.format(error_code))
        self.api_response['code'] = 400
        self.api_response['error_code'] = error_code
        self.api_response['payload'] = payload
        self.api_render()


    def send_access_denied(self):
        self.api_response['code'] = 403
        self.api_response['success'] = False
        self.api_response['description'] = 'Error! Access Denied.'
        self.api_render()


    def handle_exception(self, exception, debug):
        # TODO: Catch custom exceptions and abort
        # Log the error.
        logging.exception(exception)

        # If the exception is a HTTPException, use its error code.
        # Otherwise use a generic 500 error code.
        if isinstance(exception, webapp2.HTTPException):
            self.response.set_status(exception.code)
        else:
            self.response.set_status(500)


    def check_etag(self, cache_header_already_set=False):
        self.response.md5_etag()
        etag = self.response.etag

        etag_with_quotes = '"' + etag + '"'
        if 'If-None-Match' in self.request.headers and self.request.headers['If-None-Match']:
            if self.request.headers['If-None-Match'] in [etag, etag_with_quotes]:
                self.response.clear()
                self.response.status = '304 Not Modified'
                return

        if not cache_header_already_set:
            self.response.headers['Cache-Control'] = "private"


    def render(self, template_path=None, cache_header_already_set=False):
        self.tv["user"] = self.user
        self.tv["year"] = self.now.year
        self.tv["site_name"] = settings.SITE_NAME
        self.tv["current_timestamp"] = time.mktime(self.now.timetuple())
        self.tv["current_url"] = self.request.uri
        self.tv["current_path_url"] = self.request.path_url
        self.tv["google_analytics_id"] = settings.GOOGLE_ANALYTICS_ID

        template = jinja_environment.get_template(template_path)
        self.response.out.write(template.render(self.tv))

        self.check_etag(cache_header_already_set=cache_header_already_set)


    def api_render(self):
        try:
            logging.info('memory consumption start of api_render : {}'.format(runtime.memory_usage()))
        except:
            logging.exception('error in logging memory consumption')

        self.response.headers['Content-Type'] = "application/json"
        if self.custom_code and self.custom_code != 200:
            logging.debug('code: ' + str(self.custom_code))
            self.response.set_status(self.custom_code)

        elif 'code' in self.api_response and self.api_response['code'] != 200:
            logging.debug('code: ' + str(self.api_response['code']))
            self.response.set_status(self.api_response['code'])

        string_response = json.dumps(self.api_response, ensure_ascii=False).encode('utf8')
        try:
            logging.debug('string_response_length : {}'.format(len(string_response)))
            if settings.test_server():
                logging.info("API Response >> ")
                if len(string_response) < 25000:
                    logging.info(string_response)
                else:
                    logging.info(string_response[:25000])
        except:
            logging.exception('error logging api_response')
        self.response.out.write(string_response)
        self.check_etag()

        try:
            logging.info('memory consumption end of api_render : {}'.format(runtime.memory_usage()))
            self.mem_end = float(runtime.memory_usage().current())

            if (self.mem_end - self.mem_start) > 5:
                message = u'request consumed {} MB - {}'.format((self.mem_end - self.mem_start), self.request.path_url)
                logging.warning(message)
        except:
            logging.exception('error in logging memory consumption')


    def get_current_user(self):
        # TODO: get user
        
        return None


    def validate_required(self, list_of_required_parameters):
        arguments = self.request.arguments()
        for required in list_of_required_parameters:
            try:
                assert required in arguments
            except AssertionError:
                logging.exception('missing required argument: ' + required)
                raise Exception('Missing required argument: ' + required)
