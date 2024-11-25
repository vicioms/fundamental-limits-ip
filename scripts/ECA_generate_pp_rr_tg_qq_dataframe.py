import numpy as np
import pandas as pd

import sys
sys.path.append('../modules')
from utils import climate


dir_data = '../data/eca_data/'
stations_pres = climate.eca_read_station_like_file("ECA_blend_station_pp.txt", directory = dir_data)
stations_prec = climate.eca_read_station_like_file("ECA_blend_station_rr.txt", directory = dir_data)
stations_tavg = climate.eca_read_station_like_file("ECA_blend_station_tg.txt", directory = dir_data)
stations_rads = climate.eca_read_station_like_file("ECA_blend_station_qq.txt", directory = dir_data)

stations_dict = {'pp' : stations_pres, 'rr' : stations_prec, 'tg' : stations_tavg, 'qq' : stations_rads}

stations = pd.concat([stations_pres, stations_prec,stations_tavg,stations_rads ]).drop_duplicates().reset_index(drop=True)


dataframes = []
for measure, stations in stations_dict.items():
    for _, row in stations.iterrows():
        if(_ % 500 == 0):
            print(_)
        stat_id = row['STAID']
        filename = "ECA_blend_%s/%s_STAID%06i.txt" % (measure, measure.upper(),stat_id)
        df = climate.eca_read_station_like_file(filename, directory = dir_data)
        df['DATE'] = pd.to_datetime(df['DATE'], format="%Y%m%d")
        df[df == -9999] = np.nan
        df.dropna(axis=0, inplace=True)
        df = df[['STAID', 'DATE', measure.upper()]]
        df.rename({'STAID': 'station_id', 'DATE' : 'date', measure.upper() : 'value' }, axis=1, inplace=True)
        df['measure'] = measure
        df.set_index(['station_id', 'measure', 'date'], drop=True, inplace=True)
        dataframes.append(df)
dataframes = pd.concat(dataframes, axis=0)

dataframes.to_parquet('../data/eca_data/eca_data.parquet', compression='gzip')