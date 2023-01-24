from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from math import *
import sys
import math

# Calcula a normal do prisma
def calculaNormal(a,b,c):
    x = 0
    y = 1
    z = 2
    v0 = a
    v1 = b
    v2 = c
    U = ( v2[x]-v0[x], v2[y]-v0[y], v2[z]-v0[z] )
    V = ( v1[x]-v0[x], v1[y]-v0[y], v1[z]-v0[z] )
    N = ( ((U[y]*V[z])-(U[z]*V[y])),((U[z]*V[x])-(U[x]*V[z])),((U[x]*V[y])-(U[y]*V[x])))
    NLength = sqrt((N[x]*N[x])+(N[y]*N[y])+(N[z]*N[z]))
    return ( N[x]/NLength, N[y]/NLength, N[z]/NLength)


def prisma():
    # Especificacoes do prisma #
    raio = 2
    N = 13
    H = 4
    pontosBase = []
    pontosTampa = []
    angulo = (2*math.pi)/N
    ####### ------------ ######

    # Adiciona na pilha de matriz atual
    glPushMatrix()
    # Multiplica a matriz atual por uma matriz de tradução.
    glTranslatef(0,-1,0)
    # Multiplica a matriz atual por uma matriz de rotação.
    glRotatef(-110,1.0,0.0,0.0)

    # Cria a base
    glBegin(GL_POLYGON)
    for i in range(N):
        x1 = raio * math.cos(i*angulo)
        y1 = raio * math.sin(i*angulo)
        pontosBase += [ (x1,y1) ]
        glVertex3f(x1,y1,0.0)
    a2 = (pontosBase[0][0],pontosBase[0][1],0.0)
    b2 = (pontosBase[1][0],pontosBase[1][1],0.0)
    c2 = (pontosBase[2][0],pontosBase[2][1],0.0)
    glNormal3fv(calculaNormal(a2,b2,c2))
    glEnd()

    # Cria a tampa
    glBegin(GL_POLYGON)
    for i in range(N):
        x2 = raio * math.cos(i*angulo)
        y2 = raio * math.sin(i*angulo)
        pontosTampa += [ (x2,y2) ]
        glVertex3f(x2,y2,H)
    a1 = (pontosTampa[0][0],pontosTampa[0][1],H)
    b1 = (pontosTampa[1][0],pontosTampa[1][1],H)
    c1 = (pontosTampa[2][0],pontosTampa[2][1],H)
    glNormal3fv(calculaNormal(a1,b1,c1))
    glEnd()

    # Cria a lateral
    glBegin(GL_QUADS)
    for i in range(N): 
        a = (pontosBase[i][0],pontosBase[i][1],H)
        b = (pontosBase[i][0],pontosBase[i][1],0.0)
        c = (pontosBase[(i+1)%N][0],pontosBase[(i+1)%N][1],0.0)
        d = (pontosBase[(i+1)%N][0],pontosBase[(i+1)%N][1],H)
        glNormal3fv(calculaNormal(a,b,d))
        glVertex3fv(a)
        glVertex3fv(b)
        glVertex3fv(c)
        glVertex3fv(d)
    glEnd()
    # Retira da pilha
    glPopMatrix()

def display():
    # Limpa a janela e o depth buffer.
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
	# Multiplica a matriz atual por uma matriz (2,1,3,0) de rotação.
    glRotatef(2,1,3,0)
    # Renderizam um prisma.
    prisma()
    # Troca os buffers da janela atual se o buffer for duplo.
    glutSwapBuffers()

def timer(i):
    # Marca a janela atual para ser exibida novamente.
    glutPostRedisplay()
	# Registra um retorno de chamada de timer para ser acionado em um número especificado de milissegundos.
    glutTimerFunc(50,timer,1)

def shape(w,h):
    # Define visor
	glViewport(0,0,w,h)
	# Aplica operações de matriz subsequentes à pilha da matriz de projeção.
	glMatrixMode(GL_PROJECTION)
	# Substitui a matriz atual pela matriz de identidade.
	glLoadIdentity()
	# Configura uma matriz de projeção de perspectiva.
	gluPerspective(45,float(w)/float(h),0.1,50.0)
	# Aplica operações de matriz subsequentes à pilha de matriz de visão de modelo.
	glMatrixMode(GL_MODELVIEW)
	# Substitui a matriz atual pela matriz de identidade.
	glLoadIdentity()
	# Define uma transformação de exibição.
	gluLookAt(0,1,10,0,0,0,0,1,0)

def init():
    ### Declaracao das variaveis ###
    diffuse = (1.0, 1.0, 1.0, 1.0)
    specular = (1.0, 1.5, 1.5, 1.0)
    shininess = (60,)
    position = (10, 0, 0)
    ######### ------------ #########

    # Especifica que a cor de fundo da janela será preta.
    glClearColor(0.0,0.0,0.0,0.0)
    #glShadeModel(GL_FLAT)
    glShadeModel(GL_SMOOTH)

    # Especifica a intensidade RGBA difusa da luz.
    glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuse)
	# Especifica a intensidade RGBA especular da luz.
    glMaterialfv(GL_FRONT, GL_SPECULAR, specular)
	# Especifica o expoente especular RGBA do material.
    glMaterialfv(GL_FRONT, GL_SHININESS, shininess)
	# Especificam a posição da luz nas coordenadas homogêneas do objeto.
    glLightfv(GL_LIGHT0, GL_POSITION, position)

    # Habilitando recursos #
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_MULTISAMPLE)
	###### ---------- ######

def glutStart():
    glutInit(sys.argv)
	# Define o modo de exibição inicial.
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | 
						GLUT_DEPTH | GLUT_MULTISAMPLE)
	# Define o tamanho da janela.
    glutInitWindowSize(1000,800)
	# Define o nome da janela.
    glutCreateWindow("Prisma Iluminada")
	# Define o retorno de chamada de remodelagem para a janela atual.
    glutReshapeFunc(shape)
	# Define o retorno de chamada de exibição para a janela atual.
    glutDisplayFunc(display)
	# Registra um retorno de chamada de timer para ser acionado em um número especificado de milissegundos.
    glutTimerFunc(50,timer,1)

def main():
    # Chama a funcao glut.
    glutStart()
    # Chamada da funcao init.
    init()
    # Entra no loop de processamento de eventos GLUT.
    glutMainLoop()

main()
