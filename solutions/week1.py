import codecs

hex = "10000000000002ae"
b64 = codecs.encode(codecs.decode(hex, 'hex'), 'base64').decode()
print(b64)




import random

L = [random.randint(0x41,0x5a) for _ in range(20)]
print(L)
L2 = [chr(x) for x in L]
print(L2)
str = "".join(L2)
print(str)
str2 = str.lower()
print(str2)
str3 = str2[2:10] * 2
print(str3)