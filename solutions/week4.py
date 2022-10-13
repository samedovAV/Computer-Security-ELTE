def encrypt_by_add_mod(message, key):
    """
    >>> encrypt_by_add_mod('Hello',123)
    'Ãàççê'
    >>> encrypt_by_add_mod(encrypt_by_add_mod('Hello',123),133)
    'Hello'
    >>> encrypt_by_add_mod(encrypt_by_add_mod('Cryptography',10),246)
    'Cryptography'
    """
    res = ""
    for m in message:
        new_byte_value = (ord(m) + key) % 256
        res += chr(new_byte_value)

    return res


def encrypt_xor_with_changing_key_by_prev_cipher(message, key, mode):
    """
    >>> encrypt_xor_with_changing_key_by_prev_cipher('Hello',123,'encrypt')
    '3V:V9'
    >>> encrypt_xor_with_changing_key_by_prev_cipher(encrypt_xor_with_changing_key_by_prev_cipher('Hello',123,'encrypt'),123,'decrypt')
    'Hello'
    >>> encrypt_xor_with_changing_key_by_prev_cipher(encrypt_xor_with_changing_key_by_prev_cipher('Cryptography',10,'encrypt'),10,'decrypt')
    'Cryptography'
    """
    res = ""
    actual_key = key
    for m in message:
        new_byte_value = ord(m) ^ actual_key
        if mode == 'encrypt':
            actual_key = new_byte_value
        elif mode == 'decrypt':
            actual_key = ord(m)
        else:
            raise Exception(f'Unknown mode {mode}')
        res += chr(new_byte_value)

    return res


def encrypt_xor_with_changing_key_by_prev_cipher_longer_key(message, key_list, mode):
    """
    >>> key_list = [0x20, 0x44, 0x54,0x20]
    >>> encrypt_xor_with_changing_key_by_prev_cipher_longer_key('abcdefg', key_list, 'encrypt')
    'A&7D$@P'
    >>> encrypt_xor_with_changing_key_by_prev_cipher_longer_key('aaabbbb', key_list, 'encrypt')
    'A%5B#GW'
    >>> encrypt_xor_with_changing_key_by_prev_cipher_longer_key(
    ...    encrypt_xor_with_changing_key_by_prev_cipher_longer_key('abcdefg',key_list,'encrypt'),
    ...        key_list,'decrypt')
    'abcdefg'
    >>> encrypt_xor_with_changing_key_by_prev_cipher_longer_key(
    ...    encrypt_xor_with_changing_key_by_prev_cipher_longer_key('Hellobello, it will work for a long message as well',key_list,'encrypt'),
    ...        key_list,'decrypt')
    'Hellobello, it will work for a long message as well'
    """
    res = ""

    key_len = len(key_list)
    chunks = [message[i::key_len] for i in range(key_len)]
    chunks_ciphers = []
    for i in range(key_len):
        chunks_ciphers.append(encrypt_xor_with_changing_key_by_prev_cipher(chunks[i], key_list[i], mode))

    for i in range(len(message)):
        which_chunk = i % key_len
        character_num = i // key_len

        res += chunks_ciphers[which_chunk][character_num]

    return res