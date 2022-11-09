from random import randbytes

from Crypto.Cipher import DES


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


IP = [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]

E = [32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9, 8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17, 16, 17, 18, 19, 20, 21, 20, 21,
     22, 23, 24, 25, 24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1]

S = \
    [
        [
            [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
            [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
            [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
            [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
        ],
        [
            [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
            [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
            [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
            [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
        ],
        [
            [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
            [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
            [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
            [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
        ],
        [
            [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
            [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
            [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
            [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
        ],
        [
            [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
            [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
            [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
            [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
        ],
        [
            [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
            [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
            [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
            [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
        ],
        [
            [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
            [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
            [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
            [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
        ],
        [
            [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
            [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
            [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
            [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
        ]
    ]

P = [
    16, 7, 20, 21, 29, 12, 28, 17,
    1, 15, 23, 26, 5, 18, 31, 10,
    2, 8, 24, 14, 32, 27, 3, 9,
    19, 13, 30, 6, 22, 11, 4, 25]


def f(prev_r, key_n):
    """
    >>> f('11110000101010101111000010101010','000110110000001011101111111111000111000001110010')
    '00100011010010101010100110111011'
    """
    # L1 = R0
    e_res_from_prev_r = bit_permutation(prev_r, E)
    xored = bin_xor(key_n, e_res_from_prev_r)
    s_boxes = [xored[i:i + 6] for i in range(0, len(xored), 6)]
    s_boxes_res = ""
    for i in range(8):
        i_ind = int(s_boxes[i][0] + s_boxes[i][-1], 2)
        j_ind = int(s_boxes[i][1:-1], 2)
        s_boxes_res += str(bin(S[i][i_ind][j_ind]))[2:].rjust(4, '0')  # from zero
    return bit_permutation(s_boxes_res, P)


IP_inverse = [40, 8, 48, 16, 56, 24, 64, 32,
              39, 7, 47, 15, 55, 23, 63, 31,
              38, 6, 46, 14, 54, 22, 62, 30,
              37, 5, 45, 13, 53, 21, 61, 29,
              36, 4, 44, 12, 52, 20, 60, 28,
              35, 3, 43, 11, 51, 19, 59, 27,
              34, 2, 42, 10, 50, 18, 58, 26,
              33, 1, 41, 9, 49, 17, 57, 25]


def encrypt_DES(key, message):
    """
    >>> encrypt_DES(b'\\x13\\x34\\x57\\x79\\x9b\\xbc\\xdf\\xf1',b'\\x01\\x23\\x45\\x67\\x89\\xab\\xcd\\xef')
    b'\\x85\\xe8\\x13T\\x0f\\n\\xb4\\x05'
    """
    message = bytes2binary(message)
    key = bytes2binary(key)
    sub_keys = create_DES_subkeys(key)
    ip_message = bit_permutation(message, IP)
    l_zero_and_r_zero = [ip_message[i:i + int(len(ip_message) / 2)] for i in
                         range(0, len(ip_message), int(len(ip_message) / 2))]
    l_zero = l_zero_and_r_zero[0]
    r_zero = l_zero_and_r_zero[1]
    l_arr = []
    r_arr = []
    l_arr.append(l_zero)
    r_arr.append(r_zero)
    for i in range(1, 17):
        l_arr.append(r_arr[i - 1])
        r_arr.append(bin_xor(l_arr[i - 1], f(r_arr[i - 1], sub_keys[i - 1])))
    ip_reverse_res = bit_permutation(r_arr[-1] + l_arr[-1], IP_inverse)
    return binary2bytes(ip_reverse_res)


def are_random_tests_all_passes(number_of_tests):
    """
    >>> are_random_tests_all_passes(100)
    True
    """
    success_tests = 0
    for i in range(number_of_tests):
        random_key = randbytes(8)
        random_message = randbytes(8)
        cipher = DES.new(random_key, DES.MODE_ECB)
        cipher_message = cipher.encrypt(random_message)

        from_my = encrypt_DES(random_key, random_message)

        success_tests += int(cipher_message == from_my)

    return success_tests == number_of_tests
