class A:
    def __init__(self, title=""):
        self.title=title
        self.myclass="A"

class B(A):
    def __init__(self, title=""):
        A.__init__(self, title)
        self.myclass="B"
        self.subarg="test"

a=A("my a")
b=B("my b")
print(a.myclass)
print(b.subarg)