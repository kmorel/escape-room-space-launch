import panda3d.core
import direct.task.Task
import direct.task.TaskManagerGlobal

import panda3d_utils

import random

class Satellite:
    def __init__(self, base):
        random.seed()

        self.texture_off = \
            base.loader.loadTexture('images/spaceship/satellite-off.png')
        self.texture_on = \
            base.loader.loadTexture('images/spaceship/satellite-on.png')

        self.node = base.render.attachNewNode(
            panda3d_utils.make_billboard('satellite'))
        width = 0.5
        ratio = self.texture_off.getYSize()/self.texture_off.getXSize()
        self.node.setScale(width, width * ratio, 1)
        self.node.setTransparency(True)

        self.target_x = 0.15
        self.target_y = 0.25

        self.x = self.target_x
        self.y = self.target_y

        self.node.setPos(self.x, self.y, 0)
        self.node.setTexture(self.texture_off)

        self.pause_dot = 0.25
        self.pause_dash = 0.75
        self.pause_between = 0.5
        self.pause_end = 4

        direct.task.TaskManagerGlobal.taskMgr.add(self.between_task, 'light')

    def between_task(self, task):
        self.node.setTexture(self.texture_off)
        if task.time < self.pause_between:
            return direct.task.Task.cont
        else:
            direct.task.TaskManagerGlobal.taskMgr.add(self.dash_task, 'light')
            return direct.task.Task.done

    def dot_task(self, task):
        self.node.setTexture(self.texture_on)
        if task.time < self.pause_dot:
            return direct.task.Task.cont
        else:
            direct.task.TaskManagerGlobal.taskMgr.add(self.between_task, 'light')
            return direct.task.Task.done

    def dash_task(self, task):
        self.node.setTexture(self.texture_on)
        if task.time < self.pause_dash:
            return direct.task.Task.cont
        else:
            direct.task.TaskManagerGlobal.taskMgr.add(self.between_task, 'light')
            return direct.task.Task.done
