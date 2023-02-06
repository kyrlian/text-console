from panel import Panel
from datetime import datetime

class Panelclock(Panel):

    def preferedsizes(self):
        self.sizes=[4,4,4]

    def update(self):
        self.content = [datetime.now().strftime("%m/%d/%Y"), datetime.now().strftime("%H:%M:%S")]
        self.contentheigth = 2