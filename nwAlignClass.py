"""
nwAlignClass.py

This class file is intended to work with the 'atiam-fpa.py'. It is an
implementation of the Neddleman-Wunsch string alignement algorithm.

Victor Wetzel, ATIAM 2017-2018
e-mail: wetzel.victor (at) gmail.com
github: WetzelVictor
"""

import numpy as np

# =========== SLOT ===========
#
# slot: defines a slot in a Needleman-Wunsch Matrix
#
#   FIELD VARIABLES:
#       - score (int): score calculated from the TOP, TOP-LEFT and LEFT slots.
#       - origin (array): List of the location of the highest score
#       anti-clockwise:  ==> 0: top
#                        ==> 1: diagonal (top left)
#                        ==> 2: left
#       - Processed (Boolean): if the slot has already been processed by an
#       other process
#       - FX: The cost of that match/dismatch of the slot
#
#   METHODS:
#       - NONE

class slot:
    def __init__(self):
        self.score = None
        self.processed = False
        self.origin = [False, False, False]
        self.penalty = None


# =========== matrix ===========
#
# matrix: Needleman-Wunsch Matrix used in the alignement algorithm. Build
# after two string's length. 
#           Filled with 'slot' objects.
#
#

class nwMatrix:
    def __init__(self, strTop, strLeft, \
                       pMatch=1, pMismatch=-1,\
                       similarityMatrix=None,
                       gap_open=-10,
                       gap_extend=-1,
                       simiMatrix='atiam-fpa_alpha.dist'):

        # Dimensions of the nwMatrix (N:rows, M:columns)
        self.N, self.M = len(strLeft)+1, len(strTop)+1
        # Compared top and left string
        self.strLeft, self.strTop = strLeft, strTop 
        # Penalty for match and mismatch
        self.pMatch, self.pMismatch = pMatch, pMismatch
        self.gap_open, self.gap_extend = gap_open, gap_extend
        

        # List of paths
        self.pathList = []

        # Creating dummy Matrix
        self.matrix = [[slot() for i in xrange(self.M)] for j in \
                                                            xrange(self.N)]
        self.initMatrix()

        if similarityMatrix is None:
            self.simiMode = 'default'
        else:
            self.simiMode = 'matrix'
 
        # Match/Mismatch
        self.matchMatrix = (np.array([list(self.strLeft)]).transpose() \
        ==list(self.strTop))
        
        # Assign Match/misMatch penalty
        self.assignPenalty()
        
        # Fill Matrix
        self.computeScore()

        # find paths
        self.findPaths('',self.N-1, self.M-1)

        # List of possible alignements
        self.alignements = [['',''] for i in xrange(len(self.pathList))]
        self.scores = [None for i in xrange(len(self.pathList))]
        self.makeAlignements()

        self.simi = {}
        self.simiDict(simiMatrix)
        self.scoreAlignements()
        
        # print 'Best Alignement: ' + str(max(self.scores))
        # print self.alignements[np.argmax(self.scores)][0]
        # print self.alignements[np.argmax(self.scores)][1]

        self.bestAlignement = self.alignements[np.argmax(self.scores)]
        
    def initMatrix(self):
        # Initializing scores
        for i in xrange(self.N):
            self.matrix[i][0].score, self.matrix[i][0].processed = -i,True
            if i>0:
                self.matrix[i][0].origin =[False, False, True]
        
        for i in xrange(1,self.M):
            self.matrix[0][i].score, self.matrix[0][i].processed = -i, True
            if i>0:
                self.matrix[0][i].origin =[True, False, False]

    def computeScore(self):
        for i in xrange(1, self.N):
            for j in xrange(1, self.M):
                adjacents = np.array([self.matrix[i-1][j].score,   \
                              self.matrix[i-1][j-1].score, \
                              self.matrix[i][j-1].score])
                
                self.matrix[i][j].score = max(adjacents) + self.matrix[i][j].penalty
                self.matrix[i][j].origin = (adjacents + \
                                            self.matrix[i][j].penalty == \
                                            self.matrix[i][j].score)
                 
                if not True in self.matrix[i][j].origin:
                    print str(i) + '-' + str(j)

    def assignPenalty(self):
        for i in xrange(self.N-1):
            for j in xrange(self.M-1):
                if(self.matchMatrix[i][j]):
                    self.matrix[i+1][j+1].penalty = self.pMatch
                else:
                    self.matrix[i+1][j+1].penalty = self.pMismatch
    
    def findPaths(self, path, i, j):
        if(not True in self.matrix[i][j].origin):
            self.pathList.append(path)
        else:
            if(self.matrix[i][j].origin[0]):
                self.findPaths('v' + path,i-1,j)
            if(self.matrix[i][j].origin[1]):
                self.findPaths('d' + path,i-1,j-1)
            if(self.matrix[i][j].origin[2]):
                self.findPaths('h' + path, i,j-1)
    
    def makeAlignements(self):
        for i,path in enumerate(self.pathList):
            al1, al2 = '', ''
            iT, iL = 0, 0

            for j,direction in enumerate(path):
                if direction == 'd':
                    al1, al2 = al1 + self.strTop[iT], al2 + self.strLeft[iL]
                    iT, iL = iT + 1, iL + 1
                elif direction == 'v':
                    al1, al2 = al1 + '-', al2 + self.strLeft[iL]
                    iL = iL + 1
                elif direction == 'h':
                    al1, al2 = al1 + self.strTop[iT], al2 + '-'
                    iT = iT + 1
            # Storing
            self.alignements[i] = [al1, al2]

    def printMatrix(self):
        print "NW Matrix"
        print np.array([[self.matrix[j][i].score for i in xrange(self.M)] \
                                                 for j in xrange(self.N)])

    def printPenalty(self):
        print "Penalty Matrix:"
        print np.array([[self.matrix[j][i].penalty for i in xrange(self.M)] \
                                                   for j in xrange(self.N)])
            

    def simiDict(self,fileName):
        dist = open(fileName)
        with dist as f:
                lineCount = sum(1 for _ in f)

        dist = open(fileName)
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

        self.simi = {}

        for i,line in enumerate(simiMatrix):
            for j,letter in enumerate(simiMatrix[0]):
                try:
                    key = simiMatrix[0][i] + letter
                    score = line[j]
                except IndexError:
                    break
                try:
                    self.simi[key] = int(score)
                except ValueError:
                    score = simiMatrix[i+1][j]
                    self.simi[key] = int(score)

        for i,letter in enumerate(simiMatrix[0]):
            for j,letter in enumerate(simiMatrix[0]):
                try:
                    key= letter + letter
                    self.simi[key]
                except:
                    print 'Didn\'t found %s' % (key)


    def scoreAlignements(self):
        for i,ali in enumerate(self.alignements):
            #init
            score = 0
            gap_open1, gap_open2 = True, True
            # print ali

            for j in xrange(len(ali[0])):
                l1, l2 = ali[0][j], ali[1][j]
                
                if l1 == '-':
                    if gap_open1:
                        score += self.gap_open
                        gap_open1= False
                    else:
                        score += self.gap_extend
                elif l2 == '-':
                    if gap_open2:
                        score += self.gap_open
                        gap_open2= False
                    else:
                        score += self.gap_extend
                else:
                    gap_open1, gap_open2 = True, True
                    try:
                        key = l1+l2
                        score += self.simi[key]
                    except KeyError:
                        if l1 == l2:
                            score += self.pMatch
                        else:
                            score += self.pMismatch 
            
            self.scores[i] = score;

