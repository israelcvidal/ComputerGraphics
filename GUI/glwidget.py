from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt5.QtWidgets import QOpenGLWidget
from objectModeling import obj
#from scenario.scenario import

class GLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)


    def initializeGL(self):
        glClearColor(0,0,0,0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

        glLightfv(GL_LIGHT0, GL_AMBIENT, [1., 1., 1.])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1., 1., 1.])
        glLightfv(GL_LIGHT0, GL_SPECULAR, [1., 1., 1.])
        glLightfv(GL_LIGHT0, GL_POSITION, [1.5, 2.9, 2.])

        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [1., 1., 1.])
        glEnable(GL_CULL_FACE)
        glFrontFace(GL_CCW)


    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(30, width / height, 0.5, 10)
        gluLookAt(1.5,1.5,9, 1.5,1.5,0, 0,1,0)


    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        rgb_wall_material = [44/255, 137/255, 142/255]
        wall_material = obj.Material(rgb_wall_material, rgb_wall_material, rgb_wall_material, 1)
        cube = obj.Obj().import_obj('../objects/cube.obj', wall_material)

        # CHÃO
        glPushMatrix()
        glScalef(3., 0.1, 4.)
        self.draw_polygon(cube)
        glPopMatrix()

        # PAREDE ESQUERDA
        glPushMatrix()
        glScalef(0.1, 3., 0.75)
        self.draw_polygon(cube)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(0, 0, 1.75)
        glScalef(0.1, 3., 0.5)
        self.draw_polygon(cube)
        glPopMatrix()

        glPushMatrix()
        glScalef(0.1, 1., 4.)
        self.draw_polygon(cube)
        glPopMatrix()

        # PAREDE DIREITA
        glPushMatrix()
        glTranslatef(2.9, 0., 0.)
        glScalef(0.1, 3., 4.)
        self.draw_polygon(cube)
        glPopMatrix()


    def draw_polygon(self, obj):
        for face in obj.faces:
            glMaterialfv(GL_FRONT, GL_AMBIENT, face.material.k_a_rgb)
            glMaterialfv(GL_FRONT, GL_DIFFUSE, face.material.k_d_rgb)
            glMaterialfv(GL_FRONT, GL_SPECULAR, face.material.k_e_rgb)
            glMaterialf(GL_FRONT, GL_SHININESS, face.material.attenuation)

            glBegin(GL_POLYGON)
            for vertex in face.vertices:
                #glNormal3f(face.normal[0], face.normal[1], face.normal[2])
                glVertex3f(vertex.coordinates[0], vertex.coordinates[1], vertex.coordinates[2])
            glEnd()
