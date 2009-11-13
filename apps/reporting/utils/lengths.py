#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


from compiler.ast import flatten
import re


DELIMITER = r"(?:\A|[\s;,\*]+|\Z)"


UNIT_PATTERNS = {
    "mm":   "mm|mill?imet(?:er|re)s?",
    "cm":   "cm|centimet(?:er|re)s?",
    "m":    "m|met(?:er|re)s?",
    "km":   "km|kilomet(?:er|re)s?",
    "inch": 'in|"|inch|inches',
    "foot": "ft|'|foot|feet",
    "yard": "yd|yards?"
}


MULTIPLIERS = {
    "mm": 0.1,
    "cm": 1,
    "m":  100,
    "km": 100000,

    # TODO
    "inch": None,
    "foot": None,
    "yard": None
}


FLOAT_PATTERN = r"\d+(?:\.\d+)?"
UNIT_PATTERN = "|".join(UNIT_PATTERNS.values())
REGEX = re.compile(
    r"%s(%s)\s*(%s)%s" %\
        (DELIMITER, FLOAT_PATTERN,
        UNIT_PATTERN, DELIMITER),
    re.I)


def extract_length(text):
    """
    """

    m = re.search(REGEX, text)

    # no match = nothing to return
    # or extract from the string
    if m is None:
        return (None, text)

    # extract the relevant parts, and crop
    # the matching part from the input
    remainder = (text[:m.start()] + " " + text[m.end():]).strip()
    num_str, unit_str = m.groups()

    # we found a match, but we don't know _which_ unit
    # was matched, so iterate the individual patterns
    for unit, pattern in UNIT_PATTERNS.items():
        if re.match(pattern, unit_str, re.I):

            # convert the result to centimeters
            cm = float(num_str) * MULTIPLIERS[unit]
            return (cm, remainder)


# run the doctests if this
# module was invoked directly
if __name__ == "__main__":
    import doctest
    doctest.testmod()
