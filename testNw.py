import nwAlignClass as nw
import numpy as np
# strA = 'GCATGCU'
# strB = 'GATTACA'
# strA = 'GCAT'
# strB = 'GATT'

# strA, strB = 'CEELECANTH', 'PELICANDIANFJTH'

strA, strB = 'ATCCCGAAAGAAA', 'ATAAAA'
test = nw.nwMatrix(strA, strB,simiMatrix='atiam-fpa_dna.dist', \
                   gap_open=-30, gap_extend=0)

import nwalign as nw
aligned = nw.global_align(strA, strB, matrix='atiam-fpa_alpha.dist')
score = nw.score_alignment('CEELECANTH', '-PELICAN--', gap_open=-5, gap_extend=-2, matrix='atiam-fpa_alpha.dist')
# print('Results for basic gap costs (linear)')
# print(aligned[0])
# print(aligned[1])
aligned = nw.global_align(strA, strB, matrix='atiam-fpa_alpha.dist', \
                            gap_open=-30, gap_extend=0)
score = nw.score_alignment('CEELECANTH', '-PELICAN--', gap_open=-5, gap_extend=-2, matrix='atiam-fpa_alpha.dist')
print('Results for affine gap costs')
print(aligned[0])
print(aligned[1])


print test.scores
