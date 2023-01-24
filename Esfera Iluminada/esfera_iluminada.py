######## IMPORTS ########
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys
######## ------- ########

def display():
	# Limpa a janela e o depth buffer.
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
	# Multiplica a matriz atual por uma matriz (2,1,3,0) de rotação.
    glRotatef(2,1,3,0)
	# Renderizam uma esfera sólida.
    glutSolidSphere(3,50,50)
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
	###### Declaracao das variaveis ######
	diffuse = (4.0, 0.0, 5.0, 1.0)
	specular = (4.0, 4.0, 4.0, 1.0)
	shininess = (60,)
	position = (100.0, 500.0, 400.0, 1.0)
	############ ------------ ############
	
	# Especifica que a cor de fundo da janela será preta.
	glClearColor(0.0,0.0,0.0,0.0)
	# Representa uma técnica de sombreamento. (GL_FLAT e GL_SMOOTH)
	glShadeModel(GL_FLAT)

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
	glutCreateWindow("Esfera Iluminada")
	# Define o retorno de chamada de remodelagem para a janela atual.
	glutReshapeFunc(shape)
	# Define o retorno de chamada de exibição para a janela atual.
	glutDisplayFunc(display)
	# Registra um retorno de chamada de timer para ser acionado em um número especificado de milissegundos.
	glutTimerFunc(50,timer,1)

def main():
	# Chama a funcao glut
	glutStart()
	# Chamada da funcao init.
	init()
	# Entra no loop de processamento de eventos GLUT.
	glutMainLoop()

main()
