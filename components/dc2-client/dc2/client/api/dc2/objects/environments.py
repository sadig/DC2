# -*- coding: utf-8 -*-
#
#
# (DC)² - DataCenter Deployment Control
# Copyright (C) 2010, 2011, 2012, 2013, 2014  Stephan Adig <sh@sourcecode.de>
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

import xmlrpclib


class Environments(object):

    def __init__(self, rpcurl=None):
        self._rpcurl = rpcurl
        self._proxy = xmlrpclib.ServerProxy(self._rpcurl, allow_none=True)

    def find_by_name(self, name=None):
        if name is not None:
            environ_list = self._proxy.dc2.configuration.environments.list(
                {"name": name})
            if (environ_list is not None and
                    len(environ_list) > 0 and
                    environ_list[0] is not None):
                return environ_list[0]

    def get_environment_variable(self, env_name=None, env_variable=None):
        if env_name is not None and env_variable is not None:
            environment = self._proxy.dc2.configuration.environments.find(
                {'name': env_name})
            if len(environment) > 0:
                envi = environment[0]
                for i in envi['variables']:
                    if i['name'].upper() == env_variable.upper():
                        return i['value']
        return None
