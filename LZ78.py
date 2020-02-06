# LZ78.py

def encode(string):
    print("encoding for",string)
    result = []
    d = {}
    token = ''
    i = 1
    last_token_index = 0
    for c in string:
        token += c
        if(token not in d):
            print(i,":",token)
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

def decode_pair(dict,pair):
    return dict[pair[0]] + pair[1]