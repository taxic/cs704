from z3 import *
def isValid(f):
    s = Solver()
    s.add(Not(f))
    if s.check() == sat:
        print s.model()
        return False
    else:
        return True

# 2.A
x = Int('x')
r = Int('r')
q = Int('q')
y = Int('y')
x1 = Int('x1')
r1 = Int('r1')
q1 = Int('q1')
y1 = Int('y1')
trans = And(r1 == r - y, q1 == q + 1, x1 == x, y1 == y)
inv = And(x == r + y * q, r >= 0)
inv1 = And(x1 == r1 + y1 * q1, r1 >= 0)
b = r >= y
vc = Implies(And(inv, b, trans), inv1)
print isValid(vc)

# 2.C
z = Int('z')
z1 = Int('z1')
trans = And(x1 == x - 1, y1 == y + 1, z1 == x + y)
inv = And(Implies(x + y == 20, True), Implies(x + y < 20, And(z == x + y, x + y >= 0)))
inv1 = And(Implies(x1 + y1 == 20, True), Implies(x1 + y1 < 20, And(z1 == x1 + y1, x1 + y1 >= 0)))
b = x + y > 0

vc = Implies(And(inv, b, trans), inv1)
print isValid(vc)
