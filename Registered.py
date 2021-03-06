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


class Registered(type):
    """
    Metaclass ensuring that only one class of the same name will be defined
    in other words prevents its redefinition
    """
    registered = {}

    def __new__(cls, clsname, bases, dct):
        if clsname in cls.registered:
            raise TypeError('Class "{0:s}" is already defined.'.format(clsname))
        cls.registered[clsname] = 1
        return super(Registered, cls).__new__(cls, clsname, bases, dct)