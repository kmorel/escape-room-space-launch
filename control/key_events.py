import direct.showbase.DirectObject

import html_server_earth_base

class KeyEvents(direct.showbase.DirectObject.DirectObject):
    def __init__(self, base):
        self.base = base

        self.accept('q', self.quit)

    def quit(self):
        html_server_earth_base.stop()
        self.base.userExit()
