from heapq import heapify
from heapq import heappop
from heapq import heappush
from random import randint
from math import floor
import timeit


def binary_search(_array, _target):
    l = 0
    r = len(_array) - 1
    acquired = False

    while l <= r and not acquired:
        mid = floor((l + r)/2)
        if _array[mid] == _target:
            acquired = True
        else:
            if _target < _array[mid]:
                r = mid - 1
            else:
                l = mid + 1
    return acquired


def linear_search(_array, _target):
    position = 0
    acquired = False
    while position < len(_array) and not acquired:
        if _array[position] == target:
            acquired = True
        position += 1
    return acquired

if __name__ == '__main__':
    array = []
    for i in range(0, 15):
        j = randint(0, 5000)
        array.append(j)

    print('###PART 1###')
    print('Randomly generated array:\n', array)
    heapify(array)

    sorted_array = []
    for m in range(0, 15):
        n = heappop(array)
        sorted_array.append(n)

    print('Heapq-pop sorted array\n', sorted_array)
    print('############')


    #############################################################################################
    ##############################PART 2#########################################################
    #############################################################################################
    x = 1
    done = False

    while not done:
        part_2_array_a = []
        for z in range(0, 1000):
            y = randint(0, 5000)
            part_2_array_a.append(z)

        start = timeit.default_timer()
        heapify(part_2_array_a)
        sorted_part_2_array_a = []
        for m in range(0, 1000):
            n = heappop(part_2_array_a)
            sorted_part_2_array_a.append(n)

        escape_a = False

        for q in range(0, x):
            while not escape_a:
                target = randint(0, 5000)
                escape_a = binary_search(sorted_part_2_array_a, target)
        stop = timeit.default_timer()

        binary_time = stop - start

        part_2_array_b = part_2_array_a

        escape_b = False

        start = timeit.default_timer()
        for q in range(0, x):
            while not escape_b:
                target = randint(0, 5000)
                escape_b = binary_search(sorted_part_2_array_a, target)
        stop = timeit.default_timer()

        linear_time = stop - start

        if binary_time < linear_time:
            print('It takes about %d calls before binary search is more efficient than linear search.' %x)
            done = True
        else:
            x += 1



#  After five runs, the average output given is 2100 processes. I think the takeaway from this assignment is that
#  presorting is great, but it is only worth using if the input is sufficiently large, and that sometimes a
#  simple linear search can do the trick.