'''
Coin Game: Consider a row of n coins of values v1 ... vn, where n is even.
We play a game against an opponent by alternating turns.
In each turn, a player selects either the first or last coin from the row,
removes it from the row permanently, and receives the value of the coin.
Determine the maximum possible amount of money we can definitely win if we move first.
Similar To: Coin-Row Problem

Recurrence:
F(i, j)=Max(Vi + Min(F(i+2, j), F(i+1, j-1)), (Vj + Min(F(i+1, j-1), F(i, j-2))))
Where
F(i, j)=Vi for == i
F(i, j)=Max(Vi, Vj) for j == i+1
and Vi, Vj are the values at i and j


Longest Increasing Subsequence: Given a sequence of n integers A1 ... An,
determine a subsequence (not necessarily contiguous) of maximum length in which the
values in the subsequence form a strictly increasing sequence.
g.  in the following sequence of 16 integers: 0, 8, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15, 4
the longest increasing subsequence is 0, 2, 6, 9, 11, 15 which has length 6.
Similar To: Making Change Problem

Recurrence:

L(j)=length of longest increasing subsequence ending at position j.
L=Max{L(1),L(2),L(3),L(n)}
L(i+1)=1+Max(L(j)
'''
# Coin Game Implementation:


def playGame(array, n):
    table = [[None for _ in range(n)] for _ in range(n)]

    for gap in range(0, n):
        i = 0
        for j in range(gap, n):
            if i+2 <= j:
                x = table[i+2][j]
            else:
                x = 0
            if i+1 <= j-1:
                y = table[i+1][j-1]
            else:
                y = 0
            if i <= j-2:
                z = table[i][j-2]
            else:
                z = 0
            table[i][j] = max((array[i] + min(x, y)), (array[j] + min(y, z)))
            i += 1
    return table[0][n-1]

if __name__ == "__main__":
    array1 = [2, 8, 6, 15, 3, 7]
    n = len(array1)
    print("%d\n" % playGame(array1, n))

    array2 = [1, 2, 3, 4, 5, 6]
    n = len(array2)
    print("%d\n" % playGame(array2, n))

    array3 = [5, 10, 15, 20, 25]
    n = len(array3)
    print("%d\n" % playGame(array3, n))
