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

import argparse

PARSER = argparse.ArgumentParser()
SUBPARSERS = PARSER.add_subparsers()


def _output(result, message):
    if result is False:
        print('ERROR: {0}'.format(message))
    else:
        print(message)

from . import servers # noqa
from . import hosts # noqa
from . import discovery # noqa
from . import state  # noqa
from . import dhcp_mgmt  # noqa
from . import ip_mgmt  # noqa
from . import environments  # noqa