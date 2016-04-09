from random import randint
import timeit


def lomuto_partition(A, l, r):
    pivot = l
    for i in range(l, r):
        if A[i] <= A[r]:
            A[i], A[pivot] = A[pivot], A[i]
            pivot += 1
    A[r], A[pivot] = A[pivot], A[r]
    return pivot


def lomuto_quicksort(A):
    l_quicksort(A, 0, (len(A) - 1))


def l_quicksort(A, l, r):
    if r - l < 1:
        return
    else:
        n = lomuto_partition(A, l, r)
        l_quicksort(A, l, n - 1)
        l_quicksort(A, n + 1, r)


def selection_sort(A):
    for front in range(0, len(A) - 1):
        minimum = front
        for j in range((front + 1), len(A)):
            if A[j] < A[minimum]:
                minimum = j
        A[front], A[minimum] = A[minimum], A[front]

if __name__ == '__main__':
    list1 = []
    list2 = []

    for i in range(0, 10000):
        list1.append((randint(0, 100000)))

    list2 = list1

    control = sorted(list1)
    start = timeit.default_timer()
    lomuto_quicksort(list1)
    stop = timeit.default_timer()
    if list1 == control:
        print('List1 sorted properly by Quicksort with Lomuto Partitioning.')
        print('Operation time:', stop - start)
    start = timeit.default_timer()
    selection_sort(list2)
    stop = timeit.default_timer()
    if list2 == control:
        print('List2 sorted properly by Brute-force Selection Sort.')
        print('Operation time:', stop - start)



'''
Lomuto.py
List1 sorted properly by Quicksort with Lomuto Partitioning.
Operation time: 0.049809701802397785
List2 sorted properly by Brute-force Selection Sort.
Operation time: 8.182898541529235

Process finished with exit code 0
'''

'''
In this instance, using quicksort is 165 times faster than brute force.
This is why it is important to have efficient algorithms!
'''