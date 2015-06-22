import pygame
from random import choice
from pygame import draw, key, locals
from math import pi, cos, sin

from ball import Ball

PLAYER_SIZE = 24
ACC = 1
DENSITY = 0.25

class Player(Ball):
    
    def __init__(self, world, position):
        self.world = world
        self.color = choice(world.COLORS)
        self.acceleration = ACC
        self.maxChain = 3
        self.baseMass = PLAYER_SIZE / DENSITY
        
        self.chain = 0
        self.baseChainAngle = 0
        
        super(Player, self).__init__(world, position = position, mass = self.baseMass,
                                     color = self.color, density = DENSITY)
        
    def draw(self, surface):
        super(Player, self).draw(surface)
        
        angle = self.baseChainAngle
        radius = self.mass * self.density
        for i in range(self.chain):
            x = self.position[0] + cos(angle) * radius * 2
            y = self.position[1] + sin(angle) * radius * 2
            size = radius / 4
            draw.ellipse(
                surface,
                self.color,
                [x - size, y - size, size * 2, size * 2]
            )
            angle += pi * 2 / self.chain
            angle %= pi * 2
    
    def update(self):
        # get input
        keys = key.get_pressed()
        
        # move based in key input
        if keys[pygame.K_LEFT]:
            self.applyForce([ -self.acceleration, 0 ])
        if keys[pygame.K_RIGHT]:
            self.applyForce([ self.acceleration, 0 ])
        if keys[pygame.K_UP]:
            self.applyForce([ 0, -self.acceleration ])
        if keys[pygame.K_DOWN]:
            self.applyForce([ 0, self.acceleration ])
        
        # update position
        super(Player, self).update()
        
        # rotate score chain
        self.baseChainAngle = (self.baseChainAngle + pi / 512) % (pi * 2)
    
    def score(self, ball):
        if self.color == ball.color:
            self.chain += 1
            if self.chain > self.maxChain:
                self.mass = self.baseMass
                self.chain = 0
                self.maxChain += 1
            else:
                self.mass += ball.mass
        else:
            self.mass = self.baseMass
            self.chain = 0
            self.color = ball.color