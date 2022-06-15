def test(): pass

def test2():
    pass

def test3(op): exit(3); \
        exit(4)

def test4(): return 1,2

def test5():
    return test4(), 2

exit(test3(2 + 2))
