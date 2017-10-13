import nwAlignClass as nw
import numpy as np

strA = 'GCATGCU'
strB = 'GATTACA'
# strA = 'GCAT'
# strB = 'GATT'

test = nw.nwMatrix(strA, strB)

print test.matchMatrix
test.printMatrix()

print test.a

