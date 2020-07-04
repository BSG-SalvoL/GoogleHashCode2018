from .threadClass import *
import time


class Ride:
    MyMap = None

    def __init__(self, position, earlystart, maxtime, index):
        self.stpos = {}
        self.stpos['X'] = position['SX']
        self.stpos['Y'] = position['SY']
        self.finpos = {}
        self.finpos['X'] = position['FX']
        self.finpos['Y'] = position['FY']
        self.earlystart = earlystart
        self.maxtime = maxtime
        self.distance = Ride.calculate_distance(self.stpos, self.finpos)
        self.priority = self.distance + 3*self.maxtime
        self.removed = False
        self.index = index

    def __lt__(self, other):
        return self.priority < other.priority

    def print(self):
        print("INDEX: " + str(self.index) + " Distanza: " + str(self.distance) + " " + str(self.stpos) +
              " " + str(self.finpos) + " " + str(self.earlystart) + " " + str(self.maxtime))

    @staticmethod
    def calculate_distance(pos_a, pos_b):
        return abs(pos_a.get('X') - pos_b.get('X')) + abs(pos_a.get('Y') - pos_b.get('Y'))

    def get_priority(self):
        return self.priority

    def is_removed(self):
        return self.removed

    def get_index(self):
        return self.index

    def is_possible(self, car_pos, actualtime):
        car_dist = self.calculate_distance(car_pos, self.stpos)
        if self.distance + car_dist >= self.maxtime-actualtime:
            return False
        else:
            return True

    def propose_to_cars(self):
        while Ride.MyMap is None:
            time.sleep(0.01)
        prevtime = -1
        while not Ride.MyMap.stop:
            if prevtime != Ride.MyMap.time:
                for car in Ride.MyMap.get_cars():
                    if car.is_free() and self.is_possible(car.get_position(), Ride.MyMap.time):
                        car.set_proposal(self)
            prevtime = Ride.MyMap.time
            time.sleep(0.2)
        print("Propose Thread Exit Point Reached")

    def startproposing(self, index):
        proposethread = MyThread(index, "Propose Thread", self.propose_to_cars)
        proposethread.start()

    def remove(self):
        self.removed = True

    def get_max_time(self):
        return self.maxtime

    def get_early_time(self):
        return self.earlystart

    def get_destination(self):
        return self.finpos

    def get_start(self):
        return self.stpos
