#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


import re, datetime


DELIMITER = r"(?:\A|[\s;,\*]+|\Z)"


PATTERN = r"""
    (?P<day>\d{1,2})
    (?P<delimiter>[.-/])
    (?P<month>\d{1,2})
    \2
    (?P<year>\d{2,4})
"""

REGEX = re.compile(DELIMITER + PATTERN + DELIMITER, re.VERBOSE)


def extract_date(text):
    """
        Attempts to extract a string that looks like a D/M/Y date from *text*,
        and returns a tuple containing a corresponding datetime object and the
        remainder of *text*. A few formats are supported:

          >>> extract_date("01.01.2009")
          (datetime.datetime(2009, 1, 1, 0, 0), '')

          >>> extract_date("2/03/2009")
          (datetime.datetime(2009, 3, 2, 0, 0), '')

          >>> extract_date("13/6/84")
          (datetime.datetime(1984, 6, 13, 0, 0), '')
    """

    m = re.search(REGEX, text)

    # no match = nothing to return
    # or extract from the string
    if m is None:
        return (None, text)

    remainder = (text[:m.start()] + " " + text[m.end():]).strip()
    dt_args = [int(m.group(x)) for x in ["year", "month", "day"]]
    return (datetime.datetime(*dt_args), remainder)


# run the doctests if this
# module was invoked directly
if __name__ == "__main__":
    import doctest
    doctest.testmod()
