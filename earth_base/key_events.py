import direct.showbase.DirectObject

import html_server_earth_base

class KeyEvents(direct.showbase.DirectObject.DirectObject):
    def __init__(self, base, containers):
        self.base = base
        self.containers = containers

        self.accept('q', self.quit)
        self.accept('z', self.move, [0, 1])
        self.accept('x', self.move, [0, 2])
        self.accept('c', self.move, [1, 0])
        self.accept('v', self.move, [1, 2])
        self.accept('b', self.move, [2, 0])
        self.accept('n', self.move, [2, 1])

    def quit(self):
        html_server_earth_base.stop()
        self.base.userExit()

    def move(self, from_stack, to_stack):
        self.containers.move(from_stack, to_stack)
