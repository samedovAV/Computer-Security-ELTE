def hex2bin(hex_string):
    """
    >>> hex2bin('f')
    '1111'
    >>> hex2bin('5')
    '101'
    >>> hex2bin('1')
    '1'
    """
    return bin(int(hex_string, base=16))[2:]


def bin2hex(bin_string):
    """
    >>> bin2hex('1111')
    'f'
    >>> bin2hex('100001')
    '21'
    >>> bin2hex('1')
    '1'
    """
    return hex(int(bin_string, base=2))[2:]


def fillupbyte(bin_string):
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
    target_length = len(bin_string) + (8 - len(bin_string) % 8) % 8
    return bin_string.rjust(target_length, '0')


def int2base64(value):
    """
    >>> int2base64(0x61)
    'YQ=='
    >>> int2base64(0x78)
    'eA=='
    """
    bin_string = bin(value)[2:]
    bin_string = fillupbyte(bin_string)
    