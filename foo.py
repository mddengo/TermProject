def bonus1(x, L=[42]):
    def g():
        (result, L[0]) = (L[0], L[0]+L[0])
        return result
    def f(f): L[0]=1; return sum([g() for f in range(f)])
    return f(x)

def bonus2(s):
    assert((type(s) == type("def")) and ("def" not in s))
    def g(s): return s*s
    return ([eval(eval(s))(g,x) for x in range(3,5)] == [12, 20])