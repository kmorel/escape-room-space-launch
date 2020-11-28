import panda3d.core

import panda3d_utils

class DigitDisplay:
    def __init__(self, base):
        self.digit_textures = [
            base.loader.loadTexture('images/control/digit-none.png'),
            base.loader.loadTexture('images/control/digit-1.png'),
            base.loader.loadTexture('images/control/digit-2.png'),
            base.loader.loadTexture('images/control/digit-3.png'),
            base.loader.loadTexture('images/control/digit-4.png'),
        ]
        ratio = 476/336

        self.node = base.render.attachNewNode(
            panda3d_utils.make_billboard('digit'))
        self.node.setScale(0.6, 0.6*ratio, 1)
        self.node.setPos(-0.4, 0.5, 1)
        self.node.setTexture(self.digit_textures[0])

        self.beep = base.loader.loadSfx('audio/beep.ogg')

    def set_digit(self, digit):
        self.node.setTexture(self.digit_textures[digit])
        self.beep.play()
