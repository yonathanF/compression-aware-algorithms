// metrics.c

int max(int a, int b) { return a > b ? a : b; }
int min(int a, int b) { return a < b ? a : b; }
int min3(int x, int y, int z) { return min(min(x, y), z); }

// https://www.geeksforgeeks.org/longest-common-subsequence-dp-4/
/* Returns length of LCS for X[0..m-1], Y[0..n-1] */
int lcs(char *X, char *Y, int m, int n) {
    int L[m + 1][n + 1];
    int i, j;

    /* Following steps build L[m+1][n+1] in bottom up fashion. Note
       that L[i][j] contains length of LCS of X[0..i-1] and Y[0..j-1] */
    for (i = 0; i <= m; i++) {
        for (j = 0; j <= n; j++) {
            if (i == 0 || j == 0)
                L[i][j] = 0;

            else if (X[i - 1] == Y[j - 1])
                L[i][j] = L[i - 1][j - 1] + 1;

            else
                L[i][j] = max(L[i - 1][j], L[i][j - 1]);
        }
    }

    /* L[m][n] contains length of LCS for X[0..n-1] and Y[0..m-1] */
    return L[m][n];
}

// https://www.geeksforgeeks.org/edit-distance-dp-5/
int edit_distance(char *str1, char *str2, int m, int n) {
    // Create a table to store results of subproblems
    int dp[m + 1][n + 1];

    // Fill d[][] in bottom up manner
    for (int i = 0; i <= m; i++) {
        for (int j = 0; j <= n; j++) {
            // If first string is empty, only option is to
            // insert all characters of second string
            if (i == 0)
                dp[i][j] = j; // Min. operations = j

            // If second string is empty, only option is to
            // remove all characters of second string
            else if (j == 0)
                dp[i][j] = i; // Min. operations = i

            // If last characters are same, ignore last char
            // and recur for remaining string
            else if (str1[i - 1] == str2[j - 1])
                dp[i][j] = dp[i - 1][j - 1];

            // If the last character is different, consider all
            // possibilities and find the minimum
            else
                dp[i][j] = 1 + min3(dp[i][j - 1],      // Insert
                                    dp[i - 1][j],      // Remove
                                    dp[i - 1][j - 1]); // Replace
        }
    }

    return dp[m][n];
}