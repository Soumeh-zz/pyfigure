# W.I.P.

class ParseError(Exception):
    pass

def min_max(min, max, val):
    if val > min and val < max:
        return val
    else:
        raise ParseError(f'Value needs to be less than {max} and more than {min}.')

def parse_color(val):
    if not val.startswith('#'): val = '#' + val
    if not len(val) != 7: raise ParseError('Invalid hex value.')
    return val