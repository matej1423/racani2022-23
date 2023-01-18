import math
import numpy as np
from pyglet.gl import *
import pyglet.window

control_points = list()

with open("spiral.txt") as file:
    for line in file:
        elems = line.split()
        control_points.append((float(elems[0]), float(elems[1]), float(elems[2])))

n_segments = len(control_points) - 3
points = list()
tangent_vectors = list()
tangents = list()
M = np.array([[-1, 3, -3, 1], [3, -6, 3, 0], [-3, 0, 3, 0], [1, 4, 1, 0]])
Mt = np.array([[-1, 3, -3, 1], [2, -4, 2, 0], [-1, 0, 1, 0]])

for i in range(n_segments):
    r = np.array([control_points[i], control_points[i+1], control_points[i+2], control_points[i+3]])
    t = 0.0
    while t < 1.0:
        T = np.array([math.pow(t, 3), math.pow(t, 2), math.pow(t, 1), 1])/6
        points.append(list(np.dot(np.dot(T, M), r)))

        T = np.array([math.pow(t, 2), math.pow(t, 1), 1]) / 2
        tangent_vectors.append(list(np.dot(np.dot(T, Mt), r)))
        t += 0.01

    tangents.append(points[100*i+50])

    x = points[100*i+50][0] + tangent_vectors[100*i+50][0]/3
    y = points[100*i+50][1] + tangent_vectors[100*i+50][1]/3
    z = points[100*i+50][2] + tangent_vectors[100*i+50][2]/3

    tangents.append([x, y, z])

V = list()
F = list()
center = [0, 0, 0]

with open("bird.obj") as file:
    for line in file:
        line = line.strip()
        if line == "":
            continue
        elems = line.split()
        if elems[0] == "f":
            F.append((int(elems[1]) - 1, int(elems[2]) - 1, int(elems[3]) - 1))
        if elems[0] == "v":
            V.append((3*float(elems[1]), 3*float(elems[2]), 3*float(elems[3])))
            center[0] += float(elems[1])
            center[1] += float(elems[2])
            center[2] += float(elems[3])

center[0] /= len(V)
center[1] /= len(V)
center[2] /= len(V)

width = 1280
height = 720
window = pyglet.window.Window(width, height)

time = 0

@window.event
def on_draw():
    window.clear()
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width) / height, 0.5, 100.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(-5, -5, -65.0)

    glBegin(GL_LINE_STRIP)
    for i in range(0, 100*n_segments, 2):
        glColor3f(1, 1, 1)
        glVertex3f(points[i][0], points[i][1], points[i][2])
        glVertex3f(points[i + 1][0], points[i + 1][1], points[i + 1][2])
    glEnd()

    glBegin(GL_LINES)
    for i in range(0, 2*n_segments, 2):
        glColor3f(1, 0, 0)
        glVertex3f(tangents[i][0], tangents[i][1], tangents[i][2])
        glVertex3f(tangents[i + 1][0], tangents[i + 1][1], tangents[i + 1][2])
    glEnd()

    global time
    glTranslatef(points[time][0], points[time][1], points[time][2])

    s = [0, 0, 1]
    e = tangent_vectors[time]

    os = np.cross(s, e)
    fi = math.degrees(math.acos(np.dot(s, e)/(np.linalg.norm(s)*np.linalg.norm(e))))

    glRotatef(fi, os[0], os[1], os[2])

    glBegin(GL_TRIANGLES)
    for i in range(len(F)):
        glColor3f(0, 0, 1)
        polygon = F[i]
        v1 = V[polygon[0]]
        v2 = V[polygon[1]]
        v3 = V[polygon[2]]

        glVertex3f(v1[0], v1[1], v1[2])
        #glVertex3f(v2[0], v2[1], v2[2])

        glVertex3f(v2[0], v2[1], v2[2])
        #glVertex3f(v3[0], v3[1], v3[2])

        glVertex3f(v3[0], v3[1], v3[2])
        #glVertex3f(v1[0], v1[1], v1[2])

    glEnd()

    time += 1
    if time == n_segments * 100 - 1:
        time = 0

    glFlush()


def update_frame(f):
    pass


pyglet.clock.schedule_interval(update_frame, 1 / 50.0)
pyglet.app.run()
