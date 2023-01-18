from pyglet.gl import *
from pyglet.window import *
import math
import numpy as np

obj_v = []
obj_f = []

kontrolne_tocke = []  # kontrolne tocke krivulje
centar = [0.0, 0.0, 0.0]

with open("spiral.txt", 'r') as obj:
    dataRead = obj.read()
    linije = dataRead.splitlines()
    for linija in linije:
        jednaLinija = linija.split()
        if len(jednaLinija) > 0:
            kontrolne_tocke.append(
                [int(float(jednaLinija[0])), int(float(jednaLinija[1])), int(float(jednaLinija[2]))])

fileName = "bird.obj"
with open(fileName, 'r') as obj:
    data = obj.read()
    linije = data.splitlines()

    for linija in linije:
        jednaLinija = linija.split()
        if jednaLinija[0] == "f":
            obj_f.append((int(jednaLinija[1]) - 1, int(jednaLinija[2]) - 1, int(jednaLinija[3]) - 1))
        if jednaLinija[0] == "v":
            obj_v.append((float(jednaLinija[1]), float(jednaLinija[2]), float(jednaLinija[3])))
            centar[0] += float(jednaLinija[1])
            centar[1] += float(jednaLinija[2])
            centar[2] += float(jednaLinija[3])
            
centar[0] /= len(obj_v)
centar[1] /= len(obj_v)
centar[2] /= len(obj_v)

brSeg = len(kontrolne_tocke) - 3

tocke_krivulje = []
vektori_tangente = []  # vektori smjera tangenti

tangente = []  # tangente koje crtamo

for i in range(brSeg):
    v1 = kontrolne_tocke[i]
    v2 = kontrolne_tocke[i + 1]
    v3 = kontrolne_tocke[i + 2]
    v4 = kontrolne_tocke[i + 3]

    t = 0
    while t < 1.0:
        f1 = (-pow(t, 3.0) + 3 * pow(t, 2.0) - 3 * t + 1) / 6.0
        f2 = (3 * pow(t, 3.0) - 6 * pow(t, 2.0) + 0 + 4) / 6.0
        f3 = (-3 * pow(t, 3.0) + 3 * pow(t, 2.0) + 3 * t + 1) / 6.0
        f4 = (pow(t, 3.0)) / 6.0

        tocke_krivulje.append(np.dot([f1,f2,f3,f4], [v1,v2,v3,v4]))

        t1 = (-pow(t, 2.0) + 2 * t - 1) / 2.0
        t2 = (3 * pow(t, 2.0) - 4 * t + 0) / 2.0
        t3 = (-3 * pow(t, 2.0) + 2 * t + 1) / 2.0
        t4 = (pow(t, 2.0)) / 2.0

        vektori_tangente.append(np.dot([t1,t2,t3,t4], [v1,v2,v3,v4]))
        t += 0.01

    tangente.append(tocke_krivulje[100 * i + 25])

    x = tocke_krivulje[100 * i + 25][0] + vektori_tangente[100 * i + 25][0] * 1 / 3
    y = tocke_krivulje[100 * i + 25][1] + vektori_tangente[100 * i + 25][1] * 1 / 3
    z = tocke_krivulje[100 * i + 25][2] + vektori_tangente[100 * i + 25][2] * 1 / 3
    tangente.append([x, y, z])

    tangente.append(tocke_krivulje[100 * i + 75])
    x = tocke_krivulje[100 * i + 75][0] + vektori_tangente[100 * i + 75][0] * 1 / 3
    y = tocke_krivulje[100 * i + 75][1] + vektori_tangente[100 * i + 75][1] * 1 / 3
    z = tocke_krivulje[100 * i + 75][2] + vektori_tangente[100 * i + 75][2] * 1 / 3
    tangente.append([x, y, z])


window = pyglet.window.Window(width=800, height=700, caption='1. laboratorijska vjezba', resizable=True)
brojac = 0


@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(-6.0, -6.0, -60.0)

    global brojac

    glBegin(GL_LINE_STRIP)
    for i in range(0, 100 * brSeg, 2):
        glColor3f(0, 0, 0)
        glVertex3f(tocke_krivulje[i][0], tocke_krivulje[i][1], tocke_krivulje[i][2])
        glVertex3f(tocke_krivulje[i + 1][0], tocke_krivulje[i + 1][1], tocke_krivulje[i + 1][2])
    glEnd()

    glBegin(GL_LINES)
    for i in range(0, 4 * brSeg, 2):
        glColor3f(0, 1, 0)
        glVertex3f(tangente[i][0], tangente[i][1], tangente[i][2])
        glVertex3f(tangente[i + 1][0], tangente[i + 1][1], tangente[i + 1][2])
    glEnd()

    glTranslatef(tocke_krivulje[brojac][0], tocke_krivulje[brojac][1], tocke_krivulje[brojac][2])

    s = [0.0, 0.0, 1.0]
    e = vektori_tangente[brojac]

    os = np.cross(s,e)
    se = np.dot(s,e)
    kut = math.degrees(math.acos(se / (np.linalg.norm(s) * np.linalg.norm(e))))

    glRotatef(kut, os[0], os[1], os[2])
    glTranslatef(-centar[0], -centar[1], -centar[2])
    glColor3f(1, 0, 0)
    glBegin(GL_LINES)
    for i in range(len(obj_f)):
        polygon = obj_f[i]
        v1 = obj_v[polygon[0]]
        v2 = obj_v[polygon[1]]
        v3 = obj_v[polygon[2]]

        glVertex3f(v1[0], v1[1], v1[2])
        glVertex3f(v2[0], v2[1], v2[2])

        glVertex3f(v2[0], v2[1], v2[2])
        glVertex3f(v3[0], v3[1], v3[2])

        glVertex3f(v3[0], v3[1], v3[2])
        glVertex3f(v1[0], v1[1], v1[2])

    glEnd()

    if brojac != (100 * brSeg - 1):
        brojac += 1
    else:
        brojac = 0

    glFlush()


@window.event
def on_resize(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(gl.GL_PROJECTION)
    glLoadIdentity()
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    gluPerspective(45.0, float(width) / height, 0.5, 100.0)
    glColor3f(0, 0, 1)
    glMatrixMode(GL_MODELVIEW)
    return pyglet.event.EVENT_HANDLED


def update_frame(f):
    pass


pyglet.clock.schedule_interval(update_frame, 1 / 50.0)
pyglet.app.run()