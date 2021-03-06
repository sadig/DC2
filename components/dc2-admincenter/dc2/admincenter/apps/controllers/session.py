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

try:
    import web
except ImportError as e:
    print(e)
    print("You need to install web.py")
    sys.exit(1)

try:
    from dc2.admincenter.globals import logger
except ImportError as e:
    print(e)
    print("You are missing the necessary DC2 modules")
    sys.exit(1)

try:
    from jinja2 import Environment
    from jinja2 import FileSystemLoader
except ImportError as e:
    print(e)
    print("You didn't install jinja2 templating engine")
    sys.exit(1)

try:
    from dc2.lib.web.csrf import csrf_protected
    from dc2.lib.web.controllers import RESTController
    from dc2.lib.decorators import Logger
except ImportError as e:
    print(e)
    print("You are missing the necessary DC2 modules")
    sys.exit(1)

try:
    from settings import TEMPLATE_DIR
    from settings import KERBEROS_AUTH_ENABLED
except ImportError as e:
    print(e)
    print("You don't have a settings file")
    sys.exit(1)

try:
    from dc2.admincenter.lib.auth import do_kinit
    from dc2.admincenter.lib.auth import KerberosAuthError
    from dc2.admincenter.lib.auth import needs_auth
except ImportError as e:
    print(e)
    print("There are dc2.admincenter modules missing")
    sys.exit(1)

tmpl_env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))


class SessionLoginController(RESTController):
    @csrf_protected
    @Logger(logger=logger)
    def _create(self, *args, **kwargs):
        verb = kwargs.get('verb', None)
        params = web.input()
        if 'error' in web.ctx.session:
            del web.ctx.session.error
            del web.ctx.session.errorno
            del web.ctx.session.errormsg
        if KERBEROS_AUTH_ENABLED:
            try:
                do_kinit(params.username, params.password)
                web.ctx.session.authenticated = True
                web.ctx.session.username = params.username
                result = self._prepare_output(
                    verb['request_type'],
                    verb['request_content_type'],
                    output={'redirect': {'url': '/', 'absolute': True}})

            except KerberosAuthError, e:
                web.ctx.session.authenticated = False
                web.ctx.session.error = True
                web.ctx.session.errorno = 1020
                web.ctx.session.errormsg = e
                result = self._prepare_output(
                    verb['request_type'],
                    verb['request_content_type'],
                    output={'redirect': {'url': '/', 'absolute': True}})
        # TODO: Standard Auth
        else:
            web.ctx.session.authenticated = True
            web.ctx.session.username = params.username
            result = self._prepare_output(
                verb['request_type'],
                verb['request_content_type'],
                output={'redirect': {'url': '/', 'absolute': True}})
        return result


class SessionLogoutController(RESTController):
    @needs_auth
    @Logger(logger=logger)
    def _index(self, *args, **kwargs):
        verb = kwargs.get('verb', None)
        web.ctx.session.kill()
        result = self._prepare_output(
            verb['request_type'],
            verb['request_content_type'],
            output={'redirect': {'url': '/', 'absolute': True}})
        return result
