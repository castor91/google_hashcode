#!/usr/bin/env python
import sys

class Grid:
    def __init__(self, R, C):
        self._R = R
        self._C = C


class Car:
    def __init__(self):
        pass


class Ride:
    def __init__(self, a, b, x, y, s, f):
        self._a = a
        self._b = b
        self._x = x
        self._y = y
        self._s = s
        self._f = f

class Game:
    def __init__(self, grid, F):
        self._grid = grid
        self._cars = [Car()] * F
        self._rides = []

    def add_ride(self, ride):
        self._rides.append(ride)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'main.py input_name output_name'
        sys.exit(0)
    input_name = sys.argv[1]
    output_name = sys.argv[2]
    input_file = open(input_name, 'r')
    R, C, F, N, B, T = map(int, input_file.readline().split(' '))
    grid = Grid(R, C)
    game = Game(grid, F)


    for index in xrange(N):
        game.add_ride(Ride(map(int, input_file.readline().split(' '))))

