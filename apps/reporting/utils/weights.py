#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


from compiler.ast import flatten
import re


DELIMITER = r"(?:\A|[\s;,\*]+|\Z)"


UNIT_PATTERNS = {

    # PLANET EARTH
    "gram":  "g|gram|grams",
    "kilo":  "kg|kilo|kilos|kilogram|kilograms|kilogramme|kilogrammes",
    "tonne": "t|tonne|tonnes|metric\s+ton|metric\s+tons|megagram|megagrams",

    # AMERICA
    "ounce": "oz|ounce|ounces",
    "pound": "lb|pound|pounds",
    "stone": "st|stone|stones"
}


MULTIPLIERS = {
    "gram":  0.001,
    "kilo":  1,
    "tonne": 1000,
    "ounce": 0.0283495231,
    "pound": 0.45359237,
    "stone": 6.35029318,
}


FLOAT_PATTERN = r"\d+(?:\.\d+)?"
UNIT_PATTERN = "|".join(UNIT_PATTERNS.values())
REGEX = re.compile(
    r"%s(%s)\s*(%s)%s" %\
        (DELIMITER, FLOAT_PATTERN,
        UNIT_PATTERN, DELIMITER),
    re.I)


def extract_weight(text):
    """
        Attempts to extract a string that looks like a weight from *text*, and
        returns a tuple containing the weight in kilograms (a float), and the
        remainder of *text*. Many formats are supported:

          >>> extract_weight("10kg")
          (10.0, '')

          >>> extract_weight("15 kilos")
          (15.0, '')

          >>> extract_weight("20 kilogrammes")
          (20.0, '')

        Also, many units are supported. The output is always converted into
        kilograms before being returned, making this function unit-agnostic:

          >>> extract_weight("25lb")
          (11.33980925, '')

          >>> extract_weight("30 stones")
          (190.50879540000003, '')

        Since the remainder is returned, this function can be used to extract
        weights from arbitrary strings quite easily (like tags.models.Tag):

          >>> extract_weight("xx 40 pounds yy")
          (18.143694800000002, 'xx yy')

          >>> extract_weight("REPORT ON #1234. Weight 45kg, Height 100cm")
          (45.0, 'REPORT ON #1234. Weight Height 100cm')
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

            # convert the result to kilos
            kg = float(num_str) * MULTIPLIERS[unit]
            return (kg, remainder)


# run the doctests if this
# module was invoked directly
if __name__ == "__main__":
    import doctest
    doctest.testmod()
