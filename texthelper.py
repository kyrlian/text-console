class TextHelper:

    def ismultiline(ar):
        return len(ar) > 0 and len(ar[0]) > 1

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
            la = TextHelper.getline(a, y)
            lb = TextHelper.getline(b, y)
            for x in range(max(len(la), len(lb))):
                tto = TextHelper.getchar(a, x, y)
                cb = TextHelper.getchar(b, x, y)
                if cb != "" and cb != " ":
                    tto = cb
                to += tto
            o.append(to)
        return o

    def mergearrays(aa):
        o = aa[0]
        for i in range(1, len(aa), 1):
            o = TextHelper.mergetwoarrays(o, aa[i])
        return o