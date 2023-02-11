#kyrlian, 2023

class Cursor():

    def __init__(self):
        self.position = [0, 0] #char, line
        self.cyclesymbols = ["█",""]  # █░▒▓
        self.symbol = self.cyclesymbols[0]
        self.cycleframes = 10
        self.cyclecounter = self.cycleframes

    def getline(self):
        return self.position[1]

    def getchar(self):
        return self.position[0]

    def setline(self,y):
        self.position[1]=y
    
    def setchar(self,x):
        self.position[0]=x

    def cyclecursor(self, char=None):
        self.cyclecounter-=1
        if self.cyclecounter < 0:
            self.cyclecounter = self.cycleframes
            i = self.cyclesymbols.index(self.symbol)
            nexti = (i+1) % len(self.cyclesymbols)
            self.symbol = self.cyclesymbols[nexti]
        if char!= None and self.symbol =="":
            return char
        else :
            return self.symbol