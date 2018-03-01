#!/usr/bin/env python3
import sys
import math

def my_distance(a, b, x, y):
    return abs(a - x) + abs(b - y)

class Car:
    def __init__(self, index):
        self._index = index
        self._x = 0
        self._y = 0
        self._rides = []
        self._current_time = 0

    def add_ride(self, ride):
        self._rides.append(ride)

    def __str__(self):
        return '{} {}'.format(len(self._rides), ' '.join(list(map(str, self._rides))))


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

    def distance(self):
        return my_distance(self._a, self._b, self._x, self._y)

    def __str__(self):
        return '{}'.format(self._index)

    def __eq__(self, other):
        return self._index == other._index


class Game:
    def __init__(self, F, T, B):
        self._T = T
        self._B = B
        self._cars = [Car(i) for i in range(F)]
        self._free_rides = []
        self._handled_rides = []

    def add_ride(self, ride):
        self._free_rides.append(ride)

    def alg2(self, ride, car, current_time):
        dist = my_distance(car._x, car._y, ride._a, ride._b)
        flag = 1 if current_time + dist <= ride._s else 0
        #print (((ride.distance() + self._B * flag) / float(dist + 1)))
        wait = max(ride._s - dist - current_time, 0)
        if current_time + dist + wait + ride.distance() >= ride._f: return (-100, 0)
        return ((ride.distance() + self._B * flag) / float(dist + 1), flag)

    def alg3(self, car, current_time):
        ll = [(i, self.alg2(ride, car, current_time)) for i, ride in enumerate(self._free_rides)]
        #print()
        if len(ll) == 0: return None

        return self._free_rides[max(ll, key=lambda x: x[1])[0]]

    def alg1(self, car, current_time):
        ll = [(i, self.alg2(ride, car, current_time)) for i, ride in enumerate(self._free_rides)]
        #print()
        if len(ll) == 0: return None
        if max(ll, key=lambda x: x[1][1]) == 0: return None

        return self._free_rides[max(ll, key=lambda x: x[1])[0]]

    def solve(self):
        for car in self._cars:
            current_time = car._current_time
            while current_time < self._T:
                selected_ride = self.alg1(car, current_time)
                if selected_ride is None:
                    # No bonus
                    break
                ride_distance = selected_ride.distance()
                to_start = my_distance(car._x, car._y, selected_ride._a, selected_ride._b)
                waiting = max(selected_ride._s - to_start - current_time, 0)
                if current_time + to_start + waiting + ride_distance > self._T:
                    break
                car.add_ride(selected_ride)
                self._handled_rides.append(selected_ride)
                self._free_rides.remove(selected_ride) #TODO
                current_time += to_start + waiting + ride_distance
                car._x, car._y = selected_ride._x, selected_ride._y
            print (car._index, current_time)
            car._current_time = current_time

        for car in self._cars[::-1]:
            current_time = car._current_time
            while current_time < self._T:
                selected_ride = self.alg3(car, current_time)
                if selected_ride is None:
                    break
                ride_distance = selected_ride.distance()
                to_start = my_distance(car._x, car._y, selected_ride._a, selected_ride._b)
                waiting = max(selected_ride._s - to_start - current_time, 0)
                if current_time + to_start + waiting + ride_distance > self._T:
                    break
                car.add_ride(selected_ride)
                self._handled_rides.append(selected_ride)
                self._free_rides.remove(selected_ride) #TODO
                current_time += to_start + waiting + ride_distance
                car._x, car._y = selected_ride._x, selected_ride._y
            print (car._index, current_time)

    def __str__(self):
        return 'GAME {}'.format(len(self._cars))


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('main.py input_name output_name')
        sys.exit(0)
    input_name = sys.argv[1]
    output_name = sys.argv[2]
    input_file = open(input_name, 'r')

    R, C, F, N, B, T = map(int, input_file.readline().split(' '))
    game = Game(F, T, B)

    for index in range(N):
        game.add_ride(Ride(index, map(int, input_file.readline().split(' '))))

    input_file.close()

    '''
    print(game)
    for ride in game._free_rides:
        print(ride)
    '''
    game.solve()

    output_file = open(output_name, 'w')

    for car_culo in game._cars:
        output_file.write('{}\n'.format(str(car_culo)))

    output_file.close()

