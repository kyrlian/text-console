""" cursor class """
#kyrlian, 2023

class Cursor():
    """ cursor class """
    def __init__(self, symbols=["█",""] ):
        self.position = [0, 0] #char, line
        self.cyclesymbols = symbols  # █░▒▓
        self.symbol = self.cyclesymbols[0]
        self.cycleframes = 10
        self.cyclecounter = self.cycleframes

    def getline(self):
        """ get cursor line """
        return self.position[1]

    def getchar(self):
        """ get cursor char """
        return self.position[0]

    def setline(self,y):
        """ set cursor line """
        self.position[1]=y

    def setchar(self,x):
        """ set cursor char """
        self.position[0]=x

    def cyclecursor(self, char=None):
        """ cycle cursor and char symbols """
        self.cyclecounter-=1
        if self.cyclecounter < 0:
            self.cyclecounter = self.cycleframes
            i = self.cyclesymbols.index(self.symbol)
            nexti = (i+1) % len(self.cyclesymbols)
            self.symbol = self.cyclesymbols[nexti]
        if char is not None and self.symbol =="":
            return char
        return self.symbol

    def placeincontent(self,cx,cy,linesarray):
        """ replace cursor in a text array """
        newy = min(max(0,cy),len(linesarray)-1)
        self.setline(newy)
        self.setchar(min(max(0,cx),len(linesarray[newy])))

    # def moverel(self,dx,dy):
    #     self.position=[self.getchar()+dx,self.getline()+dy]

    # def moveabs(self,x,y):
    #     self.position=[x,y]
