from z3 import *
def isValid(f):
    s = Solver()
    s.add(Not(f))
    if s.check() == sat:
        print s.model()
        return False
    else:
        return True

# Here, we argue an valid example:
# {x > 0} x <- x + 1 {x > 1}
# 
# (x > 0 /\ x' = x + 1) => x' > 1
#  pre        enc          post
x = Int('x')
x1 = Int('x1')
pre = x > 0
post = x1 > 1
enc = x1 == x + 1
vc = Implies(And(pre, enc), post)
print isValid(vc)

# Now consider:
# {x > 0} x <- x + y {x > 1}
# 
# (x > 0 /\ x' = x + y) => x' > 1
#  pre        enc          post
y = Int('y')
y1 = Int('y1')
x = Int('x')
x1 = Int('x1')
pre = x > 0
post = x1 > 1
enc = And(x1 == x + y, y1 == y)
vc = Implies(And(pre, enc), post)
print isValid(vc)

# More example:
"""
{lock == 0 /\ new != old}
while new != old:
    old = new
    if (*):
        lock = 0
        new ++
    else:
        lock = 1
{lock != 0}
"""
lock = Int('lock')
lock1 = Int('lock1')
new = Int('new')
new1 = Int('new1')
old = Int('old')
old1 = Int('old1')
trans = And(old1 == new, Or(And(lock1 == 0, new1 == new + 1), And(lock1 == 1, new1 == new)))
b = new != old
inv = Implies(new == old, lock != 0)
inv1 = Implies(new1 == old1, lock1 != 0)
vc = Implies(And(inv, b, trans), inv1)
print isValid(vc)
