from Crypto.Cipher import AES
from week6 import PKCS7_pad


def decrypt_aes_ecb(input_bytearray, key):
    """
    >>> key = bytes([57, 226, 240, 61, 125, 240, 75, 68, 22, 35, 124, 205, 144, 27, 118, 220])
    >>> decrypt_aes_ecb(bytes([215, 221, 59, 138, 96, 94, 155, 69, 52, 90, 212, 108, 49, 65, 138, 179]),key)
    b'lovecryptography'
    >>> decrypt_aes_ecb(bytes([147, 140, 44, 177, 97, 209, 42, 239, 152, 124, 241, 175, 202, 164, 183, 18]),key)
    b'!!really  love!!'
    """
    aes = AES.new(key, AES.MODE_ECB)
    message = aes.decrypt(input_bytearray)
    return message


def xor_byte_arrays(input1, input2):
    """
    >>> xor_byte_arrays(bytes([1,2,3,4]),bytes([2,3,4,5]))
    b'\\x03\\x01\\x07\\x01'
    >>> xor_byte_arrays(bytes([1,2,3,4]),bytes([]))
    b'\\x01\\x02\\x03\\x04'
    >>> xor_byte_arrays(bytes([1,2,3,4]),bytes([1,2]))
    b'\\x01\\x02\\x02\\x06'
    >>> xor_byte_arrays(bytes([1,2,4,8,16,32,64,128]),bytes([1,1,1,1,1,1,1,1]))
    b'\\x00\\x03\\x05\\t\\x11!A\\x81'
    """
    ret = b""
    max_len = max(len(input1), len(input2))
    input1_padded = input1.rjust(max_len, bytes([0]))
    input2_padded = input2.rjust(max_len, bytes([0]))

    for i in range(max_len):
        ret += bytes([input1_padded[i] ^ input2_padded[i]])

    return ret


def decrypt_aes_cbc_with_ecb(input_bytearray, key, iv):
    """
    >>> key = bytes([57, 226, 240, 61, 125, 240, 75, 68, 22, 35, 124, 205, 144, 27, 118, 220])
    >>> iv = bytes([241, 147, 66, 129, 194, 34, 37, 51, 236, 69, 188, 205, 64, 140, 244, 204])
    >>> decrypt_aes_cbc_with_ecb(bytes([255, 18, 67, 115, 172, 117, 242, 233, 246, 69, 81, 156, 52, 154, 123, 171]),key,iv)
    b'hello world 1234'
    >>> decrypt_aes_cbc_with_ecb(bytes([171, 218, 160, 96, 193, 134, 73, 81, 221, 149, 19, 180, 31, 247, 106, 64]),key,iv)
    b'lovecryptography'
    """
    message = b""
    aes = AES.new(key, AES.MODE_ECB)
    actual_running_key = iv
    for i in range(len(input_bytearray) // 16):
        actual_block = input_bytearray[16 * i:16 * (i + 1)]
        block_decrypted = aes.decrypt(actual_block)
        xored_block = xor_byte_arrays(actual_running_key, block_decrypted)
        message = message + xored_block

        actual_running_key = actual_block

    return message


def encrypt_aes_cbc_with_ecb(input_bytearray, key, iv):
    """
    >>> key = bytes([57, 226, 240, 61, 125, 240, 75, 68, 22, 35, 124, 205, 144, 27, 118, 220])
    >>> iv = bytes([241, 147, 66, 129, 194, 34, 37, 51, 236, 69, 188, 205, 64, 140, 244, 204])
    >>> encrypt_aes_cbc_with_ecb(b'hello world 1234',key,iv)
    b'\\xff\\x12Cs\\xacu\\xf2\\xe9\\xf6EQ\\x9c4\\x9a{\\xab'
    >>> encrypt_aes_cbc_with_ecb(bytes(b'lovecryptography'),key,iv)
    b'\\xab\\xda\\xa0`\\xc1\\x86IQ\\xdd\\x95\\x13\\xb4\\x1f\\xf7j@'
    """
    input_bytearray_padded = PKCS7_pad(input_bytearray, len(input_bytearray) + len(input_bytearray) % 16)
    cipher = b""
    aes = AES.new(key, AES.MODE_ECB)
    actual_running_key = iv
    for i in range(len(input_bytearray_padded) // 16):
        actual_block = input_bytearray_padded[16 * i:16 * (i + 1)]
        xored_block = xor_byte_arrays(actual_running_key, actual_block)

        block_encrypted = aes.encrypt(xored_block)
        cipher = cipher + block_encrypted

        actual_running_key = block_encrypted

    return cipher
