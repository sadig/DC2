# -*- coding: utf-8 -*-
#
# (DC)² - DataCenter Deployment Control
# Copyright (C) 2010, 2011, 2012, 2013, 2014 Stephan Adig <sh@sourcecode.de>
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

import sys
import re

try:
    import web
except ImportError as e:
    print(e)
    print "You need to install web.py"
    sys.exit(1)


class Controller(object):

    def __init__(self, *args, **kwargs):
        self._request_context = kwargs.get('request_context', None)
        self._controller_path = kwargs.get('controller_path', None)
        self._initialize_verbs()
        self._REQ_METHODS = {}

    def set_context(self, ctx):
        self._request_context = ctx

    def _initialize_verbs(self):
        self._verb_methods = {
            'GET': [],
            'POST': [],
            'PUT': [],
            'DELETE': []
        }

    def add_process_method(self, action_name='', action_method=None):
        if action_name is None or action_name == '':
            raise ValueError('action_name can\'t be None or empty')
        if action_name in self._REQ_METHODS:
            raise ValueError('action_name \'{0}\' is already defined'.format(
                action_name))
        if action_method is None:
            raise ValueError('action_method is none')

        self._REQ_METHODS[action_name] = action_method

    def add_url_handler_to_verb(
        self,
        verb='GET',
        urlre='^$',
        action_name='',
            **kwargs):
        url_regexp = '^%s/%s$' % (self._controller_path, urlre)
        verb_method = {'urlre': url_regexp, 'action': action_name}
        if len(kwargs) > 0:
            for key in kwargs.keys():
                verb_method[key] = kwargs[key]
        self._verb_methods[verb].append(verb_method)

    def _content_type(self, *args, **kwargs):
        return 'text/html; charset=utf-8'

    def process(self, path='/'):
        verb = self._process_request(path)
        if verb is not None:
            func = self._REQ_METHODS[verb['action']]
            return func(verb=verb)
        return web.notfound()

    def _process_request(self, path):
        verbs = self._verb_methods[self._request_context.method.upper()]
        for verb in verbs:
            found = re.search(verb['urlre'], path)
            if found is not None:
                verb['request_data'] = found.groupdict()
                return verb

    def _prepare_output(self, *args, **kwargs):
        return 'No Output'
