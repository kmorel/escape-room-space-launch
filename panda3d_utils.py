import panda3d.core

# Makes a square parallel to the x/y plane from -1 to 1 in the
# x and y directions. A Panda3D GeomNode of the given name is
# returned. The square can be resized and scaled to the proper
# location. Texture coordinates are added to paste on an image.
def make_billboard(name, color=(1, 1, 1)):
    vertex_format = panda3d.core.GeomVertexFormat.getV3n3cpt2()
    vdata = panda3d.core.GeomVertexData(
        'square', vertex_format, panda3d.core.Geom.UHDynamic)

    v = panda3d.core.GeomVertexWriter(vdata, 'vertex')
    v.addData3(-1, -1, 0)
    v.addData3( 1, -1, 0)
    v.addData3( 1,  1, 0)
    v.addData3(-1,  1, 0)

    n = panda3d.core.GeomVertexWriter(vdata, 'normal')
    n.addData3(0, 0, 1)
    n.addData3(0, 0, 1)
    n.addData3(0, 0, 1)
    n.addData3(0, 0, 1)

    c = panda3d.core.GeomVertexWriter(vdata, 'color')
    c.addData4(color[0], color[1], color[2], 1)
    c.addData4(color[0], color[1], color[2], 1)
    c.addData4(color[0], color[1], color[2], 1)
    c.addData4(color[0], color[1], color[2], 1)

    t = panda3d.core.GeomVertexWriter(vdata, 'texcoord')
    t.addData2f(0.0, 0.0)
    t.addData2f(1.0, 0.0)
    t.addData2f(1.0, 1.0)
    t.addData2f(0.0, 1.0)

    tris = panda3d.core.GeomTriangles(panda3d.core.Geom.UHDynamic)
    tris.addVertices(0, 1, 3)
    tris.addVertices(1, 2, 3)

    square_geom = panda3d.core.Geom(vdata)
    square_geom.addPrimitive(tris)

    square_node = panda3d.core.GeomNode(name)
    square_node.addGeom(square_geom)
    return square_node

