#kyrlian, 2023

class TextHelper:

    def getline(self,ar, y):
        if (y < len(ar)):
            return ar[y]
        return ""

    def getchar(self,ar, x, y):
        if (y < len(ar)):
            if (x < len(ar[y])):
                return ar[y][x:x+1]
        return ""

    def mergetwoarrays(self,a, b):
        o = []
        for y in range(max(len(a), len(b))):
            to = ""
            la = self.getline(a, y)
            lb = self.getline(b, y)
            for x in range(max(len(la), len(lb))):
                tto = self.getchar(a, x, y)
                cb = self.getchar(b, x, y)
                if cb != "" and cb != " ":
                    tto = cb
                to += tto
            o.append(to)
        return o

    def mergearrays(self, aa):
        o = aa[0]
        for i in range(1, len(aa), 1):
            o = self.mergetwoarrays(o, aa[i])
        return o