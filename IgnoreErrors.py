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


class IgnoreErrors(object):
    """
    Container class for ignoring all errors. This class is callable. I use it for cleanup routines after
    unexpected exception is handled and I do not want to damage stack trace prior re-rise original exception
    typical use:

    Ignore(callable[, exceptions])(*args_for_callable, **kwargs_for_callable)

    to run callable without ignoring errors use Ignore.run(*args, **kwargs)
    """

    #noinspection PyShadowingBuiltins
    def __init__(self, callable, exceptions=Exception):
        """
        @param exceptions:       what exceptions to ignore either single exception or tuple of exceptions
        @param callable:        what callable to run
        """
        self.__callable = callable
        self.__exceptions = exceptions

    def run(self, *args, **kwargs):
        """
        runs callable without ignoring exceptions
        """
        return self.__callable(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        """
        runs callable and if exception is instance of exception, it is silently ignored
        """
        #noinspection PyBroadException
        try:
            return self.run(*args, **kwargs)
        except self.__exceptions:
            pass