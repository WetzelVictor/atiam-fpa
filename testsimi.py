import string
import numpy as np



# for m1 in string.ascii_uppercase:
#     dist.write(m1)
#     if (m1 < 'Z'):
#         dist.write('  ')
# dist.write('\n')
# for m1 in string.ascii_uppercase:
#     dist.write(m1 + '  ')
#     for m2 in string.ascii_uppercase:
#         if (m2 == m1):
#             dist.write('5  ')
#         else:
#             dist.write('-3  ')
#     dist.write('\n')
# dist.close()



dist = open('atiam-fpa_alpha.dist')
with dist as f:
        lineCount = sum(1 for _ in f)

dist = open('atiam-fpa_alpha.dist')


simiMatrix = [[] for i in xrange(lineCount)]

for i in xrange(lineCount):
    if i ==0:
        line = list(dist.readline())
    else:
        line= list(dist.readline((i+4)*(lineCount-1)))
    
    if i !=0:
        line[0:1]=[]

    while(True):
        try:
            ind = line.index(' ')
        except ValueError:
            break
        line[ind:ind+1]=[]
    
    while(True):
        try:
            ind = line.index('-')
        except ValueError:
            break
        line[ind:ind+1]=[]
        line[ind] = '-' + line[ind]
    try:
        ind = line.index('\n')
    except ValueError:
        print 'oups %i' % (i)

    line[ind:ind+1] = []
    simiMatrix[i] = line

simi = {}

for i,line in enumerate(simiMatrix):
    for j,letter in enumerate(simiMatrix[0]):
        try:
            key = simiMatrix[0][i] + letter
            score = line[j]
        except IndexError:
            break
        try:
            simi[key] = int(score)
        except ValueError:
            score = simiMatrix[i+1][j]
            simi[key] = int(score)

for i,letter in enumerate(simiMatrix[0]):
    for j,letter in enumerate(simiMatrix[0]):
        try:
            key= letter + letter
            simi[key]
        except:
            print 'Didn\'t found %s' % (key)

