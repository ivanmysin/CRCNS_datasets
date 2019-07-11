import numpy as np
import h5py
import os
import pandas as pd
import lib4reading_hc3_dataset as rlib

metadata_path = "/media/ivan/Seagate Backup Plus Drive/Data/Data_from_CRCNS/hc-3/docs/hc3-metadata-tables/"
origin_path = "/media/ivan/Seagate Backup Plus Drive/Data/Data_from_CRCNS/hc-3/ec012ec.11/ec012ec.11/ec012ec.187/"
target_path = "/media/ivan/Seagate Backup Plus Drive/Data/myCRCNC/hc-3/ec012ec.11/ec012ec.187/"


cells, sessions, files, epos = rlib.get_metadata(metadata_path)
topdir = "ec012ec.11"
datadir = "ec012ec.187"


# print(epos.head(10))

# lfp = np.random.rand(8, 500000)
# times = np.random.rand(8, 50000)
# shapes = np.random.rand(8, 500)
# properties = np.random.rand(8, 5000000)

animal_name = epos["animal"][sessions["topdir"] == topdir][0]
if (sum( sessions["session"].where(sessions["topdir"] == topdir).isin([datadir]))  ) :  #
    session_name = datadir



print(animal_name)
print(session_name)


"""
with h5py.File(target_path + 'ec012ec.187.hdf5', 'w') as h5file:
    h5file.attrs["animal"] = animal_name
    h5file.attrs["session"] = session_name
    
    h5file.attrs["familarity_of_environment"] = 10
    h5file.attrs["behavior_test"] = "linear"
    h5file.attrs["duration"] = 100
    h5file.attrs["topdir"] = topdir

    # Тут необходим цикл по электродам
    ele = h5file.create_group('electrode_1')
    ele.attrs['coordinates of electrode'] = 0
    ele.attrs['brain zone'] = 'CA1'
    ele.attrs['layers'] = "channel_1 : alveuls; channel_2 : pyr;" # !!!!!!


    lfp_group = ele.create_group('lfp')
    lfp_group.attrs['fd'] = 1250

    ## Надо сделать цикл по всем каналам !!!!!!!
    lfp_group.create_dataset("channel_1", data = lfp[0, :])

    spikes_group = ele.create_group('spikes')
    spikes_group.attrs["fd"] = 20000

    ## Надо сделать цикл по всем кластерам !!!!!!!
    cluster = spikes_group.create_group("cluster_1")
    cluster.attrs["type"] = "Pyr" # Int or None

    cluster.create_dataset("times", data=times)
    cluster.create_dataset("shapes", data=shapes)
    cluster.create_dataset("properties", data=properties)
"""


