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
except ImportError as e:
    print('You do not have dc2.lib installed!')
    print(e)
    sys.exit(1)

try:
    from settings import MONGOS
except ImportError as e:
    print 'You do not have a settings file!'
    print e
    sys.exit(1)

tbl_ribs = Table(MONGOS["admincenter"]["database"].get_table("ribtypes"))


def rib_list():
    result = tbl_ribs.find(sort_fieldname='remote_type')
    if result is not None:
        return result
    return []


def rib_new():
    rec = {}
    rec['remote_type'] = ''
    rec['name'] = ''
    return rec


def rib_add(rec=None):
    if rec is None or not isinstance(rec, dict):
        raise ValueError('rec is not a Dict type or rec is None')
    if 'remote_type' not in rec or 'name' not in rec:
        raise ValueError("no 'title' or 'backend_url' in rec")
    doc_id = tbl_ribs.save(rec)
    return doc_id


def rib_update(rec=None):
    if rec is None or not isinstance(rec, dict):
        raise ValueError('rec is not a Dict type or rec is None')
    if '_id' not in rec:
        raise ValueError("no '_id'")
    if tbl_ribs.find_one({'_id': rec['_id']}) is not None:
        doc_id = tbl_ribs.save(rec)
        return doc_id
    return None


def rib_get(rec=None):
    if rec is None or not isinstance(rec, dict):
        raise ValueError('rec is not a Dict type or rec is None')
    if '_id' not in rec:
        raise ValueError("no '_id'")
    result = tbl_ribs.find_one(rec)
    if result is not None:
        return result
    return None


def rib_delete(rec=None):
    if rec is None or not isinstance(rec, dict):
        raise ValueError('rec is not a Dict type or rec is None')
    if '_id' not in rec:
        raise ValueError("no '_id'")
    result = tbl_ribs.remove(rec)
    return result
