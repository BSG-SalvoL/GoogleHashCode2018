from .Vettura import *
from .Ride import *
from .threadClass import *
import time


class Map:
    available = 0
    time = 0
    stop = False
    availablethread = None

    def __init__(self, inputstring=""):
        splitted = inputstring.split()
        self.rows = int(splitted[0])
        self.columns = int(splitted[1])
        self.cars_num = int(splitted[2])
        self.rides_num = int(splitted[3])
        self.bonus = int(splitted[4])
        self.stepmax = int(splitted[5])
        self.rides = []
        Ride.MyMap = self
        self.cars = []
        for index in range(self.cars_num):
            self.cars.append(Car())
        Car.MyMap = self
        for car in self.cars:
            car.start_moving()

    def get_cars(self):
        return self.cars

    def get_maxtime(self):
        return self.stepmax

    def load_rides(self, rides=[]):
        for ride in rides:
            splitted = ride.split()
            position = {"SX": int(splitted[0]), "SY": int(splitted[1]), "FX": int(splitted[2]), "FY": int(splitted[3])}
            self.rides.append(Ride(position, int(splitted[4]), int(splitted[5]), rides.index(ride)))
        Map.availablethread = MyThread(0, "Available Thread", self.available_rides)
        Map.availablethread.start()
        return len(self.rides)

    def available_rides(self):
        cont = -1
        while cont != 0:
            cont = 0
            for ride in self.rides:
                if not ride.is_removed():
                    cont += 1
            Map.available = cont
            time.sleep(0.1)
        print("Thread Available Exit Point Reached")

    def propose_rides(self):
        for ride in self.rides:
            ride.startproposing(self.rides.index(ride))

    def accept_rides(self):
        for car in self.cars:
            car.start_ride_selection()

    def increment_time(self):
        Map.time += 1
        if Map.time < self.stepmax:
            return False
        else:
            Map.stop = True
            return True

    def loop(self):
        prev_num = 1
        cont = 0
        self.propose_rides()
        self.accept_rides()
        while Map.available > 0:
            if self.increment_time():
                break
            print("ACTUAL TIME: " + str(Map.time) + " Available Rides: " + str(Map.available))
            if prev_num == Map.available:
                cont += 1
            else:
                cont = 0
            prev_num = Map.available
            if cont > 1000 or prev_num == 0:
                Map.stop = True
                return
        Map.availablethread.join()
