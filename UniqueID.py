#!/usr/bin/env python
"""
 (C) Copyright 2013, Jaromir Sedlacek (jaromir.sedlacek@gmail.com).

 All rights reserved.

 This is free software; you can redistribute it and/or modify it
 under the terms of the GNU Lesser General Public License (LGPL) as
 published by the Free Software Foundation; either version 3.0 of
 the License, or (at your option) any later version.

 This software is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 GNU LGPL http://www.gnu.org/licenses/lgpl.html.
"""

#noinspection PyStatementEffect
"""
set of function for getting unique IDs or names using MD5
"""

from random import random, SystemRandom
from time import time
from hashlib import md5


def unique_id():
    """
    generate unique id based on current time and a random number which can be used as unique transaction ID

    @return:        md5 hexdigest
    """
    #noinspection PyBroadException
    try:
        rnd = SystemRandom().random()
    except:
        rnd = random()

    return md5('{:.31f}'.format(time()).replace('.', '')[:30]
               + '{:.31f}'.format(rnd).replace('.', '')[1:30]).hexdigest()


def unique_name(name='', transaction=unique_id()):
    """
    get unique file name, based on the name and transaction
    it should always return same string for same name and transaction

    @param name:            file name as a base
    @param transaction:     transaction ID
    @return:                md5(name + _seed).hexdigest()
    """

    return md5(name + transaction).hexdigest()
