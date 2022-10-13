# Task 1 (A)
def encrypt_with_power(message, key):
    """
    >>> encrypt_with_power('Hello',250)
    '²A|lo'
    >>> encrypt_with_power(encrypt_with_power('Hello',123),123)
    'Hello'
    >>> encrypt_with_power(encrypt_with_power('Cryptography',10),10)
    'Cryptography'
    """
    res = ""

    actual_key = key

    for m in message:
        new_byte_value = (ord(m) ^ actual_key) % 256
        actual_key = pow(actual_key, 2)
        res += chr(new_byte_value)

    return res


# Task 2 (A)
def encrypt_with_power2(message, key, mode):
    """
    >>> encrypt_with_power2('Hello',253,'encrypt')
    'µl=Í.'
    >>> encrypt_with_power2('Hello2',131,'encrypt')
    'Ël=Í.³'
    >>> encrypt_with_power2(encrypt_with_power2('Hello',123,'encrypt'),123,'decrypt')
    'Hello'
    >>> encrypt_with_power2(encrypt_with_power2('Cryptography',10,'encrypt'),10,'decrypt')
    'Cryptography'
    """
    res = ""

    actual_key = key
    for m in message:
        new_byte_value = ord(m) ^ actual_key
        actual_key = pow(actual_key, 2) % 256
        if mode == 'encrypt':
            if actual_key == 0 or actual_key == 1:
                actual_key = ord(m)
        elif mode == 'decrypt':
            if actual_key == 0 or actual_key == 1:
                actual_key = new_byte_value
        else:
            raise Exception(f'Unknown mode {mode}')
        res += chr(new_byte_value)

    return res


# Task 3 (A)
def swap_lower_and_upper_bits(value):
    """
    >>> swap_lower_and_upper_bits(0)
    0
    >>> swap_lower_and_upper_bits(1)
    16
    >>> swap_lower_and_upper_bits(2)
    32
    >>> swap_lower_and_upper_bits(8)
    128
    >>> bin(swap_lower_and_upper_bits(0b1111))
    '0b11110000'
    >>> bin(swap_lower_and_upper_bits(0b10011010))
    '0b10101001'
    """
    bin_value = bin(value)
    target_length = len(bin_value[2::]) + (8 - len(bin_value[2::]) % 8) % 8
    bin_value = bin_value[2:].zfill(target_length)
    new_value = bin_value[4:8] + bin_value[0:4]
    return int(new_value, 2)


# Task 4 (A)
def encrypt_with_power_and_swap(message, key, mode):
    """
    >>> encrypt_with_power_and_swap('Hello',11,'encrypt')
    '4ÁÕÐê'
    >>> encrypt_with_power_and_swap(encrypt_with_power_and_swap('Hello',123,'encrypt'),123,'decrypt')
    'Hello'
    >>> encrypt_with_power_and_swap(encrypt_with_power_and_swap('Cryptography',12,'encrypt'),12,'decrypt')
    'Cryptography'
    """
    res = ""

    actual_key = key
    for m in message:
        if mode == 'encrypt':
            new_byte = swap_lower_and_upper_bits(ord(m))
            new_byte_value = new_byte ^ actual_key
            actual_key = pow(actual_key, 2) % 256
            if actual_key == 0 or actual_key == 1:
                actual_key = new_byte
        elif mode == 'decrypt':
            new_byte = swap_lower_and_upper_bits(ord(m))
            new_byte_value = (new_byte ^ actual_key) % 256
            actual_key = pow(actual_key, 2) % 256
            if actual_key == 0 or actual_key == 1:
                actual_key = new_byte
        else:
            raise Exception(f'Unknown mode {mode}')
        res += chr(new_byte_value)

    return res
