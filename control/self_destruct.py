import panda3d.core
import direct.task.Task
import direct.task.TaskManagerGlobal

import panda3d_utils

from control import qr_display


class NotePanel:
    def __init__(self, base):
        self.node = base.render.attachNewNode(
            panda3d_utils.make_billboard('note_panel', color=(0.6, 0.6, 0.6)))
        self.node.setScale(0.8, 0.8, 1)
        self.node.setPos(-1.15, -0.5, 1)

    def reveal(self):
        direct.task.TaskManagerGlobal.taskMgr.add(self.move_task, 'move-panel')

    def move_task(self, task):
        current_pos = self.node.getPos()
        next_y = -0.5 - (task.time * 0.5)
        if next_y > -1.5:
            self.node.setPos(current_pos[0], next_y, current_pos[2])
            return direct.task.Task.cont
        else:
            self.node.setPos(current_pos[0], -1.5, current_pos[2])
            return direct.task.Task.done

class SelfDestruct:
    def __init__(self, base):
        self.panel = NotePanel(base)

        self.qr = qr_display.QrDisplay(base)

    def intro(self):
        self.qr.intro()

    def doDestruct(self):
        self.qr.move_qr_out()
        # Play dialog

        self.panel.reveal()
