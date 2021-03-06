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
import re
import types
import json

try:
    import web
except ImportError as e:
    print(e)
    print "You need to install web.py"
    sys.exit(1)

try:
    from dc2.lib.decorators import Logger
    from dc2.lib.transports import get_xmlrpc_transport
except ImportError as e:
    print(e)
    print 'you do not have dc2.lib installed'
    print e
    sys.exit(1)

try:
    from dc2.admincenter.lib.controllers import JSONController
    from dc2.admincenter.lib import backends
    from dc2.admincenter.lib.auth import needs_auth
    from dc2.admincenter.lib.auth import needs_admin
    from dc2.admincenter.globals import logger
except ImportError as e:
    print(e)
    print 'you have a problem with dc2.admincenter'
    print e
    sys.exit(1)

try:
    from dc2.api.dc2.inventory import Servers
except ImportError as e:
    print(e)
    print 'you didn\'t have dc2.api installed'
    print e
    sys.exit(1)


class JSONAdminBackendsServerController(JSONController):
    def __init__(self, *args, **kwargs):
        super(JSONAdminBackendsServerController, self).__init__(*args, **kwargs)
        self._prepare_urls()

    def _prepare_urls(self):
        # Single Server Delete
        self.add_url_handler_to_verb('DELETE', 'backend_server_delete',
                                     'backend_server_delete')
        self.add_process_method('backend_server_delete',
                                self._backend_server_delete)

        # Single Server incl. hosts, installstate etc.
        self.add_url_handler_to_verb('DELETE', 'backend_server_delete_complete',
                              'backend_server_delete_complete')
        self.add_process_method('backend_server_delete_complete',
                                self._backend_server_delete_complete)


    def _init_backends(self, backend_id):
        backend = backends.backend_get({'_id':backend_id})
        transport = get_xmlrpc_transport(backend['backend_url'],
                                         backend['is_kerberos'])
        self._servers = Servers(transport)

    @needs_auth
    @needs_admin
    @Logger(logger=logger)
    def _backend_server_delete(self, *args, **kwargs):
        verb = kwargs.get('verb', None)
        if verb is not None:
            params = web.input()
            backend_id = params.get('backend_id', None)
            server_id = params.get('server_id', None)
            if backend_id is not None and server_id is not None:
                self._init_backends(backend_id)
                if self._servers.delete(server_id=server_id):
                    result = self._prepare_output(result=
                                                  {'redirect':
                                                   {'url':'/backends/%s' %
                                                    (backend_id),
                                                    'absolute':'true'}})
                    return result
        result = self._prepare_output(result=
                                      {'redirect':
                                       {'url':'/backends/%s' % (backend_id),
                                        'absolute':'true'}})

        return result

    @needs_auth
    @needs_admin
    @Logger(logger=logger)
    def _backend_server_delete_complete(self, *args, **kwargs):
        verb = kwargs.get('verb', None)
        if verb is not None:
            params = web.input()
            backend_id = params.get('backend_id', None)
            server_id = params.get('server_id', None)
            if backend_id is not None and server_id is not None:
                self._init_backends(backend_id)
                if self._servers.delete_complete(server_id=server_id):
                    result = self._prepare_output(result=
                                                  {'redirect':
                                                   {'url':'/backends/%s' %
                                                    (backend_id),
                                                    'absolute':'true'}})
                    return result
        result = self._prepare_output(result=
                                      {'redirect':
                                       {'url':'/backends/%s' % (backend_id),
                                        'absolute':'true'}})

        return result
