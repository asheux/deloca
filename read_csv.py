import csv

def read_file(filename):
    with open(filename) as f:
        reader = csv.reader(f, delimiter=',')
        reader_list = list(reader)

    return reader_list

