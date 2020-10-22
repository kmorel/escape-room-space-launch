import panda3d.core
import direct.task.Task
import direct.task.TaskManagerGlobal

import panda3d_utils

import enum
import random

class Code:
    DOT = enum.auto()
    DASH = enum.auto()
    END_LETTER = enum.auto()

message = [
    Code.DOT, Code.DOT, Code.DOT,  # S
    Code.END_LETTER,
    Code.DASH,                     # T
    Code.END_LETTER,
    Code.DOT, Code.DASH,           # A
    Code.END_LETTER,
    Code.DOT, Code.DASH, Code.DOT, # R
]

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
        self.pause_dash = 1
        self.pause_between_d = 0.5
        self.pause_end_letter = 1
        self.pause_end = 6

        self.code_location = 0

        direct.task.TaskManagerGlobal.taskMgr.add(self.between_d_task, 'light')

    def between_d_task(self, task):
        self.node.setTexture(self.texture_off)
        if task.time < self.pause_between_d:
            return direct.task.Task.cont
        else:
            if self.code_location < len(message):
                tasks = {
                    Code.DOT: self.dot_task,
                    Code.DASH: self.dash_task,
                    Code.END_LETTER: self.between_letter_task,
                }
                direct.task.TaskManagerGlobal.taskMgr.add(
                    tasks[message[self.code_location]], 'light')
                self.code_location += 1
            else:
                direct.task.TaskManagerGlobal.taskMgr.add(
                    self.end_task, 'light')
                self.code_location = 0
            return direct.task.Task.done

    def between_letter_task(self, task):
        self.node.setTexture(self.texture_off)
        if task.time < self.pause_end_letter:
            return direct.task.Task.cont
        else:
            direct.task.TaskManagerGlobal.taskMgr.add(self.between_d_task, 'light')
            return direct.task.Task.done

    def end_task(self, task):
        self.node.setTexture(self.texture_off)
        if task.time < self.pause_end:
            return direct.task.Task.cont
        else:
            direct.task.TaskManagerGlobal.taskMgr.add(self.between_d_task, 'light')
            return direct.task.Task.done

    def dot_task(self, task):
        self.node.setTexture(self.texture_on)
        if task.time < self.pause_dot:
            return direct.task.Task.cont
        else:
            direct.task.TaskManagerGlobal.taskMgr.add(self.between_d_task, 'light')
            return direct.task.Task.done

    def dash_task(self, task):
        self.node.setTexture(self.texture_on)
        if task.time < self.pause_dash:
            return direct.task.Task.cont
        else:
            direct.task.TaskManagerGlobal.taskMgr.add(self.between_d_task, 'light')
            return direct.task.Task.done
