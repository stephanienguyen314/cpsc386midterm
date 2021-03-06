# Stephanie Nguyen
# CPSC 386 Section 01
# Midterm - Coding Portion
# 3/18/20
# This .py file is uploaded on github at the following link: stephanienguyen314.github.io

import pygame as pg
from vector import Vector
from laser import Laser


class Ship:
    def __init__(self, game, vector=Vector()):
        self.game = game
        # assuming screen belongs to game class
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.velocity = vector

        # get the image of the ship
        # assume ship image is stored in /images under name 'ship.png'
        self.image = pg.image.load('images/ship.png')
        # get the rect of the ship to make sure the ship stays in the game screen
        self.rect = self.image.get_rect()
        # initially center ship's rect on bottom of screen in the middle
        self.rect.midbottom = self.screen_rect.midbottom
        # store the lasers that the ship will be shooting, in a group
        self.lasers = pg.sprite.Group()

    def center_ship(self):
        # this method is called when the game restarts, to make the ship start again in the center of the bottom
        # of the screen
        self.rect.midbottom = self.screen_rect.midbottom

    def fire(self):
        # assume we have a class called Laser that handles...
        # ...what the laser looks like, its move method, its draw method, and its display method
        laser = Laser(game=self.game)
        # create a new laser object every time the user hits the key in the play loop that
        # will call this method (self.ship.fire())
        # add the newly created laser to the lasers group that is defined in this class's __init__ method
        self.lasers.add(laser)

    def remove_lasers(self):
        # this method remove_laser() will be called when the game restarts and we need to remove all lasers
        self.lasers.remove()

    def move(self):
        # if the velocity vector is 0, then don't move the ship at all and simply exit this method
        if self.velocity == Vector():
            return

        # otherwise, continue to move the ship in whatever the current velocity vector is, which is
        # based on the player's keystrokes
        self.rect.left += self.velocity.x
        self.rect.top += self.velocity.y

        # limits the player's movement so that they must stay on the screen of the game
        self.rect.left = max(0, self.rect.left)
        # assume the game's WIDTH and HEIGHT are stored in the Game class
        self.rect.right = min(self.rect.right, self.game.WIDTH)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(self.rect.bottom, self.game.HEIGHT)

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        # get the current fleet of aliens from the game class
        fleet = self.game.fleet

        self.move()
        self.draw()

        # move each laser in the self.lasers group
        for laser in self.lasers.sprites():
            laser.update()

        # create a copy of the current self.lasers group
        for laser in self.lasers.copy():
            # if the laser has reached the top of the screen, remove it from the self.lasers group so that
            # the group is not infinitely growing with lasers as time goes on
            if laser.rect.bottom <= 0:
                self.lasers.remove(laser)

        # stored as dictionary
        aliens_hit = pg.sprite.groupcollide(fleet.aliens, self.lasers, False, True)

        for alien in aliens_hit:
            alien.hit()
            if alien.health <= 0:
                fleet.aliens.remove(alien)

        # if all aliens from the screen have been destroyed, start new game
        if not fleet.aliens:
            self.game.restart()


class Vector:

    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __repr__(self):
        return "Vector ({}, {})".format(self.x, self.y)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        # utilize the previous defined __add__ method
        return self.__add__(other=(-1 * other))

    # need 2 multiplication methods depending on if coefficient is the first term or the second term
    def __rmul__(self, k: float):
        return Vector(k * self.x, k * self.y)

    def __mul__(self, k: float):
        return self.__rmul__(k=k)

    def __truediv__(self, k: float):
        # division is inverse of multiplication
        return self.__rmul__(1.0 / k)

    def __neg__(self):
        self.x *= -1
        self.y *= -1

    def __eq__(self, other):
        # checks for equality
        return self.x == other.x and self.y == other.y

    @staticmethod
    def test():
        v = Vector(x=5, y=5)
        u = Vector(x=4, y=4)
        print('v is {}'.format(v))
        print('u is {}'.format(u))
        print('uplusv is {}'.format(u + v))
        print('uminusv is {}'.format(u - v))
        print('ku is {}'.format(3 * u))
        print('-u is {}'.format(-1 * u))

def main():
    Vector.test()
