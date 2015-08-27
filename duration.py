# -*- coding: UTF-8 -*-

import re
import datetime

_nanosecond_size  = 1
_microsecond_size = 1000 * _nanosecond_size
_millisecond_size = 1000 * _microsecond_size
_second_size      = 1000 * _millisecond_size
_minute_size      = 60   * _second_size
_hour_size        = 60   * _minute_size

def _to_str_small(total_seconds, sign):

    result_str = ""
    nanoseconds = total_seconds * _second_size

    if not nanoseconds:
        return "0"

    milliseconds = int(nanoseconds / _millisecond_size)
    if milliseconds:
        nanoseconds -= _millisecond_size * milliseconds
        result_str += "{}ms".format(milliseconds)

    microseconds = int(nanoseconds / _microsecond_size)
    if microseconds:
        nanoseconds -= _microsecond_size * microseconds
        result_str += "{}us".format(microseconds)

    if nanoseconds:
        result_str += "{}ns".format(nanoseconds)

    return "{}{}".format(sign, result_str)


def _to_str_large(total_seconds, sign):

    result_str = ""
    nanoseconds = total_seconds * _second_size

    hours = int(nanoseconds / _hour_size)
    if hours:
        nanoseconds -= _hour_size * hours
        result_str += "{}h".format(hours)

    minutes = int(nanoseconds / _minute_size)
    if minutes:
        nanoseconds -= _minute_size * minutes
        result_str += "{}m".format(minutes)

    seconds = float(nanoseconds) / float(_second_size)
    if seconds:
        nanoseconds -= _second_size * seconds
        result_str += "{}s".format(seconds)

    return "{}{}".format(sign, result_str)


def to_str(delta):

    total_seconds = delta.total_seconds()
    sign = "-" if total_seconds < 0 else ""

    if total_seconds < 1:
        return _to_str_small(abs(total_seconds), sign)
    else:
        return _to_str_large(abs(total_seconds), sign)


def from_str(duration):

    units = {
        "ns" : _nanosecond_size,
        "us" : _microsecond_size,
        "µs" : _microsecond_size,
        "μs" : _microsecond_size,
        "ms" : _millisecond_size,
        "s"  : _second_size,
        "m"  : _minute_size,
        "h"  : _hour_size
    }

    if duration in ("0", "+0", "-0"):
        return datetime.timedelta()

    pattern = re.compile('([\-\+\d\.]+)([a-z]+)')
    total = 0
    sign = -1 if duration[0] == '-' else 1
    matches = pattern.findall(duration)

    if not len(matches):
        raise Exception("invalid duration")

    for (value, unit) in matches:
        if unit not in units:
            raise Exception(
                "Unknown unit {} in duration {}".format(unit, duration))
        try:
            total += int(value) * units[unit]
        except:
            raise Exception(
                "Invalid value {} in duration {}".format(value, duration))

    microseconds = total / _microsecond_size
    return datetime.timedelta(microseconds=sign * microseconds)

