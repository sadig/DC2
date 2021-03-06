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

#
# Std. Python Libs
#
import sys

try:
    from dc2.lib.db.mongo import Table
except ImportError:
    print('You do not have dc2.lib installed!')
    sys.exit(1)

try:
    from settings import MONGOS
except ImportError:
    print('You do not have a settings file!')
    sys.exit(1)

tbl_interfacetypes = Table(MONGOS["admincenter"]["database"].get_table(
    "interfacetypes"))


def itype_list():
    result = tbl_interfacetypes.find()
    if result is not None:
        return result
    return []


def itype_new():
    rec = {}
    rec['type'] = ''
    rec['desc'] = ''
    return rec


def itype_add(rec=None):
    if rec is None or not isinstance(rec, dict):
        raise ValueError('rec is not a Dict type or rec is None')
    if 'type' not in rec or 'desc' not in rec:
        raise ValueError("no 'type' or 'desc' in rec")
    doc_id = tbl_interfacetypes.save(rec)
    return doc_id


def itype_update(rec=None):
    if rec is None or not isinstance(rec, dict):
        raise ValueError('rec is not a Dict type or rec is None')
    if '_id' not in rec:
        raise ValueError("no '_id'")
    if tbl_interfacetypes.find_one({'_id': rec['_id']}) is not None:
        doc_id = tbl_interfacetypes.save(rec)
        return doc_id
    return None


def itype_get(rec=None):
    if rec is None or not isinstance(rec, dict):
        raise ValueError('rec is not a Dict type or rec is None')
    if '_id' not in rec:
        raise ValueError("no '_id'")
    result = tbl_interfacetypes.find_one(rec)
    if result is not None:
        return result
    return None


def itype_delete(rec=None):
    if rec is None or not isinstance(rec, dict):
        raise ValueError('rec is not a Dict type or rec is None')
    if '_id' not in rec:
        raise ValueError("no '_id'")

    result = tbl_interfacetypes.remove(rec)
    return result
