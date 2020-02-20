# LZ78.py

def encode(string):
    # print("encoding for",string)
    result = []
    d = {}
    token = ''
    i = 1
    last_token_index = 0
    for c in string:
        token += c
        if(token not in d):
            # print(i,":",token)
            d[token] = i
            i += 1
            result.append((last_token_index,c))
            token = ''
            last_token_index = 0
        else:
            last_token_index = d[token]
    result.append((last_token_index,''))
    return result

def decode(pairs):
    result = ''
    d = {0:''}
    i = 1
    for pair in pairs:
        num = pair[0]
        char = pair[1]
        if(num == 0):
            d[i] = char
            result += char
        else:
            string = d[num] + char
            d[i] = string
            result += string
        i += 1
    return result

"""
def encodeNumbers(nums):
    # print("encoding for",string)
    result = []
    d = {}
    token = []
    i = 1
    last_token_index = 0
    for num in nums:
        token.append(num)
        if(tuple(token) not in d):
            # print(i,":",token)
            d[tuple(token)] = i
            i += 1
            result.append((last_token_index,num))
            token = []
            last_token_index = 0
        else:
            last_token_index = d[tuple(token)]
    result.append((last_token_index,0))
    return result

def decodeNumbers(pairs):
    result = []
    d = {0:0}
    i = 1
    for pair in pairs:
        index = pair[0]
        num = pair[1]
        if(index == 0):
            d[i] = [num]
            result += num
        else:
            string = d[index] + [num]
            d[i] = string
            result += string
        i += 1
    return result
"""