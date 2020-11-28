import panda3d.core
import direct.task.Task
import direct.task.TaskManagerGlobal

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
        direct.task.TaskManagerGlobal.taskMgr.remove('clear-digit')
        direct.task.TaskManagerGlobal.taskMgr.add(
            self.clear_digit_task, 'clear-digit')

    def clear_digit_task(self, task):
        # Clear out digit after 30 seconds
        if task.time < 30:
            return direct.task.Task.cont
        else:
            self.node.setTexture(self.digit_textures[0])
            return direct.task.Task.done
