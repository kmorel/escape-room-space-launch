import panda3d.core
import direct.showbase.ShowBase

import panda3d_utils

from earth_base import key_events
from earth_base import shipping_container

import html_server_earth_base

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

    background_texture = \
        base.loader.loadTexture('images/earth_base/background.png')

    background = base.render.attachNewNode(
        panda3d_utils.make_billboard('background'))
    background.setTexture(background_texture)
    background.setPos(0, 0, -1)
    background.setScale(2*ratio, 2, 1)

    container_stacks = shipping_container.ContainerStacks(base)

    k = key_events.KeyEvents(base, container_stacks)

    html_server_earth_base.start(base, container_stacks)

    base.run()

    html_server_earth_base.stop()
