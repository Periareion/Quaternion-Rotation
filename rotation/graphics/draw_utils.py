
from OpenGL.GL import *
from OpenGL.GLU import *

from ..qmath.quaternion import *
from ..qmath.qarray import *

from .color import *

def drop_vertex(position, color):
    glColor3fv(color)
    glVertex3fv(position)

def draw_line(pos1, pos2, color, width=1):
    glLineWidth(GLfloat(width))
    glBegin(GL_LINES)
    drop_vertex(pos1, color)
    drop_vertex(pos2, color) #tuple(x/2 for x in color)
    glEnd()

from copy import copy, deepcopy

class MeshVertices:

    def __init__(self, mesh, parent_position, unit_vectors):
        self.mesh = mesh
        self.QParent = Q(0, *parent_position)
        self.QVertices = []
        for vertex in mesh.QVertices:
            new_vertex = (vertex + mesh.root_position).axis_transform(*unit_vectors) + self.QParent
            self.QVertices.append(new_vertex)

class Polyhedron(MeshVertices):

    def __init__(self, mesh, parent_position=(0,0,0), unit_vectors=deepcopy(UNIT_QUATERNIONS)):
        super().__init__(mesh=mesh, parent_position=parent_position, unit_vectors=unit_vectors)

    def render(self, faces=True, edges=False):

        if faces:
            for face in self.mesh.faces:
                match len(face):
                    case 3: glBegin(GL_TRIANGLES)
                    case 4: glBegin(GL_QUADS)
                    case _: continue

                for vertex_index in face:
                    vertex = self.QVertices[vertex_index]
                    drop_vertex(vertex.vector(), self.mesh.color)
                glEnd()

        if edges:
            for edge in self.mesh.edges:
                vertex1 = self.QVertices[edge[0]].vector()
                vertex2 = self.QVertices[edge[1]].vector()
                draw_line(
                    vertex1,
                    vertex2,
                    Color(200,200,200), 2)

def draw_cube(cube, unit_vectors=deepcopy(UNIT_QUATERNIONS), parent_position=(0,0,0), filled_faces=True):
    QParent = Q(0, *parent_position)
    QVertices = []
    for vertex in cube.QVertices:
        new_vertex = (vertex + cube.root_position).axis_transform(*unit_vectors[0:3]) + QParent
        QVertices.append(new_vertex)

    if filled_faces:
        glBegin(GL_QUADS)
        for face in cube.faces:
            for vertex_index in face:
                vertex = QVertices[vertex_index]
                glColor3fv(cube.color)
                glVertex3fv(vertex.components[1:4])
        glEnd()

    for edge in cube.edges:
        vertex1 = QVertices[edge[0]]
        vertex2 = QVertices[edge[1]]
        draw_line(
            vertex1.components[1:4],
            vertex2.components[1:4],
            Color(200,200,200), 2)
        

quadric = gluNewQuadric()
def draw_sphere(position, color, size):
    glColor3fv(color)
    glPushMatrix()
    glTranslatef(*position)
    gluSphere(quadric, size, 50, 50)
    glPopMatrix()
