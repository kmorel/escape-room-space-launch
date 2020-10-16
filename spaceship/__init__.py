import panda3d.core
import direct.showbase.ShowBase

import panda3d_utils

from spaceship import key_events
from spaceship import launcher

import html_server_spaceship

def start():
    width = 1280
    height = 1024
    ratio = float(width)/height
    panda3d.core.loadPrcFileData('', 'win-size {} {}'.format(width, height))

    base = direct.showbase.ShowBase.ShowBase()

    base.disableMouse()
    base.camera.setPos(0, 0, 3)
    base.camera.lookAt(0, 0, 0)

    lens = panda3d.core.OrthographicLens()
    lens.setFilmSize(2*ratio, 2)
    base.cam.node().setLens(lens)

    l = launcher.Launcher(base)

    k = key_events.KeyEvents(base)

    html_server_spaceship.start(base, l)

    base.run()

    html_server_spaceship.stop()
