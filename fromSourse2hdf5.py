import numpy as np
import h5py
import os


origin_path = "/media/ivan/Seagate Backup Plus Drive/Data/Data_from_CRCNS/hc-3/ec012ec.11/ec012ec.11/ec012ec.187/"

target_path = "/media/ivan/Seagate Backup Plus Drive/Data/myCRCNC/hc-3/ec012ec.11/ec012ec.187/"

# print("Hello!")

lfp = np.random.rand(8, 500000)
times = np.random.rand(8, 50000)
shapes = np.random.rand(8, 500)
properties = np.random.rand(8, 5000000)

with h5py.File(target_path + 'ec012ec.187.hdf5', 'w') as h5file:
    h5file["animal"] = "ec012ec"
    h5file["familarity_of_environment"] = 14
    h5file["behavior_test"] = "linear"
    h5file["duration"] = 100
    h5file["origin_path"] = "hc-3/ec012ec.11/ec012ec.11/ec012ec.187/"

    ele = h5file.create_group('electrode1')
    ele.attrs['coordinates of electrode'] = 0
    ele.attrs['brain zone'] = 'CA1'
    ele.attrs['layers'] = "ch1 : alveuls; ch2 : pyr;" # !!!!!!


    lfp_group = h5file.create_group('lfp')
    lfp_group.attrs['fd'] = 1250

    ## Надо сделать цикл по всем каналам !!!!!!!
    lfp_group.create_dataset("ch1", data = lfp)

    spikes_group = h5file.create_group('spikes')
    spikes_group.attrs["fd"] = 20000

    ## Надо сделать цикл по всем кластерам !!!!!!!
    cluster = spikes_group.create_group("cluster1")
    cluster.attrs["type"] = "Pyr" # Int or None

    cluster.create_dataset("times", data=times)
    cluster.create_dataset("shapes", data=shapes)
    cluster.create_dataset("properties", data=properties)



