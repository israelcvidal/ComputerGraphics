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
        glEnable(GL_NORMALIZE)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.5, 0.0, 0.0, 1.0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.7, 0.7, 0.7, 1.0])
        glLightfv(GL_LIGHT0, GL_SPECULAR, [1., 1., 1., 1.0])
        glLightfv(GL_LIGHT0, GL_POSITION, [1.5, 2.9, 2.0, 1.0])

        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.5, 0.0, 0.0, 1.0])
        glEnable(GL_CULL_FACE)
        glFrontFace(GL_CCW)
        glShadeModel(GL_SMOOTH)


    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(30, width / height, 0.5, 100)
        gluLookAt(-1.5,2.,12, 1.5,1.5,0, 0,1,0)


    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        rgb_wall_material = [44/255, 137/255, 142/255]
        wall_material = obj.Material(rgb_wall_material, rgb_wall_material, rgb_wall_material, 1)
        cube = obj.Obj().import_obj('../objects/cube2.obj', wall_material)

        glPointSize(5.0)
        glBegin(GL_POINTS)
        glVertex3f(1.5, 2.9, 2.0)
        glEnd()


        # CHÃO
        glPushMatrix()
        glScalef(3., 0.1, 4.)
        self.draw_polygon(cube)
        glPopMatrix()

        # PAREDE ESQUERDA
        glPushMatrix()
        glTranslatef(0, 1, 0)
        glScalef(0.1, 2., 0.75)
        self.draw_polygon(cube)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(0, 1, 1.75)
        glScalef(0.1, 2., 0.5)
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

        glPushMatrix()
        glTranslatef(0.1, 1., 1.)
        glScalef(0.1, 2., 4.)
        self.draw_polygon(cube)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(5.9, 0., 0.)
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
                glNormal3fv(vertex.normal)
                glVertex3f(vertex.coordinates[0], vertex.coordinates[1], vertex.coordinates[2])
            glEnd()
            '''
            glBegin(GL_LINES)
            for vertex in face.vertices:
                vx = float(vertex.coordinates[0]) + float(vertex.normal[0])
                vy = float(vertex.coordinates[1]) + float(vertex.normal[1])
                vz = float(vertex.coordinates[2]) + float(vertex.normal[2])
                glVertex3f(vertex.coordinates[0], vertex.coordinates[1], vertex.coordinates[2])
                glVertex3f(vx, vy, vz)
            glEnd()'''
            
