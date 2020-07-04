from .threadClass import *
import threading
import time


class Car:
    MyMap = None

    def __init__(self):
        self.position = {'X': 0, 'Y': 0}
        self.destination = {'X': 0, 'Y': 0}
        self.in_use = False
        self.usage_time = 0
        self.taken_rides = []
        self.proposals = []

    def get_position(self):
        return self.position

    def is_free(self):
        return not self.in_use

    def get_taken_rides(self):
        return len(self.taken_rides), self.taken_rides

    def set_proposal(self, ride):
        self.proposals.append(ride)

    def start_ride(self, ride):
        self.destination = ride.get_destination()
        self.in_use = True
        ride_start = ride.__getattribute__("stpos")
        self.usage_time = ride.__getattribute__('distance') + ride.calculate_distance(ride_start, self.position)
        self.taken_rides.append(ride.get_index())
        ride.remove()

    def move(self):
        prev_time = -1
        while not Car.MyMap.stop:
            if Car.MyMap.time != prev_time and not self.is_free():
                self.usage_time -= 1
                if self.position['X'] < self.destination['X']:
                    self.position['X'] += 1
                elif self.position['X'] > self.destination['X']:
                    self.position['X'] -= 1
                else:
                    if self.position['Y'] < self.destination['Y']:
                        self.position['Y'] += 1
                    elif self.position['Y'] > self.destination['Y']:
                        self.position['Y'] -= 1
                    else:
                        self.in_use = False
                        self.usage_time = 0
        print("Move Thread Exit Point Reached")

    def print(self, index=0):
        print("Car Index: " + str(index) + " Position: " + str(self.get_position()) + " In Use: " + str(self.in_use))

    def start_moving(self):
        movethread = MyThread(Car.MyMap.get_cars().index(self), "Move Thread", self.move)
        movethread.start()

    def start_ride_selection(self):
        thLock = threading.Lock()
        selectthread = MyThread(0, "Select Thread", self.select_ride, thLock)
        selectthread.start()

    def select_ride(self, threadlock):
        prevtime = -1
        while not Car.MyMap.stop:
            threadlock[0].acquire()
            if self.is_free() and Car.MyMap.time != prevtime and len(self.proposals) > 0:
                self.proposals.sort()
                actual_best = {"Index": 0, "StDistance": 3*Car.MyMap.get_maxtime(), "Attesa": 3*Car.MyMap.get_maxtime()}
                for ride in self.proposals:  # I percorsi che si propongono sono tutti fattibili
                    if ride.is_removed():
                        continue
                    distanza_start = ride.calculate_distance(self.get_position(), ride.get_start())
                    attesa = ride.get_early_time() - (Car.MyMap.time + distanza_start)
                    if distanza_start == 0:  # Se sono già in posizione
                        if attesa == 0:  # Allora devo partire (BEST CASE)
                            print("BEST CASE FOUND ON INDEX: " + str(ride.get_index()))
                            self.start_ride(ride)
                        elif attesa < 0:  # Sono In Ritardo e sono in posizione, parto ma non prenderò bonus
                            print("LATE-InPos FOUND ON INDEX: " + str(ride.get_index()))
                            self.start_ride(ride)
                        else:  # Sono in Anticipo, devo aspettare, c'è un percorso migliore?
                            if distanza_start + abs(attesa) < actual_best['StDistance'] + actual_best['Attesa']:
                                print("Better Ride case 0 FOUND ON INDEX: " + str(ride.get_index()))
                                actual_best['Index'] = self.proposals.index(ride)
                                actual_best['StDistance'] = distanza_start
                                actual_best['Attesa'] = abs(attesa)
                    else:  # Non sono in posizione
                        if distanza_start + abs(attesa) < actual_best['StDistance'] + actual_best['Attesa']:
                            print("Better Ride case 1 FOUND ON INDEX: " + str(ride.get_index()))
                            actual_best['Index'] = self.proposals.index(ride)
                            actual_best['StDistance'] = distanza_start
                            actual_best['Attesa'] = abs(attesa)
                if len(self.proposals) > 0 and not self.proposals[actual_best['Index']].is_removed():
                    print("Starting BEST INDEX: " + str(actual_best['Index']))
                    self.start_ride(self.proposals[actual_best['Index']])
                self.proposals.clear()
            threadlock[0].release()
            time.sleep(0.01)