#!/usr/bin/env python
"""
 (C) Copyright 2013, Jaromir Sedlacek <jaromir.sedlacek@gmail.com>

 All rights reserved.

 This is free software; you can redistribute it and/or modify it
 under the terms of the GNU Lesser General Public License (LGPL) as
 published by the Free Software Foundation; either version 3.0 of
 the License, or (at your option) any later version.

 This software is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 GNU LGPL http://www.gnu.org/licenses/lgpl.html.



 httpdate converts http-date rfc2616 string to datetime object and datetime object to rfc1123 string

 examples:
    # get datetime object from rfc850-date string
    httpdate('Sunday, 06-Nov-94 08:49:37 GMT')

    # get datetime object from rfc1123-date string
    httpdate('Sun, 06 Nov 1994 08:49:37 GMT')

    # convert ascitime-date string to rfc1123
    httpdate(httpdate('Sun Nov  6 08:49:37 1994'))
"""

from re import compile
from datetime import datetime

wkdayl = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
weekdayl = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
monthl = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# rfc2116 http://www.w3.org/Protocols/rfc2616/rfc2616-sec3.html#sec3.3.1

wkday = '(?P<wkday>(?i)(' + '|'.join(wkdayl) + '))'
weekday = '(?P<weekday>(?i)(' + '|'.join(weekdayl) + '))'
month = '(?P<month>(?i)(' + '|'.join(monthl) + '))'
time = '((?P<hour>([01][0-9])|([2][0-3]))[:](?P<min>[0-5][0-9]):(?P<sec>[0-5][0-9]))'
day2digit = '([0][1-9]|[12][0-9]|[3][01])'
day1digit = '([ ][1-9])'
year2digit = '(?P<year>[0-9][0-9])'
year4digit = '(?P<year>[0-9][0-9][0-9][0-9])'
date3 = '(' + month + '[ ]' + '(?P<day>' + day2digit + '|' + day1digit + ')' + ')'
date2 = '(' + '(?P<day>' + day2digit + ')' + '[-]' + month + '-' + year2digit + ')'
date1 = '(' + '(?P<day>' + day2digit + ')' + '[ ]' + month + '[ ]' + year4digit + ')'
ascitime = '(' + wkday + '[ ]' + date3 + '[ ]' + time + '[ ]' + year4digit + ')'
rfc850 = '(' + weekday + '[,][ ]*' + date2 + '[ ]' + time + '[ ]GMT)'
rfc1123 = '(' + wkday + '[,][ ]*' + date1 + '[ ]' + time + '[ ]GMT)'

re_asc = compile('^' + ascitime + '$')
re_850 = compile('^' + rfc850 + '$')
re_1123 = compile('^' + rfc1123 + '$')


#noinspection PyShadowingBuiltins,PyShadowingNames
def __mapdate(datedict):
    """
    To avoid issues with locales, I do my own mapping
    @param datedict:    groupdict from regexp
    @return:            datestring, format
    """
    month = monthl.index(datedict['month']) + 1
    if 'wkday' in datedict:
        wkday = wkdayl.index(datedict['wkday'])
    else:
        wkday = weekdayl.index(datedict['weekday'])
    year = datedict['year']
    day = datedict['day']
    if day[0] == ' ':
        day = '0' + day[1]
    hour = datedict['hour']
    min = datedict['min']
    sec = datedict['sec']

    # I know it is not nice to go through string and strptime,
    # but it seems to be easiest and most robust I could find way
    #      [%y|%Y]-  %m   - %d    %w    %H  : %M  : %S   %Z
    _date = '{0:s}-{1:02d}-{2:s} {3:d} {4:s}:{5:s}:{6:s} UTC'.format(year, month, day, wkday, hour, min, sec)
    _format = ('%Y' if len(year) == 4 else '%y') + '-%m-%d %w %H:%M:%S %Z'
    return datetime.strptime(_date, _format)


#noinspection PyShadowingNames
def __gendate(_datetime):
    """
    To avoid issues with locale, I do conversion myself
    @param _datetime:   datetime object
    @return:            rfc1123-date string
    """
    year, month, day, hour, minute, second, wkday, dayyear, dst = _datetime.utctimetuple()
    wkday += 1      # (Monday = 0)
    if wkday >= len(wkdayl):
        wkday = 0
        # rfc1123-date:   Sun, 06 Nov 1994 08:49:37 GMT
    return '{0:s}, {1:02d} {2:s} {3:04d} {4:02d}:{5:02d}:{6:02d} GMT'.format(wkdayl[wkday], day,
                                                                             monthl[month - 1], year,
                                                                             hour, minute, second)


def httpdate(datestring):
    """
    Converts http-date (rfc2616) to datetime objects or datetime object to rfc1123-date string
    @param datestring:      either rfc2616 http-date string or datetime object
    @return:                rfc1123-date string if datestring is instance of datetime object else datetime object
    """
    if isinstance(datestring, datetime):
        # generate http-date (rfc2616) rfc1123-date string
        return __gendate(datestring)
    else:
        # parse http-date (rfc2616) ascitime-date, rfc850-date, rfc1123-date strings
        match = re_1123.search(datestring)
        if match is not None:
            # rfc1123-date
            return __mapdate(match.groupdict())
        match = re_850.search(datestring)
        if match is not None:
            # rfc850-date
            return __mapdate(match.groupdict())
        match = re_asc.search(datestring)
        if match is not None:
            # asctime-date
            return __mapdate(match.groupdict())
        raise ValueError('It seems that "{0:s}" does not conform http-date rfc2616.'.format(datestring))