# -*- coding: utf-8 -*-
###############################################################################
#
#    (DC)² - DataCenter Deployment Control
#    Copyright (C) 2010, 2011, 2012, 2013, 2014  Stephan Adig <sh@sourcecode.de>
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
###############################################################################

import sys
import os
import os.path
import json
try:
    import web
except ImportError as e:
    print(e)
    print "You need to install web.py"
    sys.exit(1)

try:
    from dc2.admincenter.globals import connectionpool
    from dc2.admincenter.globals import CSS_FILES
    from dc2.admincenter.globals import JS_LIBS
    from dc2.admincenter.globals import ADMIN_MODULES
    from dc2.admincenter.globals import logger
except ImportError as e:
    print(e)
    print "You are missing the necessary DC2 modules"
    sys.exit(1)

try:
    from jinja2 import Environment, FileSystemLoader
except ImportError as e:
    print(e)
    print "You didn't install jinja2 templating engine"
    sys.exit(1)

try:
    from dc2.lib.web.pages import Page
    from dc2.lib.web.csrf import csrf_protected
    from dc2.lib.auth.helpers import get_realname
    from dc2.lib.auth.helpers import check_membership_in_group
    from dc2.lib.web.controllers import RESTController
    from dc2.lib.web.helpers import convert_values
    from dc2.lib.transports import get_xmlrpc_transport
    from dc2.lib.decorators import Logger
except ImportError as e:
    print(e)
    print "You are missing the necessary DC2 modules"
    print e
    sys.exit(1)

try:
    from settings import TEMPLATE_DIR
    from settings import KERBEROS_AUTH_ENABLED
    from settings import GRP_NAME_DC2ADMINS
except ImportError as e:
    print(e)
    print "You don't have a settings file"
    print e
    sys.exit(1)

try:
    from dc2.admincenter.lib import backends
    from dc2.admincenter.lib.controllers import AdminController
    from dc2.admincenter.lib.auth import needs_auth
    from dc2.admincenter.lib.auth import needs_admin
except ImportError as e:
    print(e)
    print "There are dc2.admincenter modules missing"
    print e
    sys.exit(1)

try:
    from dc2.api.dc2.configuration import DefaultClasses
except ImportError as e:
    print(e)
    print "You didn't install dc2.api package"
    print e
    sys.exit(1)

tmpl_env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))


class BackendDefaultClassesController(AdminController):
    CONTROLLER_IDENT = {'title':'DC2 Backends Defaultclasses',
                        'url':'/admin/backends/defaultclasses',
                        'show_in_menu':'False'}

    def _init_backend(self, backend):
        self._transport = get_xmlrpc_transport(backend['backend_url'],
                                               backend['is_kerberos'])
        self._defaultclasses = DefaultClasses(self._transport)

    @needs_auth
    @needs_admin
    @Logger(logger=logger)
    def _index(self, *args, **kwargs):
        params = web.input()
        verb = kwargs.get('verb', None)
        page = self._prepare_page(verb)
        backend_list = backends.backend_list()
        backend_id = params.get('backend_id', None)
        backend = backends.backend_get({'_id':backend_id})
        self._init_backend(backend)
        defaultclasses = self._defaultclasses.list()
        page.set_title('DC2 Admincenter - Backends - Default Classes - Index')
        page.add_page_data({
            'backendlist':backend_list,
            'backend_id':backend_id,
            'backend_defclasses':defaultclasses,
        })
        page.set_action('index')
        result = self._prepare_output(verb['request_type'],
                                      verb['request_content_type'],
                                      output={'content':page.render()})
        return result

    @needs_auth
    @needs_admin
    @Logger(logger=logger)
    def _new(self, *args, **kwargs):
        params = web.input()
        verb = kwargs.get('verb', None)
        page = self._prepare_page(verb)
        backendlist = backends.backend_list()
        backend_id = params.get('backend_id', None)
        backend = backends.backend_get({'_id':backend_id})
        self._init_backend(backend)
        defaultclass = self._defaultclasses.new()
        page.set_title('DC2 Admincenter - Backends - Defaultclasses - Add')
        page.add_page_data({
            'backendlist':backendlist,
            'backend_id':backend_id,
            'defclass':defaultclass,
            })
        page.set_action('new')
        result = self._prepare_output(verb['request_type'],
                                      verb['request_content_type'],
                                      output={'content':page.render()})
        return result

    @needs_auth
    @needs_admin
    @Logger(logger=logger)
    def _edit(self, *args, **kwargs):
        params = web.input()
        verb = kwargs.get('verb', None)
        page = self._prepare_page(verb)
        backendlist = backends.backend_list()
        backend_id = params.get('backend_id', None)
        backend = backends.backend_get({'_id':backend_id})
        self._init_backend(backend)
        defaultclass = self._defaultclasses.get(id=verb['request_data']['id'])
        page.set_title('DC2 Admincenter - Backends - Defaultclasses - Edit')
        page.add_page_data({
            'backendlist':backendlist,
            'backend_id':backend_id,
            'defclass':defaultclass
            })
        page.set_action('edit')
        result = self._prepare_output(verb['request_type'],
                                      verb['request_content_type'],
                                      output={'content':page.render()})
        return result

    @needs_auth
    @needs_admin
    @Logger(logger=logger)
    def _create(self, *args, **kwargs):
        params = web.input()
        verb = kwargs.get('verb', None)
        backend_id = params.get('backend_id', None)
        backend = backends.backend_get({'_id':backend_id})
        self._init_backend(backend)
        defaultclass = {}
        result = json.loads(web.data())
        defaultclass['classname'] = result['result']['defclass']['classname']
        defaultclass['description'] = result['result']['defclass']['description']
        self._defaultclasses.add(defclass=defaultclass)
        output_format = verb.get('request_output_format', None)
        if output_format.lower() == 'json':
            result = self._prepare_output('json',
                                          verb['request_content_type'],
                                          verb['request_output_format'],
                                          {'redirect':
                                           {'url':'%s?backend_id=%s' %
                                            (self._controller_path, backend_id),
                                            'absolute':'true'}})
        else:
            result = self._prepare_output(verb['request_type'],
                                          verb['request_content_type'],
                                          output={'redirect':
                                                  {'url':'%s?backend_id=%s' %
                                                   (self._controller_path,
                                                    backend_id),
                                                   'absolute':'true'}})
        return result

    @needs_auth
    @needs_admin
    @Logger(logger=logger)
    def _update(self, *args, **kwargs):
        params = web.input()
        verb = kwargs.get('verb', None)
        backend_id = params.get('backend_id', None)
        backend = backends.backend_get({'_id':backend_id})
        self._init_backend(backend)
        defaultclass = {}
        result = json.loads(web.data())
        defaultclass['_id'] = verb['request_data']['id']
        defaultclass['classname'] = result['result']['defclass']['classname']
        defaultclass['description'] = result['result']['defclass']['description']
        self._defaultclasses.update(defclass=defaultclass)
        output_format = verb.get('request_output_format', None)
        if output_format.lower() == 'json':
            result = self._prepare_output('json',
                                          verb['request_content_type'],
                                          verb['request_output_format'],
                                          {'redirect':
                                           {'url':'%s?backend_id=%s' %
                                            (self._controller_path, backend_id),
                                            'absolute':'true'}})
        else:
            result = self._prepare_output(verb['request_type'],
                                          verb['request_content_type'],
                                          output={'redirect':
                                                  {'url':'%s?backend_id=%s' %
                                                   (self._controller_path,
                                                    backend_id),
                                                   'absolute':'true'}})
        return result



    @needs_auth
    @needs_admin
    @Logger(logger=logger)
    def _delete(self, *args, **kwargs):
        params = web.input()
        verb = kwargs.get('verb', None)
        backend_id = params.get('backend_id', None)
        backend = backends.backend_get({'_id':backend_id})
        self._init_backend(backend)
        defclass_id = verb['request_data']['id']
        result = self._defaultclasses.delete(id=defclass_id)
        output_format = verb.get('request_output_format', None)
        if output_format.lower() == 'json':
            result = self._prepare_output('json',
                                          verb['request_content_type'],
                                          verb['request_output_format'],
                                          {'redirect':
                                           {'url':'%s?backend_id=%s' %
                                            (self._controller_path, backend_id),
                                            'absolute':'true'}})
        else:
            result = self._prepare_output(verb['request_type'],
                                          verb['request_content_type'],
                                          output={'redirect':
                                                  {'url':'%s?backend_id=%s' %
                                                   (self._controller_path,
                                                    backend_id),
                                                   'absolute':'true'}})
        return result


