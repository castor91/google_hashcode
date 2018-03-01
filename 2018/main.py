#!/usr/bin/env python
import sys

class Grid:
    def __init__(self, R, C):
        self._R = R
        self._C = C

    def __str__(self):
        return 'GRID {} {}'.format(R, C)

class Car:
    def __init__(self):
        self._rides = []


class Ride:
    def __init__(self, index, vals):
        a, b, x, y, s, f = vals
        self._index = index
        self._a = a
        self._b = b
        self._x = x
        self._y = y
        self._s = s
        self._f = f

    def __str__(self):
        return 'RIDE {} {} {} {} {} {} {}'.format(self._index, self._a, self._b, self._x, self._y, self._s, self._f)

class Game:
    def __init__(self, grid, F):
        self._grid = grid
        self._cars = [Car()] * F
        self._rides = []

    def add_ride(self, ride):
        self._rides.append(ride)

    def solve(self):
        pass

    def __str__(self):
        return 'GAME {}'.format(len(self._cars))


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
        game.add_ride(Ride(index, map(int, input_file.readline().split(' '))))

    input_file.close()

    print grid
    print game
    for ride in game._rides:
        print ride

    game.solve()

    output_file = open(output_name, 'w')

    for i in xrange(len(game._cars)):
        car = game._cars[i]
        output_file.write('{}\n'.format(i, ' '.join(car._rides)))

    output_file.close()

