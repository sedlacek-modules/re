#!/usr/bin/env python
"""
 (C) Copyright 2014, Jaromir Sedlacek <jaromir.sedlacek@gmail.com>.

 All rights reserved.

 This is free software; you can redistribute it and/or modify it
 under the terms of the GNU Lesser General Public License (LGPL) as
 published by the Free Software Foundation; either version 3.0 of
 the License, or (at your option) any later version.

 This software is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 GNU LGPL http://www.gnu.org/licenses/lgpl.html.


 Formatting either stdin and sending it to stdout (filter mode)
 or formatting stout and stderr of supplied command

 input and output is line buffered.
"""

import argparse

from calendar import timegm
from datetime import datetime
from time import clock, localtime, strftime
from sys import stdout, stderr, stdin
from subprocess import Popen, PIPE
from threading import Thread


def utc_epoch():
    return timegm(datetime.utcnow().utctimetuple())


def cpu_clock():
    return clock()


def timestamp(fmt='%Y-%m-%d %H:%M:%S%Z', time=utc_epoch()):
    return strftime(fmt, localtime(time))


# noinspection PyShadowingNames
class Flush(object):
    """
    Class overriding buffering by doing flush after each write
    """

    def __init__(self, _file):
        self._file = _file

    def write(self, *args, **kwargs):
        self._file.write(*args, **kwargs)
        self._file.flush()

    def writelines(self, *args, **kwargs):
        self._file.writelines(*args, **kwargs)
        self._file.flush()


# noinspection PyShadowingNames
class InOut(object):
    """
    Get Input and pass it reformatted to output
    """

    # noinspection PyDefaultArgument
    def __init__(self, name=None, fmt=None, _in=None, _out=None, values={}):
        if _in is None:
            _in = stdin
        if _out is None:
            _out = Flush(stdout)
        if name is None:
            name = 'input'
        if fmt is None:
            fmt = '{' + name + '}\n'
        self.fmt = fmt
        self.values = values
        self.name = name
        self._in = _in
        self._out = _out


    def process(self):
        while True:
            line = self._in.readline()
            if not line:
                break
            epoch = utc_epoch()
            self.values.update(
                {self.name: line.rstrip(), 'clock': cpu_clock(), 'epoch': epoch, 'timestamp': timestamp(time=epoch)})
            self._out.write(self.fmt.format(**self.values))

    def __call__(self, *args, **kwargs):
        self.process(*args, **kwargs)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Prefix command output')
    parser.add_argument('--stdout', default=None, dest='stdout', metavar='<stdout>', help='format of stdout')
    parser.add_argument('--stderr', default=None, dest='stderr', metavar='<stderr>', help='format of stderr')
    parser.add_argument('--stdin', default=None, dest='stdin', metavar='<stdin>', help='format of stdin')
    parser.add_argument('--timestamp', default='%Y-%m-%d %H:%M:%S%Z', dest='timestamp', metavar='<timestamp>',
                        help='timestamp format, available as {timestamp}')
    parser.add_argument('cmd', nargs='*', metavar='<cmd>', help='command to run')

    args = vars(parser.parse_args())

    if len(args['cmd']) == 0:
        # we just filter stdin
        if args['stdin'] is None:
            args['stdin'] = '{timestamp} {input}\n'
        _stdin = InOut(fmt=args['stdin'])
        _stdin()
    else:
        if args['stdout'] is None:
            args['stdout'] = 'O {timestamp} {stdout}\n'
        if args['stderr'] is None:
            args['stderr'] = 'E {timestamp} {stderr}\n'

        # open process
        process = Popen(args['cmd'], bufsize=1, stdout=PIPE, stderr=PIPE)

        # define threads
        t_stdout = Thread(target=InOut(name='stdout', _in=process.stdout, _out=stdout, fmt=args['stdout']))
        t_stderr = Thread(target=InOut(name='stderr', _in=process.stderr, _out=stderr, fmt=args['stderr']))

        # start threads
        t_stdout.start()
        t_stderr.start()

        # wait for all to finish
        t_stdout.join()
        t_stderr.join()
        process.wait()


