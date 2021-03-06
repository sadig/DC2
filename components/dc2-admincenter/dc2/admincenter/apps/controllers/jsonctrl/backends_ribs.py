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
    print "You need to install web.py"
    sys.exit(1)

try:
    from dc2.lib.decorators import Logger
    from dc2.lib.transports import get_xmlrpc_transport
    from dc2.lib.exceptions.authentication import KerberosError
except ImportError as e:
    print(e)
    print('you do not have dc2.lib installed')
    sys.exit(1)

try:
    from dc2.admincenter.lib.controllers import JSONController
    from dc2.admincenter.lib import backends
    from dc2.admincenter.lib.auth import needs_auth
    from dc2.admincenter.globals import logger
except ImportError as e:
    print(e)
    print('you have a problem with dc2.admincenter')
    sys.exit(1)

try:
    from dc2.api.dc2.inventory import Ribs
except ImportError as e:
    print(e)
    print('you didn\'t have dc2.api installed')
    sys.exit(1)


class JSONRibBackendController(JSONController):

    def __init__(self, *args, **kwargs):
        super(JSONRibBackendController, self).__init__(*args, **kwargs)
        self._prepare_urls()

    def _prepare_urls(self):
        self.add_url_handler_to_verb('GET', 'backend_rib_delete',
                                     'backend_rib_delete')
        self.add_process_method('backend_rib_delete', self._backend_rib_delete)

    @needs_auth
    @Logger(logger=logger)
    def _backend_rib_delete(self, *args, **kwargs):
        verb = kwargs.get('verb', None)
        if verb is not None:
            try:
                params = web.input()
                backend_id = params.get('backend_id', None)
                rib_id = params.get('rib_id', None)
                if backend_id is not None and rib_id is not None:
                    backend = backends.backend_get({'_id': backend_id})
                    transport = get_xmlrpc_transport(backend['backend_url'],
                                                     backend['is_kerberos'])
                    s = Ribs(transport)
                    s.delete(id=rib_id)
                    result = self._prepare_output(
                        result={'backend_id': backend_id,
                                'entry_type': 'boolean',
                                'entry': True})
                    return result
            except KerberosError as e:
                (first, last) = e.message
                (message, error_no) = last
                result = self._prepare_output(result={'backend_id': backend_id,
                                                      'error': True,
                                                      'error_type': 'Kerberos',
                                                      'error_msg': message,
                                                      'error_no': error_no})
                return result
            result = self._prepare_output(result={'backend_id': backend_id,
                                                  'entry_type': 'boolean',
                                                  'entry': False})
            return result
