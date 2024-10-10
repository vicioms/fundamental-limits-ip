import pandas as pd
import numpy as np
import re
from datetime import datetime, timedelta
def parse_line_ghcnd(line):
    num_chars_id = 11
    num_chars_year = 4
    num_chars_month = 2
    num_chars_measure = 4
    num_chars_val = 5
    num_chars_bs = 3
    # header part
    id_val = line[:num_chars_id]
    block = line[num_chars_id:]
    year = int(block[:num_chars_year])
    block = block[num_chars_year:]
    month = int(block[:num_chars_month])
    block = block[num_chars_month:]
    measure = block[:num_chars_measure]
    block = block[num_chars_measure:]
    values = []
    
    while(len(block) > 0):
        if(len(values) == 31):
            break
        val = int(block[:num_chars_val])
        if(val == -9999):
            val = np.nan
        block = block[num_chars_val+num_chars_bs:]
        values.append(val)
    return id_val, year, month, measure, values
def populate_dly_ghcnd(filename, station_name, min_year, data_dict):
    try:
        with open(filename) as file:
            lines = file.readlines()
            for line in lines:
                id_val, year,  month, measure, values = parse_line_ghcnd(line)
                if(year < min_year):
                    continue
                num_values = len(values)
                data_dict['station'].extend([station_name]*num_values)
                data_dict['year'].extend([year]*num_values)
                data_dict['month'].extend([month]*num_values)
                data_dict['day'].extend(list(range(1, 1+ num_values)))
                data_dict['measure'].extend([measure]*num_values)
                data_dict['value'].extend(values)

    except Exception as e:
        print(e)

