import panda3d.core
import direct.showbase.ShowBase

import panda3d_utils

from control import key_events

import html_server_control

def start():
    width = 1280
    height = 720
    ratio = float(width)/height
    panda3d.core.loadPrcFileData('', 'win-size {} {}'.format(width, height))

    base = direct.showbase.ShowBase.ShowBase()

    base.disableMouse()
    base.camera.setPos(0, 0, 3)
    base.camera.lookAt(0, 0, 0)

    lens = panda3d.core.OrthographicLens()
    lens.setFilmSize(2*ratio, 2)
    base.cam.node().setLens(lens)

    panel_texture = \
        base.loader.loadTexture('images/control/control-panel.png')

    panel = base.render.attachNewNode(
        panda3d_utils.make_billboard('panel'))
    panel.setTexture(panel_texture)
    panel.setPos(0, 0, 0)
    panel.setScale(2*ratio, 2, 1)

    k = key_events.KeyEvents(base)

    html_server_control.start(base)

    base.run()

    html_server_earth_base.stop()