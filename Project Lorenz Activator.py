import random
from random import randint
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
# from pygame import * #this will import everything inside the pygame module
import pygame, sys
import math


# from pygame.locals import *


class Lorenz:
    def __init__(self):  #WAS def __int__(self):
        self.xMin, self.xMax = -30, 30
        self.yMin, self.yMax = -30, 30
        self.zMin, self.zMax = 0, 50
        self.X, self.Y, self.Z = 0.1, 0.0, 0.0
        self.oX, self.oY, self.oZ = self.X, self.Y, self.Z
        self.dt = 0.0001  #WAS 0.01
        self.a, self.b, self.c, = 10, 23, 8 / 3
        self.pixelColor = (255, 0, 0)

    def step(self):
        self.oX, self.oY, self.oZ = self.X, self.Y, self.Z

        # I'm not 100% sure about this, but I'm pretty sure you don't want to use the new X to compute the new Y,
        # and the new X and Y to calculate the new Z.
        self.X = self.oX + (self.dt * self.a * (self.oY - self.oX))  #WAS self.X = self.X + (self.dt * self.a * (self.Y - self.X))
        self.Y = self.oY + (self.dt * (self.oX * (self.b - self.oZ) - self.oY))  #WAS self.Y + (self.dt * (self.X * (self.b - self.Z) - self.Y))
        self.Z = self.oZ + (self.dt * (self.oX * self.oY * self.c - self.oZ))  #WAS self.Z = self.Z + (self.dt * (self.X * self.Y * self.c - self.Z))

    def draw(self, displaySurface):
        width, height = displaySurface.get_size()
        oldPos = self.ConvertToScreen(self.oX, self.oY, self.xMin, self.xMax, self.yMin, self.yMax, width, height)
        newPos = self.ConvertToScreen(self.X, self.Y, self.xMin, self.xMax, self.yMin, self.yMax, width, height)

        # Draw current line segment
        newRect = pygame.draw.line(displaySurface, self.pixelColor, oldPos, newPos, 1)  #WAS thickness= 2

        # Return the bounding rectangle
        return newRect

    def ConvertToScreen(self, x, y, xMin, xMax, yMin, yMax, width, height):
        newX = width * ((x - xMin) / (xMax - xMin))   #WAS newX = width * ((x - xMax) / (xMax - xMin))
        newY = height * ((y - yMin) / (yMax - yMin))  #WAS newY = height * ((y - yMin) / (yMax / yMin))
        return round(newX), round(newY)


class Application:
    def __init__(self):
        self.isRunning = True
        self.displaySurface = None
        self.fpsClock = None
        self.attractors = []
        self.size = self.width, self.height = 1920, 1080
        self.count = 0
        self.outputCount = 1

    # Pygame clock
    def on_init(self):
        pygame.init()
        pygame.display.set_caption('Lorenz Attractor')
        self.displaySurface = pygame.display.set_mode(self.size)
        self.isRunning = True
        self.fpsClock = pygame.time.Clock()

        # Configure the attractor
        color = []
        color.append((51,128,204))
        color.append((255,128,0))
        color.append((255,191,0))
        
        for i in range(0,3):
            self.attractors.append(Lorenz())

            self.attractors[i].X = random.uniform(-0.1,0.1)

            self.attractors[i].pixelColor = color[i]

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.isRunning = False

    # Call the step method for the attractor
    def on_loop(self):

        for x in self.attractors:
            x.step()

    # Draw the attractor
    def on_render(self):
        for x in self.attractors:
            newRect = x.draw(self.displaySurface)
            pygame.display.update(newRect)

    def on_execute(self):
        if self.on_init() == False:
            self.isRunning = False

        while self.isRunning:
            for event in pygame.event.get():
                self.on_event(event)

            self.on_loop()
            self.on_render()

            self.fpsClock.tick()
            self.count += 1

        pygame.quit()


if __name__ == '__main__':  #WAS if __name__ == '_main_':
    t = Application()
    t.on_init()  # ADDED
    t.on_execute()

''' Attempt
    continue 
    attempt
    repeat  '''