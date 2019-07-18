import numpy as np
import matplotlib.pyplot as plt
import h5py

file = "/media/ivan/Seagate Backup Plus Drive/Data/Data_from_CRCNS/hc-3/ec012ec.11/ec012ec.11/ec012ec.187/ec012ec.187.whl"

file = "/media/ivan/Seagate Backup Plus Drive/Data/Data_from_CRCNS/hc-3/docs/additional_whl_files/" + "/".join(file.split("/")[-2:])

print(file)



# import skvideo.io
# file = "/media/ivan/Seagate Backup Plus Drive/Data/Data_from_CRCNS/hc-3/ec012ec.11/ec012ec.11/ec012ec.187/ec012ec.187.m1v"
# videodata = skvideo.io.vread(file)
# print(videodata.shape)

# file = "/media/ivan/Seagate Backup Plus Drive/Data/myCRCNC/hc-3/ec012ec.11/ec012ec.187/ec012ec.187.hdf5"
#
# with h5py.File(file, 'r') as f:
#     lfp = f['electrode_1/lfp/channel_8'][:10000]
#     spike_shapes = f['electrode_1/spikes/cluster_9/spike_shapes'][:]
#
# print(spike_shapes.shape)
# spike_shapes2 = spike_shapes.reshape(-1, 32, 8)
# print(spike_shapes2.shape)
#
# plt.figure()
# plt.plot( spike_shapes2[0, :, :] )
#
# plt.figure()
# plt.plot( spike_shapes[:32, :] )
# plt.show()

#############################################################################################
# sourse_path = "/media/ivan/Seagate Backup Plus Drive/Data/Data_from_CRCNS/hc-3/ec012ec.11/ec012ec.11/ec012ec.187/"
# file = "ec012ec.187.eeg"
#
# lfp = np.fromfile(sourse_path+file, dtype=np.int16)
#
# fd = 1250
#
# t = np.linspace(0, 1000, 1250)
#
# plt.plot(t, lfp[8:1250*33:33])
# plt.show()