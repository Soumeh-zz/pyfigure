from typing import Union

Number = Union[float, int]

class ParseError(Exception):
    pass

def min_max(val: Number, min: Number = None, max: Number = None) -> Number:
    if min and max:
        if val > min and val < max:
            return val
        else:
            raise ParseError(f'Value needs to be less than {max} and more than {min}')
    if max:
        if val < max:
            return val
        else:
            raise ParseError(f'Value needs to be less than {max}')
    if min:
        if val > min:
            return val
        else:
            raise ParseError(f'Value needs to be more than {min}')
    return val

if __name__ == '__main__':
    print(min_max(8, max=7))