"""
Your implementation should take a Hoare triple:
{\phi} 
while b do P_{body}  
{\psi}
"""
from z3 import *
def kInduction(k, b, enc):
# Input:    k (>= 1), b, enc(P_{body})
# Output:   "success" or "failure"

# Requirements:
#   1. exhaustively comment the code
#   2. encode 3 non-trivial Hoare triples
#   3. a valid Hoare triple, where k-induction cannot prove correctness
#      (with explanation)

