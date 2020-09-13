import panda3d.core
import direct.showbase.ShowBase

import panda3d_utils


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

    background_node = panda3d.core.GeomNode('background')
    background_node.addGeom(panda3d_utils.make_square(-1, -1, 0, 1, 1, 0))

    background_texture = loader.loadTexture('images/earth_base/background.png')

    background = render.attachNewNode(background_node)
    background.setTexture(background_texture)
    background.setPos(panda3d.core.LVector3(0, 0, -1))
    background.setScale(ratio, 1, 1)

    base.run()
