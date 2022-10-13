from week2 import hex2bin, bin2hex


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


# ref: Week 3 - solutions
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


# for i in range(16):
#    print(bin(i)[2:].rjust(4,'0'),hex(i)[2:])

# ref: https://canvas.elte.hu/courses/21877/pages/week-3-solutions
def hex_xor(hex1, hex2):
    '''
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
    '''

    # if len(hex1) != len(hex2):
    #    raise Exception("The two arguments has to be the same! Received: '"+str(hex1)+"' and '"+str(hex2)+"'")

    # Find the bigger length of the two hex
    target_len = max(len(hex1), len(hex2))

    # Pad both of the input to have the same number of zeroes in binary format
    # rjust because: 123 = 0123, but 123 not equal 1230 in decimal case as well
    bin1 = hex2bin(hex1).rjust(target_len * 4, '0')
    bin2 = hex2bin(hex2).rjust(target_len * 4, '0')

    bin3 = ""
    for i in range(len(bin1)):
        if bin1[i] == bin2[i]:
            bin3 += "0"
        else:
            bin3 += "1"

    return bin2hex(bin3).rjust(target_len, '0')


def create_repeated_key(key, target_len):
    '''
    >>> create_repeated_key('aa',4)
    'aaaa'
    >>> create_repeated_key('ab',4)
    'abab'
    >>> create_repeated_key('ab',8)
    'abababab'
    '''
    ret = ""

    inner_counter = 0
    for i in range(target_len):
        ret += key[inner_counter]
        inner_counter = (inner_counter + 1) % len(key)

    return ret


def encrypt_single_byte_xor(input_message, key):
    '''
    >>> encrypt_single_byte_xor('aaabbccc','00')
    'aaabbccc'
    >>> encrypt_single_byte_xor(string2hex('hello'),'aa')
    'c2cfc6c6c5'
    >>> hex2string(encrypt_single_byte_xor(encrypt_single_byte_xor(string2hex('hello'),'aa'),'aa'))
    'hello'
    >>> hex2string(encrypt_single_byte_xor(encrypt_single_byte_xor(string2hex('Encrypt and decrypt are the same'),'aa'),'aa'))
    'Encrypt and decrypt are the same'
    >>> encrypt_single_byte_xor(string2hex('Hi! You have found me!'),'a1')
    'e9c88081f8ced481c9c0d7c481c7ced4cfc581ccc480'
    >>> encrypt_single_byte_xor(string2hex('Congratulations you have find the password!'),'f1')
    'b29e9f96839085849d9085989e9f82d1889e84d199908794d197989f95d1859994d181908282869e8395d0'
    >>> encrypt_single_byte_xor(string2hex('Who knows what is happening? Where am I?'),'b6')
    'e1ded996ddd8d9c1c596c1ded7c296dfc596ded7c6c6d3d8dfd8d18996e1ded3c4d396d7db96ff89'
    '''
    long_key = create_repeated_key(key, len(input_message))
    return hex_xor(input_message, long_key)


# for key in range(256):
#    hex_key = hex(key)[2:]
#    decrypted_message = hex2string(encrypt_single_byte_xor('e9c88081f8ced481c9c0d7c481c7ced4cfc581ccc480',hex_key))
#    print(hex_key, decrypted_message)

valid_characters = "abcdefghijklmnopqrstuvxyz'- \"ABCDEFGHIJKLMNOPQRSTUVXYZ"


def count_simple_text_chars(string):
    count = 0
    for c in string:
        if c in valid_characters:
            count += 1

    return count


def decrypt_single_byte_xor(cipher):
    '''
    >>> decrypt_single_byte_xor('e9c88081f8ced481c9c0d7c481c7ced4cfc581ccc480')
    'Hi! You have found me!'
    >>> decrypt_single_byte_xor('b29e9f96839085849d9085989e9f82d1889e84d199908794d197989f95d1859994d181908282869e8395d0')
    'Congratulations you have find the password!'
    >>> decrypt_single_byte_xor('e1ded996ddd8d9c1c596c1ded7c296dfc596ded7c6c6d3d8dfd8d18996e1ded3c4d396d7db96ff89')
    'Who knows what is happening? Where am I?'
    '''

    # Run a maximum search on the results
    best = None
    best_count = None
    for key in range(256):
        hex_key = hex(key)[2:].zfill(2)
        decrypted_message = hex2string(encrypt_single_byte_xor(cipher, hex_key))
        # print(decrypted_message) We count how many normal characters can be found in a message Results that
        # decrypted message that has the most normal character You can use more sophisticated function to determine
        # is a text normal text or not like character distribution for example.
        actual_count = count_simple_text_chars(decrypted_message)
        if best == None or best_count < actual_count:
            best = decrypted_message
            best_count = actual_count

    return best
