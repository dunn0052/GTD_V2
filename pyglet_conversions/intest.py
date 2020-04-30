
class A(object):
    _A = "tests"

    def __init__(self):
        pass

    def A(self):
        print(self._A)

class B(A):
    pass

    def C(self):
        print(self._A)

b = B()

b.C()
