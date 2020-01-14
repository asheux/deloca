"""
Imports
"""
import re
import time
import datetime
import sys
from process_data import VehicleRouting, ht
from two_opt import TwoOptimal
from read_csv import read_file

MATRIX = list(read_file('data/distance_data.csv'))
# Creating instances
P = VehicleRouting()
T = TwoOptimal(MATRIX)


def display(address, t, status):
    """
    this function creates the display to simulate a qui alternative
    """
    addr_size = len('195 W Oakland Ave')
    t_size = len('11:00:00')
    lt = len(t)
    # create paddings
    if lt < t_size:
        tl = t_size - lt
        t += " " * tl
    if len(address) > addr_size:
        address = address[:addr_size]
    elif len(address) < addr_size:
        l = len(address)
        d = addr_size - l
        address += " " * d
    matrix = [
        [
            '+--------------------------------------------------------------------+'
        ],
        [f'|      {address}          |  {t}     |   {status}      |'],
    ]
    ds = ""

    # Display the matrix
    for r in matrix:
        for i in range(len(r)):
            ds += r[i]
        ds += '\n'
    return ds


def for_matrix(m):
    """
    matrix helper fuction
    """
    for i in m:
        for j in i:
            print(j)


def print_mileage(mileage):
    m = [[
        '                     +----------------------------+                   '
    ],
         [
             f'                     |   MILEAGE = {mileage} MILES    |                   '
         ],
         [
             '                     +----------------------------+                   '
         ]]
    for_matrix(m)


def start_simulation():
    """
    The simulation function to handle the simulation of deliveries
    """
    tours = [
        P.find_tour(P.f_truck),
        P.find_tour(P.s_truck),
        P.find_tour(P.s_trip)
    ]
    trucks = [P.f_truck, P.s_truck, P.s_trip]
    mileage = 0
    print('\n')
    print(
        '+-----------------------WELCOME TO THE FUTURE------------------------+'
    )
    # I need to iterate over the list of trucks information
    # to be able to simulate them one by one
    for index, tour in enumerate(tours):
        T.find_best_path(tour)
        P.set_delivery_time(T.best_route, trucks[index])
        truck_number = index + 1
        print('\n')
        print(
            f'+-------------------------------TRUCK {truck_number}------------------------------+'
        )
        i = 0
        # update each row with info based on the delivery
        for delivery in P.tour_info:
            t = delivery['DeliveredAt']
            address = delivery['DeliverTo'][1]
            status = delivery['Status']
            sys.stdout.write(display(address, t, status))
            sys.stdout.flush()
            time.sleep(
                1
            )  # show a delivery made after 1 second to immitate how a real time delivery system would only that the delay in real time would be the time difference between delivery
            i += 1
        route_distance = round(T.best_route['Best Path']['cost'], 1)
        mileage += route_distance
        print(
            '+--------------------------------------------------------------------+'
        )
        print(
            f'+                |   COST or DISTANCE = {route_distance} MILES    |              +'
        )
        print(
            '+--------------------------------------------------------------------+'
        )
        print('\n')
    print_mileage(mileage)


def check_time(time_input):
    """
    checks if time the user inputs in within the constrains
    and converts it to delta time
    """
    message = 'Invalid time input!'
    l = len(time_input)
    if l == 11 or l == 10:
        print(message)
        exit()
    if l == 5 or l == 4:
        print(message)
        exit()
    h, m, _ = time_input.split(
        ':'
    )  # unpack the time user inputs (8:19:12) to get hours(8), minutes(19) and seconds(12)
    delta_time = datetime.timedelta(hours=int(h), minutes=int(m))
    return delta_time


def display_packages(p):
    """
    print a table containing the information of the packages
    """
    addr_size = len('195 W Oakland Ave')
    t_size = len('11:00:00')
    pid = p["DeliverTo"][0]
    addr = p["DeliverTo"][1]
    dl = p["DeliverTo"][5]
    city = p["DeliverTo"][2]
    zcode = p["DeliverTo"][4]
    s = p["Status"]
    lt = len(dl)

    # this is to help with padding
    if lt < t_size:
        tl = t_size - lt
        dl += " " * tl
    if len(pid) < 2:
        k = 2 - len(pid)
        pid += " " * k
    if len(city) < addr_size + 1:
        l = len(city)
        d = (addr_size + 1) - l
        city += " " * d
    if len(s) < 10:
        l = len(s)
        d = 10 - l
        s += " " * d
    if len(addr) > addr_size:
        addr = addr[:addr_size]
    elif len(addr) < addr_size:
        l = len(addr)
        d = addr_size - l
        addr += " " * d
    m = [[
        '+-----------------------------------------------------------------------------------------------+'
    ], [
        f'|  {pid}    |   {addr}  |  {dl}   |  {city}  |  {zcode}   |  {s}   |'
    ]]
    for_matrix(m)


def pretty_print(p):
    n = 20
    m = [['+-------------------------------------------------+'],
         ['|          NAME          |          VALUE          '],
         ['+-------------------------------------------------+'],
         [f'| Delivery Address       |  {p["DeliverTo"][1]}    '],
         [f'+-------------------------------------------------+'],
         [f'| Delivery Deadline      |  {p["DeliverTo"][5]}    '],
         [f'+-------------------------------------------------+'],
         [f'| Delivery City          |  {p["DeliverTo"][2]}    '],
         [f'+-------------------------------------------------+'],
         [f'| Delivery Zip Code      |  {p["DeliverTo"][4]}    '],
         [f'+-------------------------------------------------+'],
         [f'| Delivery Status        |  {p["Status"]}          '],
         ['+-------------------------------------------------+']]

    for_matrix(m)


def time_lookup():
    """
    perform look up by time
    """
    t = input('\nEnter time in format (hh:mm) to check, e.g, (8:12): ')
    if not t:
        exit()
    t += ':00'
    print(
        '+-----------------------------------------------------------------------------------------------+'
    )
    print(
        '|  Pk    |   Address            |  Deadline   |  City                |  ZipCode |   Status      |'
    )
    for count in range(1, len(ht.array) + 1):
        look_function(str(count), t, display_packages)
    print(
        '+-----------------------------------------------------------------------------------------------+'
    )


def package_lookup():
    """
    A lookup function to find the status of the package
    on its delivery
    """
    pk = input('\nEnter package id to look up (int): ')
    if not pk:
        exit()
    if not re.match('^[0-9]*$', pk):
        print(f'\nInvalid package id {pk}')
    elif int(pk) > len(ht.array):
        print(f'\nNo package with the provided id {int(pk)}')
    elif int(pk) <= 0:
        print('\nPackage id should not be less than 1')
    else:
        user_time = input(
            '\nEnter time in formant (hh:mm) to check e.g (8:12): ')
        if not user_time:
            exit()
        user_time += ':00'
        look_function(pk, user_time, pretty_print)


def look_function(pk, user_time, callback):
    """
    this look up function checks the specified package and updates
    it based on the time user specifies
    """
    package_info = ht.get(pk)  # look up in a hash table for pk as the key
    start_time = check_time(package_info['DeliveryStart'])
    delivery_time = check_time(package_info['DeliveredAt'])
    u_time = check_time(user_time)

    # compare user time with the start time of the delivery and the delivery time
    # and display accordingly
    if u_time <= start_time:
        package_info['Status'] = 'At Hub'
        callback(package_info)
    if u_time > start_time and u_time < delivery_time:
        package_info['Status'] = 'On the way'
        callback(package_info)
    if u_time >= delivery_time:
        callback(package_info)


def manitor_trip():
    """
    This is just a function to handle manual look up if
    the user decides not to choose simulation
    """
    tours = [
        P.find_tour(P.f_truck),
        P.find_tour(P.s_truck),
        P.find_tour(P.s_trip)
    ]
    trucks = [P.f_truck, P.s_truck, P.s_trip]
    for index, tour in enumerate(tours):
        T.find_best_path(tour)
        P.set_delivery_time(T.best_route, trucks[index])
    print('\nMonitoring...\n\nKeys:\n')
    print('\t(time): to lookup by time\n\t(pk): to lookup by package id\n')

    query = input('Please enter key to perform: ')
    while query != 'q' or not query:
        if query == 'pk':
            package_lookup()
        elif query == 'time':
            time_lookup()
        else:
            exit()
            print('Invalid key: please provide a valid key')


def print_welcome_note():
    print(
        '\nWELCOME TO DeLoca, A ROUTING SYSTEM THAT GIVES YOU THE BEST DELIVERY ROUTE!\n'
    )


def main():
    print_welcome_note()
    quiz = input(
        'Type "lookup" for package lookup or any key for simulation: ')
    quiz = quiz.lower()
    if quiz == 'lookup':
        manitor_trip()
    else:
        start_simulation()


if __name__ == '__main__':
    main()
