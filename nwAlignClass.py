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
    def __init__(self, strTop, strLeft, pMatch=1, pMismatch=-1):
        # Dimensions of the nwMatrix (N:rows, M:columns)
        self.N, self.M = len(strLeft)+1, len(strTop)+1
        # Compared top and left string
        self.strLeft, self.strTop = strLeft, strTop 
        # Penalty for match and mismatch
        self.pMatch, self.pMismatch = pMatch, pMismatch
        
        # List of paths
        self.pathList = []

        # Creating dummy Matrix
        self.matrix = [[slot() for i in xrange(self.M)] for j in \
                                                            xrange(self.N)]
        self.initMatrix()

    def initMatrix(self):
        # Initializing scores
        for i in xrange(self.N):
            self.matrix[i][0].score, self.matrix[i][0].processed = -i,True
            if i>0:
                self.matrix[i][0].origin =[False, False, True]
        for i in xrange(1,self.M):
            self.matrix[0][i].score, self.matrix[0][i].processed = -i, True
            if i>0:
                self.matrix[i][0].origin =[True, False, False]
        
        # Match/Mismatch
        self.matchMatrix = (np.array([list(self.strLeft)]).transpose() \
        ==list(self.strTop))
        
        # Assign Match/misMatch penalty
        self.assignPenalty()
        # Fill Matrix
        self.computeScore()

        self.findPaths('',self.N-1, self.M-1)

        print self.pathList

        #  =======
        # == END ==
        #  =======


    def printMatrix(self):
        print "NW Matrix"
        print np.array([[self.matrix[j][i].score for i in xrange(self.M)] \
                                                 for j in xrange(self.N)])

    def printPenalty(self):
        print "Penalty Matrix:"
        print np.array([[self.matrix[j][i].penalty for i in xrange(self.M)] \
                                                   for j in xrange(self.N)])

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
                self.findPaths(path + 'v',i-1,j)
            if(self.matrix[i][j].origin[1]):
                self.findPaths(path + 'd',i-1,j-1)
            if(self.matrix[i][j].origin[2]):
                self.findPaths(path + 'h', i,j-1)



