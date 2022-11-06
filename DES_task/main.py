def bytes2binary(value):
    """
    >>> bytes2binary(b'\\x01')
    '00000001'
    >>> bytes2binary(b'\\x03')
    '00000011'
    >>> bytes2binary(b'\\xf0')
    '11110000'
    >>> bytes2binary(b'\\xf0\\x80')
    '1111000010000000'
    """
    res = ''
    temp = bin(int.from_bytes(value, byteorder='big'))[2:]
    res += temp.rjust(8 * len(value), '0')
    return res


def binary2bytes(value):
    """
    >>> binary2bytes('00000001')
    b'\\x01'
    >>> binary2bytes('00000011')
    b'\\x03'
    >>> binary2bytes('11110000')
    b'\\xf0'
    >>> binary2bytes('1111000010000000')
    b'\\xf0\\x80'
    """
    # ref: https://stackoverflow.com/questions/32675679/convert-binary-string-to-bytearray-in-python-3
    return int(value, 2).to_bytes((len(value) + 7) // 8, byteorder='big')


def bin_xor(first, second):
    """
    >>> bin_xor('1011','0000')
    '1011'
    >>> bin_xor('1','0000')
    '0001'
    >>> bin_xor('1101','1011')
    '0110'
    >>> bin_xor('10101010','01010101')
    '11111111'
    """
    res = ''
    target_len = max(len(first), len(second))
    first = first.rjust(target_len, '0')
    second = second.rjust(target_len, '0')
    # res = [str(int(first[i]) ^ int(second[i])) for i in range(len(first))]
    for i in range(len(first)):
        res += str(int(first[i]) ^ int(second[i]))
    return res


key_plus_order = [57, 49, 41, 33, 25, 17, 9,
                  1, 58, 50, 42, 34, 26, 18,
                  10, 2, 59, 51, 43, 35, 27,
                  19, 11, 3, 60, 52, 44, 36,
                  63, 55, 47, 39, 31, 23, 15,
                  7, 62, 54, 46, 38, 30, 22,
                  14, 6, 61, 53, 45, 37, 29,
                  21, 13, 5, 28, 20, 12, 4]

# Key- Compression Table : Compression of key from 56 bits to 48 bits
key_comp = [14, 17, 11, 24, 1, 5,
            3, 28, 15, 6, 21, 10,
            23, 19, 12, 4, 26, 8,
            16, 7, 27, 20, 13, 2,
            41, 52, 31, 37, 47, 55,
            30, 40, 51, 45, 33, 48,
            44, 49, 39, 56, 34, 53,
            46, 42, 50, 36, 29, 32]


def bit_permutation(message, order_arr):
    res = ""
    for i in order_arr:
        res += message[i - 1]

    return res


def left_shift_rot(value, step=1):
    return value[step:] + value[:step]


def create_DES_subkeys(key):
    """
    >>> create_DES_subkeys('0001001100110100010101110111100110011011101111001101111111110001')
    ['000110110000001011101111111111000111000001110010', '011110011010111011011001110110111100100111100101', '010101011111110010001010010000101100111110011001', '011100101010110111010110110110110011010100011101', '011111001110110000000111111010110101001110101000', '011000111010010100111110010100000111101100101111', '111011001000010010110111111101100001100010111100', '111101111000101000111010110000010011101111111011', '111000001101101111101011111011011110011110000001', '101100011111001101000111101110100100011001001111', '001000010101111111010011110111101101001110000110', '011101010111000111110101100101000110011111101001', '100101111100010111010001111110101011101001000001', '010111110100001110110111111100101110011100111010', '101111111001000110001101001111010011111100001010', '110010110011110110001011000011100001011111110101']
    """
    k = key
    k_plus = bit_permutation(k, key_plus_order)
    c_zero_and_d_zero = [k_plus[i:i + int(len(k_plus) / 2)] for i in range(0, len(k_plus), int(len(k_plus) / 2))]
    c_zero = c_zero_and_d_zero[0]
    d_zero = c_zero_and_d_zero[1]
    c_arr = []
    d_arr = []
    c_arr.append(c_zero)
    d_arr.append(d_zero)

    for i in range(1, 17):
        if i == 1 or i == 2 or i == 9 or i == 16:
            c_arr.append(left_shift_rot(c_arr[i - 1], 1))
            d_arr.append(left_shift_rot(d_arr[i - 1], 1))
        else:
            c_arr.append(left_shift_rot(c_arr[i - 1], 2))
            d_arr.append(left_shift_rot(d_arr[i - 1], 2))

    k_arr = []
    for i in range(1, 17):
        k_arr.append(bit_permutation(c_arr[i] + d_arr[i], key_comp))

    return k_arr


def f():
    """
    >>> f('11110000101010101111000010101010','000110110000001011101111111111000111000001110010')
    '00100011010010101010100110111011'
    """
    return ""


def encrypt_DES(key, message):
    """
    >>> encrypt_DES(b'\\x13\\x34\\x57\\x79\\x9b\\xbc\\xdf\\xf1',b'\\x01\\x23\\x45\\x67\\x89\\xab\\xcd\\xef')
    b'\\x85\\xe8\\x13T\\x0f\\n\\xb4\\x05'
    """