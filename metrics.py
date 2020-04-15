# metrics.py

import sys
sys.setrecursionlimit(10**6)

LCS_results = {}  # please copy this line with the function


def LCS(s1, s2):
    if(s1 == "" or s2 == ""):
        return ""
    if(s1 in LCS_results and s2 in LCS_results[s1]):
        return LCS_results[s1][s2]
    result = ""
    if(s1[-1] == s2[-1]):
        result = LCS(s1[:-1], s2[:-1]) + s1[-1]
    else:
        reduce_s1_result = LCS(s1[:-1], s2)
        reduce_s2_result = LCS(s1, s2[:-1])
        if(len(reduce_s1_result) > len(reduce_s2_result)):
            result = reduce_s1_result
        else:
            result = reduce_s2_result
    if s1 not in LCS_results:
        LCS_results[s1] = {}
    LCS_results[s1][s2] = result
    # print("LCS(",s1,",",s2,") :",result)
    return result


def matrix_pretty_print(matrix):
    """Prints the matrix more nicely """
    for row in matrix:
        print(row)


def EditDistance(s1, s2):
    matrix = [[0 for _ in range(len(s2))] for _ in range(len(s1))]

    for i in range(1, len(s1)):
        matrix[i][0] = i

    for j in range(1, len(s2)):
        matrix[0][j] = j

    for j in range(1, len(s2)):
        for i in range(1, len(s1)):
            if s1[i] == s2[j]:
                sub_cost = 0
            else:
                sub_cost = 1

            matrix[i][j] = min(matrix[i - 1][j] + 1,
                               matrix[i][j - 1] + 1,
                               matrix[i - 1][j - 1] + sub_cost)

    return matrix[len(s1) - 1][len(s2) - 1]


def HammingDistance(s1, s2):
    if len(s1) != len(s2):
        return -1
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))

# the Needleman-Wunsch algorithm for Sequence Alignment


def SequenceAlignment(s1, s2):
    pass


def StringReconstruction(s1, s2):
    pass

metrics = {
    "HammingDistance": HammingDistance,
    "StringReconstruction": StringReconstruction,
    "SequenceAlignment": SequenceAlignment,
    "EditDistance": EditDistance,
    "LCS": LCS,
}
