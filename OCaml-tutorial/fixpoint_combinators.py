# most from http://matt.might.net/articles/python-church-y-combinator/
Delta = lambda x : x(x)

# customized recursive lambda calculus
fact = lambda h: lambda x: 1 if x == 0 else x * (h (h))(x - 1)
factu = Delta (fact)

print (factu (6))

fib = lambda f: lambda x: x if (x == 0 or x == 1) else f(x - 1) + f(x - 2)


# In Python, Y2 and Y3 doesn't work.
# Because Python uses Call-By-Value beta-reduction
# Y2 = Delta (lambda h: lambda f: f (h (h)) (f))
# Y3 = lambda g: (Delta (lambda x: g (x (x))))

# we need to apply eta-expansion to Y2 and Y3:
Y1 = Delta (lambda h: lambda f: f (lambda x: (h (h)) (f) (x)))
print (Y1 (fib) (7))

Y4 = lambda g: (Delta (lambda x: g (lambda y: (x (x)) (y))))
print (Y4 (fib) (30))

# caching Y combinator
def Ymem(F, cache=None):
    if cache is None:
        cache = {}

    def fun(arg):
        if arg in cache:
            return cache[arg]

        res = (F(lambda n: (Ymem(F, cache))(n)))(arg)
        cache[arg] = res
        return res
    return fun

print (Ymem (fib) (300))
