import panda3d.core
import direct.task.Task
import direct.task.TaskManagerGlobal

import panda3d_utils

from spaceship import satellite

import random

class Launcher:
    def __init__(self, base):
        random.seed()

        ratio = base.cam.node().getLens().getAspectRatio()

        background_texture = \
            base.loader.loadTexture('images/spaceship/background.png')

        self.background = base.render.attachNewNode(
            panda3d_utils.make_billboard('background'))
        self.background.setTexture(background_texture)
        self.background.setPos(0, 3, -1)
        self.background.setScale(2*ratio, 8, 1)

        self.thud_sound = base.loader.loadSfx('audio/thud.ogg')
        self.launch_sound = base.loader.loadSfx('audio/rocket-launch.ogg')
        self.dialogue_before = base.loader.loadSfx(
            'audio/dialogue/launch-before.ogg')
        self.dialogue_after = base.loader.loadSfx(
            'audio/dialogue/launch-after.ogg')

        self.has_launched = False

    def launch(self):
        if self.has_launched:
            return
        self.has_launched = True
        panda3d_utils.play_then_run(self.dialogue_before, self.lock)

    def lock(self):
        panda3d_utils.play_then_run(self.thud_sound, self.start_launch)

    def start_launch(self):
        direct.task.TaskManagerGlobal.taskMgr.add(self.wait_task, 'launch')
        self.launch_sound.play()

    def wait_task(self, task):
        if task.time < 3:
            return direct.task.Task.cont
        else:
            direct.task.TaskManagerGlobal.taskMgr.add(self.shake_task, 'launch')
            return direct.task.Task.done

    def shake_task(self, task):
        if task.time < 4:
            shake = 0.1
            self.background.setPos(
                random.uniform(0 - shake, 0 + shake),
                random.uniform(3 - shake, 3 + shake),
                -1)
            return direct.task.Task.cont
        else:
            self.background.setPos(0, 3, -1)
            direct.task.TaskManagerGlobal.taskMgr.add(self.move_task, 'launch')
            return direct.task.Task.done

    def move_task(self, task):
        interp = task.time/18
        if interp < 1:
            self.background.setPos(0, 3 - (6 * interp), -1)
            return direct.task.Task.cont
        else:
            self.background.setPos(0, -3, -1)
            self.satellite = satellite.Satellite(base)
            self.dialogue_after.play()
            return direct.task.Task.done
