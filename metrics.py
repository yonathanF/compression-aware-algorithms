# metrics.py

# https://www.geeksforgeeks.org/longest-common-subsequence-dp-4/
def LCS(X , Y): 
    # find the length of the strings 
    m = len(X) 
    n = len(Y) 
  
    # declaring the array for storing the dp values 
    L = [[None]*(n+1) for i in range(m+1)] 
  
    """Following steps build L[m+1][n+1] in bottom up fashion 
    Note: L[i][j] contains length of LCS of X[0..i-1] 
    and Y[0..j-1]"""
    for i in range(m+1): 
        for j in range(n+1): 
            if i == 0 or j == 0 : 
                L[i][j] = 0
            elif X[i-1] == Y[j-1]: 
                L[i][j] = L[i-1][j-1]+1
            else: 
                L[i][j] = max(L[i-1][j] , L[i][j-1]) 
  
    # L[m][n] contains the length of LCS of X[0..n-1] & Y[0..m-1] 
    return L[m][n] 

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
    "Hamming Distance": HammingDistance,
    #"StringReconstruction": StringReconstruction,
    #"SequenceAlignment": SequenceAlignment,
    "Edit Distance": EditDistance,
    "LCS Length": LCS,
}
