import pandas as pd
import numpy as np
import csv
import time

FEATURE_COLS = [
    'logged_in','serror_rate','srv_serror_rate','same_srv_rate',
    'dst_host_srv_count','dst_host_same_srv_rate','dst_host_diff_srv_rate',
    'dst_host_same_src_port_rate','dst_host_serror_rate','dst_host_srv_serror_rate'
]

def normal():
    return [1, 0.0, 0.0, 1.0, 0.8, 0.9, 0.1, 0.9, 0.0, 0.0]

def dos():
    return [0, 0.9, 0.9, 0.1, 1.0, 0.1, 0.9, 0.1, 0.9, 0.9]

def probe():
    return [0, 0.5, 0.5, 0.2, 0.5, 0.2, 0.8, 0.2, 0.5, 0.5]

with open('simulation/live_traffic.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(FEATURE_COLS)
    for i in range(200):
        if i % 5 == 0:
            w.writerow(dos())
        elif i % 7 == 0:
            w.writerow(probe())
        else:
            w.writerow(normal())

print("Traffic file generated: simulation/live_traffic.csv")