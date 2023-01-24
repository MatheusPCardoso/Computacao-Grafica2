from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from sys import argv
import math
import png

window_name = "Globo" # Nome da tela
local_x_start = -100.0 # Local onde a rotação da esfera comecara (x)
local_y_start = 180.0 # Local onde a rotação da esfera comecara (y)
rotacao = 0.5 # Velocidade de rotacao
background_color = (0, 0, 0, 1)
n1 = 40
n2 = 40 
r = 2 # raio
texture = []

#funcao que setara a textura
def setTextura():
    global texture
    texture = glGenTextures(2)
    reader = png.Reader(filename='mapa.png')
    w, h, pixels, metadata = reader.read_flat()
    if(metadata['alpha']):
        modo = GL_RGBA
    else:
        modo = GL_RGB
    glBindTexture(GL_TEXTURE_2D, texture[0])
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexImage2D(GL_TEXTURE_2D, 0, modo, w, h, 0, modo, GL_UNSIGNED_BYTE, pixels.tolist())
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

# funcao responsavel pelo calculo do plot
def return_L(i,j):
    k = (math.pi*i/(n1-1))-(math.pi/2)
    p = 2*math.pi*j/(n2-1)
    x = r*math.cos(k)*math.cos(p)
    y = r*math.sin(k)
    z = r*math.cos(k)*math.sin(p)
    s = p/(2*math.pi)
    t = (k + math.pi/2)/(math.pi)
    return x,y,z,s,t

# funcao que gera a figura
def figure():
    glPushMatrix()
    glRotatef(local_x_start, 1.0, 1.0, 0.0)
    glRotatef(local_y_start, 0.0, 0.0, 1.0)
    glBindTexture(GL_TEXTURE_2D, texture[0])
    glBegin(GL_QUAD_STRIP)
    for i in range(0,n1): 
        for j in range(0,n2):
            x,y,z,s,t = return_L(i,j)
            glTexCoord2f(s,t)
            glVertex3f(x,y,z)
            x,y,z,s,t = return_L(i+1,j)
            glTexCoord2f(s,t)
            glVertex3f(x,y,z)
    glEnd()  
    glPopMatrix()

# Starta o plot
def plot():
    global local_x_start
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    figure()
    local_x_start = local_x_start + rotacao
    glutSwapBuffers()

def count(i):
    glutPostRedisplay()
    glutTimerFunc(10, count, 1)

#inicio - p
def glCreate():
    glutInit(argv)
    glutInitWindowSize(800, 800)
    glutCreateWindow(window_name)
    glutDisplayFunc(plot)
    setTextura()
    glEnable(GL_MULTISAMPLE)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    gluPerspective(-35, 800 / 800, 0.1, 100.0)
    glTranslatef(0.0, 0.0, -10)
    glutTimerFunc(10, count, 1)
    glutMainLoop()

def main():
    glCreate()

main()