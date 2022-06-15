# comment

def test():
    return 1, 2, 3, 4


test()

(a,
 b,
 c,
 d) = test()

# this line ...
(a, b, (c, d)) = (a, a, (a, a))
# compiles in same bytecode as this ...
a = a; b = a; (c, d) = (a, a)
# and this...
a = a; b = a; c = a; d = a