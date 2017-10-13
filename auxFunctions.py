""" """
"""  FUNCTION ========================
quicksort: DECREASING partition based sorting algorithm, recursive
    INPUT: 
        - A: Array to sort
        -lo: Ordering from 'lo' index in the array...
        -hi: ... up to the the 'hi' index. 
            => To sort the whole array: 'lo = 0' 'hi = len(A)-1'

Lomuto quicksort algorithm, pseudo code on wikipedia, implemented in python
https://en.wikipedia.org/wiki/Quicksort
"""

def quicksort(A, lo, hi):
    if lo < hi:
        p = partition(A, lo, hi)
        quicksort(A, lo, p-1)
        quicksort(A, p+1, hi)

def partition(A, lo, hi):
    pivot = A[hi] # leftmost element: avoids worst case

    i = lo - 1
    for j in xrange(lo, hi):
        if A[j] < pivot:
            i = i  + 1
            A[i], A[j] = A[j], A[i]

    if A[hi] < A[i+1]:
            A[i+1], A[hi] = A[hi], A[i+1]

    return i + 1

## EXAMPLE:
# import random as r
# myArray = [int(10*r.random()) for i in xrange(50)]
# print myArray
# quicksort(myArray, 0, len(myArray)-1)
# print myArray

#========== END =============

""" """
"""  FUNCTION ========================
quicksort: DECREASING partition based sorting algorithm, recursive
    INPUT: 
        - A: Array to sort
        -lo: Ordering from 'lo' index in the array...
        -hi: ... up to the the 'hi' index. 
            => To sort the whole array: 'lo = 0' 'hi = len(A)-1'

Lomuto quicksort algorithm, pseudo code on wikipedia, implemented in python
https://en.wikipedia.org/wiki/Quicksort
"""

def revQuicksort(A, lo, hi):
    if lo < hi:
        p = revPartition(A, lo, hi)
        revQuicksort(A, lo, p-1)
        revQuicksort(A, p+1, hi)

def revPartition(A, lo, hi):
    pivot = A[hi] # leftmost element: avoids worst case

    i = lo - 1
    for j in xrange(lo, hi):
        if A[j] > pivot:
            i = i  + 1
            A[i], A[j] = A[j], A[i]

    if A[hi] > A[i+1]:
            A[i+1], A[hi] = A[hi], A[i+1]

    return i + 1

## EXAMPLE:
# import random as r
# myArray = [int(10*r.random()) for i in xrange(50)]
# print myArray
# quicksort(myArray, 0, len(myArray)-1)
# print myArray

#========== END =============
