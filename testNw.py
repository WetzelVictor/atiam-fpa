import nwAlignClass as nw
import numpy as np

# strA = 'GCATGCU'
# strB = 'GATTACA'
# strA = 'GCAT'
# strB = 'GATT'

strA, strB = 'CEELECANTH', 'PELICAN'

test = nw.nwMatrix(strA, strB)

dist = open('atiam-fpa_alpha.dist','w')
print dist
print dist[0]
