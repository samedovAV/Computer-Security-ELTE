def hex2string(value):
    """
    >>> hex2string('61')
    'a'
    >>> hex2string('776f726c64')
    'world'
    >>> hex2string('68656c6c6f')
    'hello'
    """
    return bytes.fromhex(value).decode('utf-8')


def string2hex(value):
    """
    >>> string2hex('a')
    '61'
    >>> string2hex('hello')
    '68656c6c6f'
    >>> string2hex('world')
    '776f726c64'
    >>> string2hex('foo')
    '666f6f'
    """
    return value.encode('utf-8').hex()


def hex_xor(first, second):
    """
    >>> hex_xor('0aabbf11','12345678')
    '189fe969'
    >>> hex_xor('12cc','12cc')
    '0000'
    >>> hex_xor('1234','2345')
    '3171'
    >>> hex_xor('111','248')
    '359'
    >>> hex_xor('8888888','1234567')
    '9abcdef'
    """
    # return ''.join(a ^ b for a, b in zip(first, second))
    return '{1:0{0}x}'.format(len(first), int(first, 16) ^ int(second, 16))


def encrypt_single_byte_xor(value, key):
    """
    >>> encrypt_single_byte_xor('aaabbccc','00')
    'aaabbccc'
    >>> encrypt_single_byte_xor(string2hex('hello'),'aa')
    '68757c7c7f'
    >>> hex2string(encrypt_single_byte_xor(encrypt_single_byte_xor(string2hex('hello'),'aa'),'aa'))
    'hello'
    >>> hex2string(encrypt_single_byte_xor(encrypt_single_byte_xor(string2hex('Encrypt and decrypt are the same'),'aa'),'aa'))
    'Encrypt and decrypt are the same'
    """
    key = "{0:08b}".format(int(key, 16))
    return hex_xor(value, key)


def is_valid(data: str) -> bool:
    result = 0
    for symbol in data:
        if symbol in {"~", '-', '#', '/', '\\', '%', '(', ')', '[', ']', '?', '$', '*', '+', '^', '<', '>', '=', '@',
                      '{', '}'}:
            result += 1
        if not ord(symbol) < 128:
            result += 1

    if data[-1] not in {'.', '!', '?'}:
        result += 1
    return True if result == 0 else False


def decrypt_single_byte_xor(value):
    """
    >>> decrypt_single_byte_xor('e9c88081f8ced481c9c0d7c481c7ced4cfc581ccc480')
    'Hi! You have found me!'
    >>> decrypt_single_byte_xor('b29e9f96839085849d9085989e9f82d1889e84d199908794d197989f95d1859994d181908282869e8395d0')
    'Congratulations you have find the password!'
    """
    alphabet = ["a", "b", "c", "d", "e", "f", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    keys_list = []
    for i in alphabet:
        for j in alphabet:
            keys_list.append(f"{i}{j}")

    true_results = []
    hex_results_list = {}
    for key in keys_list:

        raw_decrypted_hex = encrypt_single_byte_xor(value, key)
        hex_results_list.update({raw_decrypted_hex: key})

        try:
            tmp_text = hex2string(raw_decrypted_hex)
            if is_valid(tmp_text):
                true_results.append(tmp_text)
        except:
            continue

    print(len(hex_results_list))
    # with open("hex_results_list.json", "w") as f:
    #     json.dump(hex_results_list, f)
    return true_results[0]
