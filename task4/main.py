from operator import itemgetter


def hex2bin(hex_value):
    '''
    >>> hex2bin('f')
    '1111'
    >>> hex2bin('1')
    '1'
    '''
    return bin(int(hex_value, 16))[2:]


def string2hex(message):
    '''
    >>> string2hex('a')
    '61'
    >>> string2hex('hello')
    '68656c6c6f'
    >>> string2hex('world')
    '776f726c64'
    >>> string2hex('foo')
    '666f6f'
    '''
    ret = ""

    for c in message:
        ret += hex(ord(c))[2:].rjust(2, '0')

    return ret


def hex2string(hex_message):
    '''
    >>> hex2string('61')
    'a'
    >>> hex2string('776f726c64')
    'world'
    >>> hex2string('68656c6c6f')
    'hello'
    '''
    ret = ""
    for i in range(0, len(hex_message), 2):
        ret += chr(int(hex_message[i:i + 2], 16))

    return ret


def encrypt_by_add_mod(value, key):
    """
    >>> encrypt_by_add_mod('Hello', 123)
    'Ãàççê'
    >>> encrypt_by_add_mod(encrypt_by_add_mod('Hello', 123), 133)
    'Hello'
    >>> encrypt_by_add_mod(encrypt_by_add_mod('Cryptography', 10), 246)
    'Cryptography'
    """
    #  get hex
    hex1 = string2hex(value)

    encrypted = ""
    # for every byte
    for i in range(0, len(hex1), 2):
        byte_from_value = int(hex1[i:i + 2], 16)
        add_res = byte_from_value + key
        mod_res = add_res % 256
        encrypted += hex2string(hex(mod_res)[2:])

    return encrypted


def encrypt_xor_with_changing_key_by_prev_cipher(value, key, operation):
    """
    >>> encrypt_xor_with_changing_key_by_prev_cipher('Hello',123,'encrypt')
    '3V:V9'
    >>> encrypt_xor_with_changing_key_by_prev_cipher(encrypt_xor_with_changing_key_by_prev_cipher('Hello',123,'encrypt'),123,'decrypt')
    'Hello'
    >>> encrypt_xor_with_changing_key_by_prev_cipher(encrypt_xor_with_changing_key_by_prev_cipher('Cryptography',10,'encrypt'),10,'decrypt')
    'Cryptography'
    """
    if operation == 'encrypt':
        encrypted = ""
        # get first byte of input
        xor_res = ord(value[0]) ^ key  # first byte cipher (key for second)
        encrypted += chr(xor_res)

        new_key = xor_res
        for i in range(1, len(value)):
            encr_byte_xor = ord(value[i]) ^ new_key
            encrypted += chr(encr_byte_xor)
            new_key = encr_byte_xor

        return encrypted

    elif operation == 'decrypt':
        decrypted = ""
        # value is encrypted value
        xor_res = ord(value[0]) ^ key  # first byte in first iteration
        decrypted += chr(xor_res)

        # new_key = xor_res  # m1
        for i in range(0, len(value) - 1):
            decr_byte_xor = ord(value[i]) ^ ord(value[i + 1])  # c1 ^ c2 etc
            decrypted += chr(decr_byte_xor)

        return decrypted


def encrypt_xor_with_changing_key_by_prev_cipher_longer_key(value, key_list, operation):
    """
    >>> key_list = [0x20, 0x44, 0x54,0x20]
    >>> encrypt_xor_with_changing_key_by_prev_cipher_longer_key(
    ...    encrypt_xor_with_changing_key_by_prev_cipher_longer_key('Hellobello, it will work for a long message as well',key_list,'encrypt'),
    ...        key_list,'decrypt')
    'Hellobello, it will work for a long message as well'
    """
    if operation == 'encrypt':
        encrypted = ""
        # create chunks (chunks amount equal to key_list length)
        chunks = [""] * len(key_list)
        value = [value[i:i + len(chunks)] for i in range(0, len(value), len(chunks))]

        for j in range(len(value)):
            for i in range(len(chunks)):
                if len(value[j]) == i:
                    break
                chunks[i] += value[j][i]

        # 1, 5, 9...  key_list[0]
        # 2, 6, 10... key_list[1]
        # 3, 7, 11... key_list[2]
        # 4, 8, 12... key_list[3]
        encrypted_chunks = []
        for i in range(len(key_list)):
            encrypted_chunks.append(encrypt_xor_with_changing_key_by_prev_cipher(chunks[i], key_list[i], operation))

        # from encrypted chunks to res
        for i in range(len(encrypted_chunks)):
            if i >= len(encrypted_chunks[i]):
                break
            else:
                if len(encrypted_chunks[-1]) < i + 1:
                    res = [x[i] for x in encrypted_chunks[0:-1]]
                else:
                    res = [x[i] for x in encrypted_chunks]
            encrypted += ''.join(res)
        return encrypted

    elif operation == 'decrypt':
        decrypted = ""
        # create chunks
        chunks = [""] * len(key_list)
        value = [value[i:i + len(chunks)] for i in range(0, len(value), len(chunks))]

        for j in range(len(value)):
            for i in range(len(chunks)):
                if len(value[j]) == i:
                    break
                chunks[i] += value[j][i]

        decrypted_chunks = []
        for i in range(len(key_list)):
            decrypted_chunks.append(encrypt_xor_with_changing_key_by_prev_cipher(chunks[i], key_list[i], operation))

        # from encrypted chunks to res
        for i in range(len(decrypted_chunks)):
            if i >= len(decrypted_chunks[i]):
                break
            else:
                if len(decrypted_chunks[-1]) < i + 1:
                    res = [x[i] for x in decrypted_chunks[0:-1]]
                else:
                    res = [x[i] for x in decrypted_chunks]
            decrypted += ''.join(res)
        return decrypted
