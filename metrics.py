# metrics.py

import sys
sys.setrecursionlimit(10**6) 

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


def EditDistance(s1,s2):
	pass

def HammingDistance(s1,s2):
	pass

def SequenceAlignment(s1,s2):
	pass

def StringReconstruction(s1,s2):
	pass

