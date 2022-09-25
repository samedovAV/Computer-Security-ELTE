import base64


def hex2bin(value):
    """
    >>> hex2bin('f')
    '1111'
    >>> hex2bin('5')
    '101'
    >>> hex2bin('1')
    '1'
    """
    return bin(int(value, 16))[2:]


def bin2hex(value):
    """
    >>> bin2hex('1111')
    'f'
    >>> bin2hex('100001')
    '21'
    >>> bin2hex('1')
    '1'
    """
    return hex(int(value, 2))[2:]


def fillupbyte(value):
    """
    >>> fillupbyte('011')
    '00000011'
    >>> fillupbyte('1')
    '00000001'
    >>> fillupbyte('10111')
    '00010111'
    >>> fillupbyte('11100111')
    '11100111'
    >>> fillupbyte('111001111')
    '0000000111001111'
    """
    if len(value) % 8 != 0:
        bytes_count = int(len(value) / 8) + 1
        zeros_needed = bytes_count * 8 - len(value)
        for i in range(zeros_needed):
            value = '0' + value
    return value


def int2base64(value):
    """
    >>> int2base64(0x61)
    'YQ=='
    >>> int2base64(0x78)
    'eA=='
    """
    return base64.b64encode(bytes([int(value)])).decode("utf-8")


def hex2base64(value):
    """
    >>> hex2base64('61')
    'YQ=='
    >>> hex2base64('123456789abcde')
    'EjRWeJq83g=='
    """
    return base64.b64encode(bytes.fromhex(value)).decode()
