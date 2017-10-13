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


        # Creating dummy Matrix
        self.matrix = [[slot() for i in xrange(self.M)] for j in \
                                                            xrange(self.N)]
        self.initMatrix()

        # Fill the Matrix
        # self.computeScore(self.N-1, self.M-1)


    def initMatrix(self):
        # Building the matrix
        
        # Initializing scores
        for i in xrange(self.N):
            self.matrix[i][0].score, self.matrix[i][0].processed = -i,True
        for i in xrange(1,self.M):
            self.matrix[0][i].score, self.matrix[0][i].processed = -i, True
        
        # Match/Mismatch
        self.matchMatrix = (np.array([list(self.strLeft)]).transpose() \
        ==list(self.strTop))
        
        # Assign Match/misMatch penalty
        self.assignPenalty()
        # Fill Matrix
        self.computeScore(1,1)
        self.computePaths(self.N, self.M) 
        #  =======
        # == END ==
        #  =======


    def printMatrix(self):
        print "NW Mtrix"
        print np.array([[self.matrix[j][i].score for i in xrange(self.M)] \
                                                 for j in xrange(self.N)])

    def printPenalty(self):
        print "Penalty Matrix:"
        print np.array([[self.matrix[j][i].penalty for i in xrange(self.M)] \
                                                   for j in xrange(self.N)])

    def computeScore(self, i, j):
        if(i == self.N or j == self.M):
            return None
        
        adjacents = np.array([self.matrix[i-1][j].score,   \
                              self.matrix[i-1][j-1].score, \
                              self.matrix[i][j-1].score])
        # print adjacents
        # if( None in adjacents):
            # return None

        self.matrix[i][j].score = max(adjacents) + self.matrix[i][j].penalty
        self.origin = (adjacents == self.matrix[i][j].score)
        
        self.computeScore(i,j+1)
        self.computeScore(i+1,j)


    def assignPenalty(self):
        for i in xrange(self.N-1):
            for j in xrange(self.M-1):
                if(self.matchMatrix[i][j]):
                    self.matrix[i+1][j+1].penalty = self.pMatch
                else:
                    self.matrix[i+1][j+1].penalty = self.pMismatch
    
    def computePaths(self, i, j, ID=0, path=[]):
        if( i==1 and j==1):
            return path
        else:
            if(self.matrix[i][j].origin[0]):
                self.computePaths(self, i-1,j, path + 'v')
                print 'v'
            elif(self.matrix[i][j].origin[1]):
                self.computePaths(self, i-1, j-1, path + 'd')
                print 'd'
            elif(self.matrix[i][j].origin[2]):
                self.computePaths(i, j-1, path + 'h',)
                print 'h'
        






# =========== path ===========
#
# path: a pile that computes and stores a way in a nwMatrix (see previous class).
#        /\
#       /!!\ Can be build we a given begining in cae there is several choices
#       ---- for the best score
#
#   FIELD VARIABLES:
#       - score: score of the path. The path that has the best score is the one
#       that we keep as best alignement.
#       - path (array): keeps track of the path through the matrix

# We need an array of stacks

class path:
    def __init__(self, path=[]):
        self.score = 0
        self.path = path


