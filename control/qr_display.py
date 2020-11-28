import panda3d.core
import direct.task.Task
import direct.task.TaskManagerGlobal

import panda3d_utils

import qrcode
import io

def get_ip():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

class QrDisplay:
    def __init__(self, base):
        self.window_pos = (1.265, -0.49, -1)

        self.node = base.render.attachNewNode(
            panda3d_utils.make_billboard('qr'))
        self.node.setScale(0.8, 0.8, 1)
        self.node.setPos(
            self.window_pos[0], self.window_pos[1], self.window_pos[2])

        self.set_qr_texture('intro')

        # Replace with actual dialogue sound
        self.intro_dialogue = base.loader.loadSfx('audio/hydraulic-lift.ogg')

    def set_qr_texture(self, page):
        url = 'http://' + get_ip() + ':5000/' + page

        image_data = qrcode.make(url, box_size=100)
        image_buffer = io.BytesIO()
        image_data.save(image_buffer)
        image_buffer.seek(0)

        pnm = panda3d.core.PNMImage()
        pnm.read(panda3d.core.StringStream(image_buffer.getvalue()))

        texture = panda3d.core.Texture()
        texture.load(pnm)
        self.node.setTexture(texture)

    def move_qr_out(self):
        direct.task.TaskManagerGlobal.taskMgr.add(self.move_out_task, 'move-qr')

    def move_out_task(self, task):
        next_x = self.window_pos[0] + (task.time * 0.5)
        if next_x < self.window_pos[0] + 1:
            self.node.setPos(next_x, self.window_pos[1], self.window_pos[2])
            return direct.task.Task.cont
        else:
            self.node.setPos(self.window_pos[0] + (task.time * 0.5),
                             self.window_pos[1],
                             self.window_pos[2])
            return direct.task.Task.done

    def move_qr_in(self):
        direct.task.TaskManagerGlobal.taskMgr.add(self.move_in_task, 'move-qr')

    def move_in_task(self, task):
        next_x = self.window_pos[0] + (task.time * 0.5) - 1
        if next_x < self.window_pos[0]:
            self.node.setPos(next_x, self.window_pos[1], self.window_pos[2])
            return direct.task.Task.cont
        else:
            self.node.setPos(
                self.window_pos[0], self.window_pos[1], self.window_pos[2])
            return direct.task.Task.done

    def intro(self):
        self.move_qr_out()
        panda3d_utils.play_then_run(
            self.intro_dialogue, self.show_self_destruct_qr)

    def show_self_destruct_qr(self):
            self.set_qr_texture('self-destruct-button')
            self.move_qr_in()
