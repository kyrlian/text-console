""" clock panel """
#kyrlian, 2023

from datetime import datetime
from panel import Panel

class PanelClock(Panel):
    """ clock panel """

    def __init__(self, title="Clock", initargs=None, status="normal"):
        Panel.__init__(self, title, initargs, status)

    def preferedsizes(self):
        self.sizes=[4,4,4]

    def updatecontent(self):
        self.content = [datetime.now().strftime("%m/%d/%Y"), datetime.now().strftime("%H:%M:%S")]
