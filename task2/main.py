base64_dict = {"000000": "A", "010000": "Q", "100000": "g", "110000": "w",
               "000001": "B", "010001": "R", "100001": "h", "110001": "x",
               "000010": "C", "010010": "S", "100010": "i", "110010": "y",
               "000011": "D", "010011": "T", "100011": "j", "110011": "z",
               "000100": "E", "010100": "U", "100100": "k", "110100": "0",
               "000101": "F", "010101": "V", "100101": "l", "110101": "1",
               "000110": "G", "010110": "W", "100110": "m", "110110": "2",
               "000111": "H", "010111": "X", "100111": "n", "110111": "3",
               "001000": "I", "011000": "Y", "101000": "o", "111000": "4",
               "001001": "J", "011001": "Z", "101001": "p", "111001": "5",
               "001010": "K", "011010": "a", "101010": "q", "111010": "6",
               "001011": "L", "011011": "b", "101011": "r", "111011": "7",
               "001100": "M", "011100": "c", "101100": "s", "111100": "8",
               "001101": "N", "011101": "d", "101101": "t", "111101": "9",
               "001110": "O", "011110": "e", "101110": "u", "111110": "+",
               "001111": "P", "011111": "f", "101111": "v", "111111": "/"}


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
    to_bin = hex2bin(str(hex(value)[2:]))
    to_bin = fillupbyte(to_bin)
    if len(to_bin) % 6 != 0:
        sextets_count = int(len(to_bin) / 6) + 1
        zeros_needed = sextets_count * 6 - len(to_bin)
        for i in range(zeros_needed):
            to_bin = to_bin + '0'

    parts = [to_bin[i:i+6] for i in range(0, len(to_bin), 6)]
    res = ""
    for i in parts:
        res += base64_dict.get(i)

    if len(res) % 4 != 0:
        pads_needed = (int(len(res) / 4) + 1) * 4 - len(res)
        for i in range(pads_needed):
            res = res + '='

    return res


def hex2base64(value):
    """
    >>> hex2base64('61')
    'YQ=='
    >>> hex2base64('123456789abcde')
    'EjRWeJq83g=='
    >>> hex2base64('7368726f6f6d')
    'c2hyb29t'
    """
    return int2base64(int(value, 16))
