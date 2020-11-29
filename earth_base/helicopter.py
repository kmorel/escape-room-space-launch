import panda3d.core
import direct.task.Task
import direct.task.TaskManagerGlobal

import panda3d_utils

import random

class Helicopter:
    def __init__(self, base, background):
        self.background = background

        self.dialogue_before = base.loader.loadSfx(
            'audio/dialogue/heli-crash-1.ogg')
        self.dialogue_during = base.loader.loadSfx(
            'audio/dialogue/heli-crash-2.ogg')
        self.dialogue_after = base.loader.loadSfx(
            'audio/dialogue/heli-crash-3.ogg')

        door_texture = base.loader.loadTexture(
            'images/earth_base/rocket-door.png')
        self.door_pos = (0.8, -.5, 1)
        self.door = base.render.attachNewNode(
            panda3d_utils.make_billboard('rocket-door'))
        self.door.setTexture(door_texture)
        self.door.setTransparency(True)
        self.door.setScale(0.93*0.5, 0.5, 1)
        self.door.setPos(0, 0, -4)

        self.explosion_sound = base.loader.loadSfx('audio/explosion.ogg')

        self.boink = base.loader.loadSfx('audio/boink.ogg')

        wheel_texture = base.loader.loadTexture('images/earth_base/wheel.png')
        self.wheel = base.render.attachNewNode(
            panda3d_utils.make_billboard('wheel'))
        self.wheel.setTexture(wheel_texture)
        self.wheel.setTransparency(True)
        self.wheel.setScale(1.02*0.25, 0.25, 1)
        self.wheel.setPos(0, 0, -4)

    def attack(self):
        self.explosion()

    def explosion(self):
        self.explosion_sound.play()
        direct.task.TaskManagerGlobal.taskMgr.add(
            self.explosion_task, 'explosion')

    def explosion_task(self, task):
        if self.explosion_sound.status() == panda3d.core.AudioSound.PLAYING:
            shake = 0.1
            dx = random.uniform(-shake, shake)
            dy = random.uniform(-shake, shake)
            self.background.setPos(dx, dy, -1)
            self.door.setPos(self.door_pos[0] + dx,
                             self.door_pos[1] + dy,
                             self.door_pos[2])
            return direct.task.Task.cont
        else:
            self.background.setPos(0, 0, -1)
            self.door.setPos(self.door_pos)
            # Start moving the wheel
            self.last_time = 0
            self.vx = -0.01
            self.vy = 0.04
            self.ay = -0.04
            self.wheel.setPos(2, -0.75, 1.5)
            direct.task.TaskManagerGlobal.taskMgr.add(self.wheel_task, 'wheel')
            return direct.task.Task.done

    def wheel_task(self, task):
        current_pos = self.wheel.getPos()
        if current_pos[1] < -0.75:
            self.vy *= -0.75
            current_pos[1] = -0.75
            self.boink.play()
        dt = task.time - self.last_time
        self.last_time = task.time
        self.vy += self.ay * dt
        self.wheel.setPos(current_pos[0] + self.vx,
                          current_pos[1] + self.vy,
                          current_pos[2])
        if current_pos > -2:
            return direct.task.Task.cont
        else:
            self.dialogue_after.play()
            return direct.task.Task.done
