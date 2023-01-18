import numpy as np
from pyglet.gl import *
import pyglet.window
from pyglet import image

class Particle:
    def __init__(self):
        self.position = [0.0, -20.0, 0.0]
        self.velocity = [0.0, 0.0, 0.0]
        self.age = 0.0
        self.original = 0.5
        self.size = self.original
        self.color = [0.0, 0.0, 0.0, 0.0]
        self.lifespan = max(1, np.random.normal(3, 0.4))
        self.VELOCITY = 1

    def update_parameters(self):
        vx = np.array([np.random.normal(0, 100), 20, np.random.normal(0, 100)])
        vx = vx/np.linalg.norm(vx)
        t = (self.lifespan - self.age)/self.lifespan
        self.velocity = vx * self.VELOCITY * t**(-0.5)
        self.position = self.position + self.velocity
        self.size = self.original * t
        t = t**(1/6)
        self.color[0] = t
        self.color[1] = -(1/(t-2))**7
        self.color[2] = (1-t)**2
        self.color[3] = -(t+0.5)**(-15) + 1.2

    def increment_age(self, a):
        self.age += a


class Source:
    def __init__(self):
        self.particles = list()

    def make_particles(self, n):
        for i in range(n):
            self.particles.append(Particle())

    def age_particles(self, a):
        i = len(self.particles) - 1
        while i >= 0:
            self.particles[i].increment_age(a)
            if self.particles[i].age >= self.particles[i].lifespan:
                del self.particles[i]
            i -= 1

    def update_particles(self):
        for p in self.particles:
            p.update_parameters()


width = 1280
height = 720
window = pyglet.window.Window(width, height)

s = Source()

pic = image.load('cestica.bmp')
texture = pic.get_texture()
glEnable(texture.target)
glBindTexture(texture.target, texture.id)

@window.event
def on_draw():
    window.clear()
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width) / height, 0.5, 100.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0, 0, -85.0)

    s.make_particles(10)
    s.update_particles()

    for p in s.particles:
        glBegin(GL_QUADS)
        glColor4f(p.color[0], p.color[1], p.color[2], p.color[3])
        glTexCoord2d(0, 0)
        glVertex3f(p.position[0] - p.size, p.position[1] - p.size, p.position[2])
        glTexCoord2d(0.5, 0)
        glVertex3f(p.position[0] + p.size, p.position[1] - p.size, p.position[2])
        glTexCoord2d(0.5, 0.5)
        glVertex3f(p.position[0] + p.size, p.position[1] + p.size, p.position[2])
        glTexCoord2d(0, 0.5)
        glVertex3f(p.position[0] - p.size, p.position[1] + p.size, p.position[2])
        glEnd()
    glFlush()
    s.age_particles(1/50)


def update_frame(f):
    pass


pyglet.clock.schedule_interval(update_frame, 1 / 50.0)
pyglet.app.run()
