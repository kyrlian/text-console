
class Panel:

    def __init__(self, title="", content="", status="normal"):
        self.controls = "□_|x"
        self.title = title
        self.status = status
        self.initcontent(content)
        self.update()

    def attachtozone(self, zone):
        self.zone = zone
        
    def preferedsizes(self):
        self.sizes=[.1,.5,.9]

    def initcontent(self,content):
        self.content=content

    def updatecontent(self):
        pass

    def update(self):
        self.updatecontent()
        self.contentheigth = 0
        if len(self.content) > 0:
            self.contentheigth = 1
            if len(self.content[0]) > 1:  # if txt is an array (multiline)
                self.contentheigth = len(self.content)
        self.preferedsizes()#is after init content, so it can use self.contentheigth

    def toggleminimised(self):
        if self.status == "minimized":
            self.status = "normal"
            self.zone.parent.resize(self.sizes[1])
        elif self.status == "normal":
            self.status = "maximized"
            self.zone.parent.resize(self.sizes[2])
        else:
            self.status = "minimized"
            self.zone.parent.resize(self.sizes[0])

    def getcolor(self, context):
        if context.focusedpanel == self:
            return (200, 200, 200)
        else:
            return (100, 100, 100)

    def isclicked(self, charx, chary):
        return charx >= self.zone.x and charx < self.zone.x + self.zone.w and chary >= self.zone.y and chary < self.zone.y + self.zone.h

    def handlecontrolclick(self, charx, chary):
        controlsminimize = -5  # "□_|x"
        controlssplith = -4
        controlssplitv = -3
        controlsclose = -2
        if chary == self.zone.y:
            if charx == self.zone.x + self.zone.w + controlsminimize:
                print("clicked minimize")
                self.toggleminimised()
            elif charx == self.zone.x + self.zone.w + controlssplith:
                print("clicked split h")
                self.zone.split("h", .5)
            elif charx == self.zone.x + self.zone.w + controlssplitv:
                print("clicked split v")
                self.zone.split("v", .5)
            elif charx == self.zone.x + self.zone.w + controlsclose:
                print("clicked close")
                self.zone.remove()

    def handlepanelclick(self, charx, chary):
        self.handlecontrolclick(charx, chary)

    def draw(self):
        txtarray = []
        for i in range(self.zone.y):
            txtarray.append("")
        txtarray.append(" "*self.zone.x+"╔"+self.title+"═"*(self.zone.w-2-len(self.title) -
                        len(self.controls))+self.controls+"╗")  # top border
        if self.contentheigth > 0:
            if self.contentheigth > 1:  # if txt is an array (multiline)
                for ti in range(self.contentheigth):
                    txtline = self.content[ti]
                    txtarray.append(" "*self.zone.x+"║"+txtline +
                                    " "*(self.zone.w-2-len(txtline))+"║")
            else:
                txtarray.append(" "*self.zone.x+"║"+self.content +
                                " "*(self.zone.w-2-len(self.content))+"║")
        for i in range(self.zone.h-2-self.contentheigth):
            txtarray.append(" "*self.zone.x+"║"+" "*(self.zone.w-2)+"║")
        txtarray.append(" "*self.zone.x+"╚"+"═" *
                        (self.zone.w-2)+"╝")  # bottom border
        cutarray=[]#generate copy array staying in the zone
        for y in range(self.zone.y+self.zone.h):
            cutarray.append(txtarray[y][0:self.zone.x+self.zone.w])
        return cutarray
