import panda3d.core

# You can't normalize inline so this is a helper function
def normalized(*args):
    myVec = panda3d.core.LVector3(*args)
    myVec.normalize()
    return myVec

# Helper function to make a square given the Lower-Left-Hand and
# Upper-Right-Hand corners. Originally written by Kwasi Mensah as
# part of the "Procedural Cube" Panda3D example.
def make_square(x1, y1, z1, x2, y2, z2,
                rgb=(1, 1, 1)):
    format = panda3d.core.GeomVertexFormat.getV3n3cpt2()
    vdata = panda3d.core.GeomVertexData(
        'square', format, panda3d.core.Geom.UHDynamic)

    vertex = panda3d.core.GeomVertexWriter(vdata, 'vertex')
    normal = panda3d.core.GeomVertexWriter(vdata, 'normal')
    color = panda3d.core.GeomVertexWriter(vdata, 'color')
    texcoord = panda3d.core.GeomVertexWriter(vdata, 'texcoord')

    # make sure we draw the sqaure in the right plane
    if x1 != x2:
        vertex.addData3(x1, y1, z1)
        vertex.addData3(x2, y1, z1)
        vertex.addData3(x2, y2, z2)
        vertex.addData3(x1, y2, z2)

        normal.addData3(normalized(2 * x1 - 1, 2 * y1 - 1, 2 * z1 - 1))
        normal.addData3(normalized(2 * x2 - 1, 2 * y1 - 1, 2 * z1 - 1))
        normal.addData3(normalized(2 * x2 - 1, 2 * y2 - 1, 2 * z2 - 1))
        normal.addData3(normalized(2 * x1 - 1, 2 * y2 - 1, 2 * z2 - 1))

    else:
        vertex.addData3(x1, y1, z1)
        vertex.addData3(x2, y2, z1)
        vertex.addData3(x2, y2, z2)
        vertex.addData3(x1, y1, z2)

        normal.addData3(normalized(2 * x1 - 1, 2 * y1 - 1, 2 * z1 - 1))
        normal.addData3(normalized(2 * x2 - 1, 2 * y2 - 1, 2 * z1 - 1))
        normal.addData3(normalized(2 * x2 - 1, 2 * y2 - 1, 2 * z2 - 1))
        normal.addData3(normalized(2 * x1 - 1, 2 * y1 - 1, 2 * z2 - 1))

    # adding different colors to the vertex for visibility
    color.addData4f(rgb[0], rgb[1], rgb[2], 1)
    color.addData4f(rgb[0], rgb[1], rgb[2], 1)
    color.addData4f(rgb[0], rgb[1], rgb[2], 1)
    color.addData4f(rgb[0], rgb[1], rgb[2], 1)

    texcoord.addData2f(0.0, 0.0)
    texcoord.addData2f(1.0, 0.0)
    texcoord.addData2f(1.0, 1.0)
    texcoord.addData2f(0.0, 1.0)

    # Quads aren't directly supported by the Geom interface
    # you might be interested in the CardMaker class if you are
    # interested in rectangle though
    tris = panda3d.core.GeomTriangles(panda3d.core.Geom.UHDynamic)
    tris.addVertices(0, 1, 3)
    tris.addVertices(1, 2, 3)

    square = panda3d.core.Geom(vdata)
    square.addPrimitive(tris)
    return square
