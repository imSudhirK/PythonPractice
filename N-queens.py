from z3 import *

import argparse
import itertools
import time 
import numpy as np
import sys 


#taking integer as input 
print ("Enter N : ")
n = int(input())
print ("\n")

#creating a 2D array
rows, cols = (n, n)
vs = []

#filling array with variable (literls)
for r in range(rows):
	nameX = "x_{}".format(r)
	colX =[]
	for c in range(cols):
		nameY = "y_{}".format(c) 
		colY= Bool(nameX + nameY)
		colX.append(colY)
	vs.append(colX)

#now overloading the array as 2D matrix of numpy 
numpyVS = np.array(vs)


#define a function  to find exactly one true value form set of literals 
def exactly_one(ls):
	at_least_one = Or (ls)
	at_most_one_list = []
	for pair in itertools.combinations(ls,2):
		l1 = pair[0]
		l2 = pair[1]
		at_most_one_list.append(Or (Not(l1), Not(l2)))
	at_most_one = And (at_most_one_list)
	return And (at_least_one, at_most_one)



#each row should have exactly one true value - constraint 1
xor_one_all_col = exactly_one(vs[n-1])
for x in range(n-1):
	xor_one_all_col = And ( xor_one_all_col , exactly_one(vs[x]))

#each column should have exactly one true value - constraint 2
coln =[ row[n-1] for row in vs ]
xor_one_all_row =exactly_one(coln) 
for y in range(n-1):
	coly = [ row[y] for row in vs ]
	xor_one_all_row = And ( xor_one_all_row , exactly_one(coly))

# constraint 1 , constraint 2 suffice that here are N queens on N*N chess board - constraint 0


#define a function to find at most true value from a set of literals 
#it could be utilized in above function  but I am not doing for easy debugging 

def At_most_one(ls):
	at_most_one_list = []
	for pair in itertools.combinations(ls,2):
		l1 = pair[0]
		l2 = pair[1]
		at_most_one_list.append(Or (Not(l1), Not(l2)))
	return And (at_most_one_list)


#each diagonal should not have more than one true value - constarint 3

#one way diagonals should not have more than one true value
atm_one_d1 = Bool(0)
for i in range (1-n , n):
	#print(i)
	atm_one_d1 = And (atm_one_d1, At_most_one(np.diag(numpyVS, i)))


#also 2nd way diagonals should not have more than one true value
rotatedVS= np.rot90(numpyVS)

atm_one_d2 = Bool(0)
for i in range (1-n , n):
	#print(i)
	atm_one_d2 = And (atm_one_d2, At_most_one(np.diag(rotatedVS, i)))


# Our final CNF
clause = And(xor_one_all_row, xor_one_all_col, atm_one_d1, atm_one_d2)


#now overloading to SAT-solver 
s= Solver()           
s.add(clause)

if s.check() == sat:
    m = s.model()
    r = [ [ m.evaluate(numpyVS[i][j]) for j in range(n) ] 
          for i in range(n) ]
    print_matrix(r)                    #prints a model in matrix form
else:
    print ("unsat")
