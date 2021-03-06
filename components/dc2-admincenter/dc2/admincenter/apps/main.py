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
    from dc2.admincenter.globals import CSS_FILES
    from dc2.admincenter.globals import JS_LIBS
    from dc2.admincenter.globals import logger
except ImportError as e:
    print(e)
    print("You are missing the necessary DC2 modules")
    sys.exit(1)

try:
    from jinja2 import Environment, FileSystemLoader
except ImportError as e:
    print(e)
    print("You didn't install jinja2 templating engine")
    sys.exit(1)

try:
    from dc2.lib.web.pages import Page
    from dc2.lib.web.csrf import csrf_protected
    from dc2.lib.decorators.logger import Logger
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
except ImportError as e:
    print(e)
    print("There are dc2.admincenter modules missing")
    sys.exit(1)

tmpl_env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))


class Home(object):

    @Logger(logger=logger)
    def GET(self):
        page = Page('index.tmpl', tmpl_env, web.ctx)
        page.set_title('DC2-AdminCenter - Index')
        page.set_cssfiles(CSS_FILES)
        page.set_jslibs(JS_LIBS)
        if ('authenticated' in web.ctx.session and
                web.ctx.session.authenticated):
            user_info = {}
            user_info['username'] = web.ctx.session.username
            user_info['realname'] = web.ctx.session.realname
            user_info['is_dc2admin'] = web.ctx.session.is_dc2admin
            page.add_page_data({'user': user_info})
        return page.render()


class Login(object):

    @csrf_protected
    @Logger(logger=logger)
    def POST(self):
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
                raise web.seeother('/')
            except KerberosAuthError, e:
                web.ctx.session.authenticated = False
                web.ctx.session.error = True
                web.ctx.session.errorno = 1020
                web.ctx.session.errormsg = e
                raise web.seeother('/')
        # TODO: Standard Auth
        else:
            web.ctx.session.authenticated = True
            web.ctx.session.username = params.username
            raise web.seeother('/')
