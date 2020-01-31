# LZ78.py

import sys
sys.setrecursionlimit(10**6) 

def LZ78_encode(string):
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

def LZ78_decode(pairs):
    result = ''
    partial_results = []
    d = {0:''}
    i = 1
    for pair in pairs:
        num = pair[0]
        char = pair[1]
        if(num == 0):
            d[i] = char
            result += char
            partial_results.append(result)
        else:
            string = d[num] + char
            d[i] = string
            result += string
            partial_results.append(result)
        i += 1
    partial_results.append(result)
    return result, partial_results

def LCS_Contiguous(s1, s2):
   m = [[0] * (1 + len(s2)) for i in range(1 + len(s1))]
   longest, x_longest = 0, 0
   for x in range(1, 1 + len(s1)):
       for y in range(1, 1 + len(s2)):
           if s1[x - 1] == s2[y - 1]:
               m[x][y] = m[x - 1][y - 1] + 1
               if m[x][y] > longest:
                   longest = m[x][y]
                   x_longest = x
           else:
               m[x][y] = 0
   return s1[x_longest - longest: x_longest]

LCS_results = {}

def LCS(s1,s2):
    if(s1 == "" or s2 == ""):
        return ""
    if(s1 in LCS_results and s2 in LCS_results[s1]):
        return LCS_results[s1][s2]
    result = ""
    if(s1[-1] == s2[-1]):
        result = LCS(s1[:-1],s2[:-1]) + s1[-1]
    else:
        reduce_s1_result = LCS(s1[:-1],s2)
        reduce_s2_result = LCS(s1,s2[:-1])
        if(len(reduce_s1_result) > len(reduce_s2_result)):
            result = reduce_s1_result
        else:
            result = reduce_s2_result
    if s1 not in LCS_results:
        LCS_results[s1] = {}
    LCS_results[s1][s2] = result
    # print("LCS(",s1,",",s2,") :",result)
    return result
    
# def LCS_compressed(a,b):

def LZ78_decode_pair(dict,pair):
    return dict[pair[0]] + pair[1]

def formatPair(pair):
    return "("+str(pair[0])+", '"+str(pair[1])+"')"

def SubproblemLCSBruteForce(a,b):
    rows = []
    cols = []
    vals = []
    a_str,a_partial_results = LZ78_decode(a)
    b_str,b_partial_results = LZ78_decode(b)
    # for i in range(len(b)):
    #     cols.append(b_partial_results[i])
    # for i in range(len(a)):
    #     rows.append(a_partial_results[i])
    for p2 in b:
        cols.append(formatPair(p2))
    for p1 in a:
        rows.append(formatPair(p1))
    for i in range(len(a_partial_results)):
        s1 = a_partial_results[i]
        this_row = []
        for j in range(len(b_partial_results)):
            s2 = b_partial_results[j]
            # print("new pair")
            this_row.append(LCS(s1,s2))
        vals.append(this_row)
    return rows,cols,vals

def PairwiseLCSBruteForce(a,b):
    rows = []
    cols = []
    vals = []
    a_str,a_partial_results = LZ78_decode(a)
    b_str,b_partial_results = LZ78_decode(b)
    # for i in range(len(b)):
    #     cols.append(b_partial_results[i])
    # for i in range(len(a)):
    #     rows.append(a_partial_results[i])
    for p2 in b:
        cols.append(formatPair(p2))
    for p1 in a:
        rows.append(formatPair(p1))
    for i in range(len(a_partial_results)):
        s1 = a_partial_results[i]
        this_row = []
        for j in range(len(b_partial_results)):
            s2 = b_partial_results[j]
            # print("new pair")
            this_row.append(LCS(s1,s2))
        vals.append(this_row)
    return rows,cols,vals

def formatWithSpace(string,num_spaces):
    num_spaces_to_print = max(0,num_spaces-len(string)) + 2
    return " " * num_spaces_to_print + string

def formatTable(rows,cols,vals):
    if(len(vals) < len(rows)):
        return "dimension mismatch - rows"
    if(len(vals[0]) < len(cols)):
        return "dimension mismatch - cols"
    row_colwidth = len(rows[0])
    for row in rows:
        if(len(row) > row_colwidth):
            row_colwidth = len(row)
    colwidths = []
    col_index = 0
    for col in cols:
        max_length = len(col)
        for i in range(len(rows)):
            if(len(vals[i][col_index]) > max_length):
                max_length = len(vals[i][col_index])
        colwidths.append(max_length)
        col_index += 1
    output = formatWithSpace('',row_colwidth)
    for i in range(len(cols)):
        output += formatWithSpace(cols[i],colwidths[i])
    output += "\n"
    for i in range(len(rows)):
        output += formatWithSpace(rows[i],row_colwidth)
        for j in range(len(cols)):
            output += formatWithSpace(vals[i][j],colwidths[j])
        output += "\n"
    return output

if not (len(sys.argv) == 3 or len(sys.argv) == 4):
    print("usage:")
    print("python LZ78.py <str1> <str2>")
    print("or")
    print("python LZ78.py -f <filename1> <filename2>")
    quit()
s1 = ""
s2 = ""
if(len(sys.argv) == 4 and sys.argv[1] == "-f"):
    s1 = open(sys.argv[2],'r').read().replace('\n','')
    s2 = open(sys.argv[3],'r').read().replace('\n','')
else:
    s1 = sys.argv[1].replace('\n','')
    s2 = sys.argv[2].replace('\n','')
print(LCS(s1,s2))
p1 = LZ78_encode(s1)
p2 = LZ78_encode(s2)
rows,cols,bruteforce = SubproblemLCSBruteForce(p1,p2)
print(formatTable(rows,cols,bruteforce))
rows,cols,bruteforce = PairwiseLCSBruteForce(p1,p2)
print(formatTable(rows,cols,bruteforce))


