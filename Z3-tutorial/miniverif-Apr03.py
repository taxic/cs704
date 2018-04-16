from z3 import *
from itertools import combinations

def isValid(phi):
    s = Solver()
    s.add (Not(phi))
    if s.check() == sat:
        return False
    else:
        return True

def isSAT(phi):
    s = Solver()
    s.add (phi)
    return s.check() == sat


############################
# predicate abstraction
# 3^|preds| possible abstractions

def abstract(phi, preds):
    res = And(True)   # if we write res = True, it will cause problems

    for p in preds:
        if isValid(Implies(phi,p)):
            res = And(res, p)
        if isValid(Implies(phi, Not(p))):
            res = And(res, Not(p))

    return simplify(res)

def isFixpoint(oldInv, newinv):
    return isValid (Implies(newinv, oldInv))

def booleanAbstract(phi, preds):
    res = And(False)
    negpreds = map (lambda x: Not(x), preds)

    for ps in combinations(preds + negpreds, len(preds)):
        if isSAT(And(phi, *ps)):
            res = Or(res, And(*ps))

    return simplify(res)


###########################
# example
# create a bunch of variables
x = Int('x')
y = Int('y')
z = Int('z')
r = Int('r')
q = Int('q')
lock = Int('lock')
old = Int('old')
new = Int('new')

xp = Int('xp')
yp = Int('yp')
zp = Int('zp')
rp = Int('rp')
qp = Int('qp')
lockp = Int('lockp')
oldp = Int('oldp')
newp = Int('newp')

# we make two lists for pairs of variables
varMap = [(x,xp), (y,yp), (z,zp), (r,rp), (q,qp), (lock,lockp), (old,oldp), (new,newp)]
varMapRev = map(lambda v: (v[1], v[0]), varMap)

##############################
### example 1 
"""
{x = 0, y = 0}
while(*)
    y = y + 1
    x = x + 1
{y = 10 -> x = 10}
"""
pre = And(x == 0, y == 0)
trans = And(xp == x + 1, yp == y + 1)
post = Implies (y == 10, x == 10)

# preds = [x > 0]
# preds = [x >= 0]
preds = [x >= y, x <= y]
# preds = [x == 0, y == 0, y == 1, x == 1, x == 2, y == 2]


#########################
### example 2
"""
{x = 10, y = 10}
while (x + y > 0):
    x = x - 1
    y = y - 1
    z = x + y
{z = 0}
"""
pre = And(x == 10, y == 10)
trans = And(x + y > 0, xp == x - 1, yp == y - 1, zp == xp + yp)
# here, we add the (x + y > 0), the while-condition, to trans
post = Implies (x + y <= 0, z == 0)

'''
wrong_inv = Implies((x + y < 20), And(z == x + y, x + y >= 0))
inv = And(x == y, Implies((x + y < 20), And(z == x + y, x + y >= 0)))
invp = substitute(inv, varMap)
print isValid(Implies(pre, inv))
print isValid(Implies(And(inv, x + y > 0, And(xp == x - 1, yp == y - 1, zp == xp + yp)), invp))
print isValid(Implies(And(inv, x + y <= 0), post))
'''
# preds = [x >= 0]  # don't know
# preds = [x == y]  # don't know
# preds = [x > 0, x == y, z == x + y] # don't know
preds = [x >= 0, x == y, z == x + y]
# preds = [x + y == 20, x + y < 20, z == x + y, x + y >= 0, x == y]

########################
### example 3
'''
{x >= 0, y >= 0}
r = x
q = 0
while (r >= y){
    r = r - y
    q = q + 1
}
{x = y * q + r, 0 <= r < y}
'''
pre = And(x >= 0, y >= 0, r == x, q == 0)
trans = And(r >= y, rp == r - y, qp == q + 1)
post = Implies(r < y, And(r < y, r >= 0, x == y * q + r))

preds = [x > 0, y > 0, r > 0, x == 0, y == 0, r == 0, x == r, r == y, x == y * q + r, q > 0, q == 0, r > y]
########################

predsprime = map(lambda p: substitute(p,*varMap), preds)
oldInv = False
inv = pre
i = 0
while not isFixpoint(oldInv, inv):
    print "\nInv at : ", i , " : ", inv
    i = i + 1

    onestep = And(inv, trans)
    onestep = abstract(onestep, predsprime)
    onestep = substitute(onestep, varMapRev)
    oldInv = inv
    inv = simplify(Or(inv, onestep)) 

print "\n"
if isValid(Implies(inv, post)):
    print ">>> CORRECT \n\n"
else:
    print ">>> I don't know \n\n"

exit()


###ex3
init = And(x == y)
trans = And(xp == x + 1, yp == y + 1)
post = Or(And(x % 2 == 0, y % 2 == 0), And(x % 2 != 0, y % 2 != 0))

preds = [x % 2 == 0, y % 2 == 0]

###ex4
init = And(lock == 0, new != old)

trans = And(new != old, oldp == new,
            Or(And(lockp == 0, newp == new + 1),
                And(lockp == 1, newp == new)))

post = Implies(new == old, lock != 0)

preds = [lock == 0, new == old]


#####################################

predsprime = map(lambda p: substitute(p,*varMap), preds)

oldInv = False
inv = booleanAbstract(init, preds)

i = 0
while not fixpoint(oldInv,inv):
    print "\nInv at ", i, ": ", inv
    i = i + 1

    # existential quantifer??
    onestep = booleanAbstract(And(inv, trans), predsprime)
    onestep = substitute(onestep, varMapRev)
    oldInv = inv
    inv = simplify(Or(inv, onestep))

print "\n"
