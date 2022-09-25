def test_function(L):
    # for i in range(len(L) - 1):
    #   chars.append(chr(L[i]))

    chars = [chr(i) for i in L]
    joined = "".join(chars).lower()
    
    return joined[2:10] * 2
