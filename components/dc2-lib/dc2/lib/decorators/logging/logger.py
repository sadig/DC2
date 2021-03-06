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


class Logger(object):
    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs
        self._logger = None
        if 'logger' in self._kwargs:
            self._logger = self._kwargs.get('logger', None)

    def _debug(self, msg):
        if self._logger is not None:
            self._logger.debug(msg)

    def __call__(self, func):
        def newf(*args, **kwargs):
            slf = args[0]
            self._debug('CLASS: {0}\tMETHOD: {1}'.format(
                slf.__class__.__name__,
                func.__name__))
            ret = func(*args, **kwargs)
            return ret
        return newf
