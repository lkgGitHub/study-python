import csv
import os
import numpy as np
from . import config

def load_data(data_file, usecols):
    with open(data_file, 'r') as cavfile:
        data_reader = csv.DictReader(cavfile)
        for row in data_reader:
            

if __name__ == '__main__':
