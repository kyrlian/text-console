class TxtHelper:
    def getline(ar, y):
        if (y < len(ar)):
            return ar[y]
        return ""

    def getchar(ar, x, y):
        if (y < len(ar)):
            if (x < len(ar[y])):
                return ar[y][x:x+1]
        return ""

    def mergetwoarrays(a, b):
        o = []
        for y in range(max(len(a), len(b))):
            to = ""
            la = TxtHelper.getline(a, y)
            lb = TxtHelper.getline(b, y)
            for x in range(max(len(la), len(lb))):
                tto = TxtHelper.getchar(a, x, y)
                cb = TxtHelper.getchar(b, x, y)
                if cb != "" and cb != " ":
                    tto = cb
                to += tto
            o.append(to)
        return o

    def mergearrays(aa):
        o = aa[0]
        for i in range(1, len(aa), 1):
            o = TxtHelper.mergetwoarrays(o, aa[i])
        return o