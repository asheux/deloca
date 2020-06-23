import datetime
from typing import List, Dict
from read_csv import read_file
from two_opt import TwoOptimal
from hashmap import HashTable

ht = HashTable()  # instantiate a hash table


class ProcessData:
    s_trip: List = []
    s_truck: List = []
    f_truck: List = []

    def __init__(self):
        self.packages = read_file('data/package_data.csv')
        self.package_list = list(self.packages)
        self.set_package_info()

    def set_package_info(self):
        """
        some information may need to be added manually
        """
        for row in self.package_list:
            package_info = {}
            package_info['Status'] = 'At Hub'
            package_info['DeliverTo'] = [row[i] for i in range(len(row))]
            package_info['DeliveryStart'] = ''

            notes = package_info["DeliverTo"][7]
            p = package_info['DeliverTo']
            self.load_trucks(p, notes, package_info)
            ht.insert_hash(package_info['DeliverTo'][0],
                           package_info)  # make use of the hash table

    def load_trucks(self, p, notes, package_info):
        """
        load trucks data from a csv file
        """
        if p[0] == '19':
            self.f_truck.append(package_info)
        if p[5] != 'EOD':
            if notes.startswith('Must') or notes == 'None':
                self.f_truck.append(package_info)
        else:
            if p[4] == '84104':
                self.s_trip.append(package_info)
        if notes.startswith('Wrong'):
            p[1], p[4] = '410 S State St.', '84111'
            self.s_trip.append(package_info)
        if notes.startswith('Delayed') or notes.startswith('Can'):
            self.s_truck.append(package_info)
        if package_info not in [*self.f_truck, *self.s_trip,
                                *self.s_truck]:  # list concatenation
            if len(self.s_truck) < len(self.s_trip):
                self.s_truck.append(package_info)
            else:
                self.s_trip.append(package_info)


class VehicleRouting(ProcessData):
    time_data: List = []
    tour_info: Dict = {}

    def __init__(self):
        super().__init__()
        # set the starting time for each truck
        self.set_deliver_start('8:00:00', self.f_truck)
        self.set_deliver_start('8:00:00', self.s_truck)
        self.set_deliver_start('11:00:00', self.s_trip)
        self.city_names = read_file('data/streetnames.csv')

    def find_tour(self, delivery: list) -> list:
        """
        generate an initial tour from the preprocessed data
        
        Paramater
        ---------
        delivery; list
            list of all the delivery to be made
            including the time
        """
        initial_tour = []
        for x in delivery:
            for y in self.city_names:
                if x['DeliverTo'][1] == y[2]:
                    initial_tour.append(int(y[0]))
        return initial_tour

    def set_deliver_start(self, start_time, delivery: list):
        for _, value in enumerate(delivery):
            value['DeliveryStart'] = start_time  # set the start time

    def set_tour_info(self, tour):
        self.tour_info = tour  # update tour information with current info
        for item in tour:
            key = item['DeliverTo'][0]
            ht.insert_hash(key, item)  # make use of the hash table to data

    def set_delivery_time(self, path, tour):
        n = len(tour)
        h, m, s = tour[0]['DeliveryStart'].split(':')
        start_time = datetime.timedelta(hours=int(h),
                                        minutes=int(m),
                                        seconds=int(s))
        self.time_data.append(
            str(start_time))  # make sure the time data list has the start time
        for i in range(n):
            tt = self.total_time(path, i)
            tour[i]['DeliveredAt'] = str(tt)
            tour[i]['Status'] = 'Delivered'
        self.set_tour_info(tour)
        self.time_data[:] = []  # empty the list of the next truck

    def total_time(self, path: Dict, i: int):
        """
        calculate time for each delivery

        Paramaters
        ----------
        path, i; Dict, int
            path is the best route
            i is the index
        """
        total_time = datetime.timedelta()
        delivery_times = path['Best Path']['time_list']
        if i < len(delivery_times):
            self.time_data.append(delivery_times[i])
        for t in self.time_data:
            hr, mn, sc = t.split(':')
            delta = datetime.timedelta(hours=int(hr),
                                       minutes=int(mn),
                                       seconds=int(sc))
            total_time += delta
        return total_time
