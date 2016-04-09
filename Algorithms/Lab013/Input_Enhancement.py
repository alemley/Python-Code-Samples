from random import randint
import timeit

alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
         'w', 'x', 'y', 'z', ' ']
bit = ['0', '1']


def generateShiftTable(pattern, alphabet):
    shift_table = []
    m = len(pattern)
    n = len(alphabet)

    for i in range(0, n):
        p = 0
        shift_table.append(p)
    for i in range(0, n):
        shift_table[i] = m
    for j in range(0, (m - 1)):
        for q in range(0, n):
            if pattern[j] == alphabet[q]:
                shift_table[q] = m-1-j

    return shift_table


def horspool(needle, haystack):
    pattern = needle

    if pattern[0] != '1' and pattern[0] != '0':
        loc_alphabet = alpha
    else:
        loc_alphabet = bit
    table = generateShiftTable(pattern, loc_alphabet)

    m = len(pattern)
    n = len(haystack)

    i = m-1
    while i <= (n-1):
        k = 0
        while (k <= (m-1)) and (pattern[m-1-k] == haystack[i-k]):
            k += 1
        if k == m:
            return i-m+1
        else:
            for z in range(0, len(table)):
                if str(loc_alphabet[z]) == str(haystack[i]):
                    i += table[z]
    return -1


def bruteForceStringMatch(pattern, haystack):
    n = len(haystack)
    m = len(pattern)
    for i in range(n-m+1):
        j = 0
        while j<m and(pattern[j] == haystack[i+j]):
            j+=1
        if j==m:
            return 1
    return -1


if __name__ == "__main__":
    pattern1 = ['b', 'a', 'o', 'b', 'a', 'b']
    pattern2 = ['0', '0', '1', '0', '1', '1', '1', '0']
    temp1 = 'bess knew about baobabs'
    temp2 = '0100111001011101011'
    haystack1 = []
    haystack2 = []
    for r in temp1:
        haystack1.append(r)
    for s in temp2:
        haystack2.append(s)

    print('\nPattern: ', pattern1)
    print('Haystack:', haystack1)
    print('Shift Table:')
    print('[', end='')
    for x in range(0, (len(alpha))):
        if x == (len(alpha)-1):
            print('_', end='')
        else:
            print('%c, ' % alpha[x],  end='')
    print(']')
    print(generateShiftTable(pattern1, alpha))
    print('Pattern found starting at position', horspool(pattern1, haystack1))

    print('\nPattern: ', pattern2)
    print('Haystack:', haystack2)
    print('Shift Table:')
    print('[', end='')
    for x in range(0, (len(bit))):
        if x == (len(bit)-1):
            print(bit[x], end='')
        else:
            print('%c, ' % bit[x],  end='')
    print(']')
    print(generateShiftTable(pattern2, bit))
    print('Pattern found starting at position', horspool(pattern2, haystack2))


    print("\n\nEfficiency Testing:")
    test_needle = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
    bitstring = []
    for t in range(0, 1000000):
        b = randint(0, 1)
        bitstring.append(b)

    start = timeit.default_timer()
    bruteForceStringMatch(test_needle, bitstring)
    stop = timeit.default_timer()
    print('Brute-force runtime:', stop-start)

    start = timeit.default_timer()
    horspool(test_needle, bitstring)
    stop = timeit.default_timer()
    print('My runtime:', stop-start)






# note, I won't have the desired time efficiency since I have an extra comparison step
# I should have made the shift table a dictionary, not an array, so I will lose efficiency
'''
Pattern:  ['a', 'd', 'v', 'a', 'n', 'c', 'e', 'd']
Haystack: ['w', 'e', 'l', 'c', 'o', 'm', 'e', ' ', 't', 'o', ' ', 'a', 'd', 'v', 'a', 'n', 'c', 'e', 'd', ' ', 'm', 'a', 't', 'h', 'e', 'm', 'a', 't', 'i', 'c', 's']
Shift Table:
[a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, _]
[4, 8, 2, 6, 1, 8, 8, 8, 8, 8, 8, 8, 8, 3, 8, 8, 8, 8, 8, 8, 8, 5, 8, 8, 8, 8, 8]
Pattern found starting at position 11

Pattern:  ['0', '0', '1', '0', '1', '1', '1', '0']
Haystack: ['0', '1', '0', '0', '1', '1', '1', '0', '0', '1', '0', '1', '1', '1', '0', '1', '0', '1', '1']
Shift Table:
[0, 1]
[4, 1]
Pattern found starting at position 7


Efficiency Testing:
Brute-force runtime: 0.2821793148621331
My runtime: 0.31852953210222057

Process finished with exit code 0
'''