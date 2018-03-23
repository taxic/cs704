# Run with Python2
#   $ python2 week8-examples.py

from z3 import *
# basic usage steps:
# 1. define vars
x = Int('x')
y = Int('y')
# 2. write formula(e)
phi = x + y > 0
# 3. create a solver
s = Solver()
# 4. add formula(e) to the solver
s.add(phi)
# 5. check sat or not
print s.check()
# 6. (option) if sat, model exists
print s.model()
m = s.model()
print "x is ", m[x]
print "y is ", m[y]

s.reset()
phi = And(x + y > x, y < 0)
s.add(phi)
print s.check()
# print s.model() 
"""
Traceback (most recent call last):
  File "Z3-tutorial/week8-examples.py", line 27, in <module>
      print s.model()
        File "/u/z/h/zhicheng/z3-z3-4.5.0/build/python/z3/z3.py", line 6118, in model
            raise Z3Exception("model is not available")
        z3.z3types.Z3Exception: model is not available
"""
# A => B is VALID: for any m, m |= A => B
def isValid(f):
    s = Solver()
    s.add(Not(f))
    if s.check() == sat:
        print s.model()
        return False
    else:
        return True

A = x > 10
B = x > -10
phi = Implies(A, B) # which is valid
print isValid(phi)
print isValid(Implies(x > 0, x > 10))


# Bool type
p = Bool('p')
q = Bool('q')
r = Bool('r')
s.reset()
# check (p \/ q) /\ (q => r)
s.add(And(Or(p, q), Implies(q, r)))
print s.check()
print s.model()
# want a new model
m = s.model()
s.add(Or(p != m[p], q != m[q], r != m[r]))
print s.check()
print s.model()
