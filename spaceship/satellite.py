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

        self.x = -1.5
        self.y = self.target_y

        self.v_x = 0
        self.v_y = 0

        self.node.setPos(self.x, self.y, 0)
        self.node.setTexture(self.texture_off)

        self.pause_dot = 0.25
        self.pause_dash = 1
        self.pause_between_d = 0.5
        self.pause_end_letter = 1
        self.pause_end = 6

        self.code_location = 0

        direct.task.TaskManagerGlobal.taskMgr.add(
            self.between_d_task, 'light')
        direct.task.TaskManagerGlobal.taskMgr.add(
            self.move_in_place_task, 'satellite_move')

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
            direct.task.TaskManagerGlobal.taskMgr.add(
                self.between_d_task, 'light')
            return direct.task.Task.done

    def end_task(self, task):
        self.node.setTexture(self.texture_off)
        if task.time < self.pause_end:
            return direct.task.Task.cont
        else:
            direct.task.TaskManagerGlobal.taskMgr.add(
                self.between_d_task, 'light')
            return direct.task.Task.done

    def dot_task(self, task):
        self.node.setTexture(self.texture_on)
        if task.time < self.pause_dot:
            return direct.task.Task.cont
        else:
            direct.task.TaskManagerGlobal.taskMgr.add(
                self.between_d_task, 'light')
            return direct.task.Task.done

    def dash_task(self, task):
        self.node.setTexture(self.texture_on)
        if task.time < self.pause_dash:
            return direct.task.Task.cont
        else:
            direct.task.TaskManagerGlobal.taskMgr.add(
                self.between_d_task, 'light')
            return direct.task.Task.done

    def move_in_place_task(self, task):
        total_time = 10
        if task.time < total_time:
            self.x = (self.target_x + 1.5) * (task.time/total_time) - 1.5
            self.node.setPos(self.x, self.y, 0)
            return direct.task.Task.cont
        else:
            direct.task.TaskManagerGlobal.taskMgr.add(
                self.jitter_task, 'satellite_move')
            return direct.task.Task.done

    def jitter_task(self, task):
        jitter = 0.00001
        max_move = 0.00005
        self.v_x += random.uniform(-jitter, jitter)
        self.v_x = min(max(self.v_x, -max_move), max_move)
        self.x += self.v_x
        self.x = min(max(self.x, self.target_x - 0.25), self.target_x + 0.25)
        self.v_y += random.uniform(-jitter, jitter)
        self.v_y = min(max(self.v_y, -max_move), max_move)
        self.y += self.v_y
        self.y = min(max(self.y, self.target_y - 0.25), self.target_y + 0.25)
        self.node.setPos(self.x, self.y, 0)
        return direct.task.Task.cont
