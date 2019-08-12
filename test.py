import os
import numpy as np
import lib4reading_hc3_dataset as rlib
import matplotlib.pyplot as plt

nChannelsinElectode = 8

spike_shapes_path = "/media/ivan/Seagate Backup Plus Drive/Data/Data_from_CRCNS/hc-3/ec014.n329/ec014.n329/2007-3-29_12-11-20/2007-3-29_12-11-20.spk.4"
shapes_data = np.fromfile(spike_shapes_path, dtype=np.int16)

sp_shapes = np.zeros((shapes_data.size // nChannelsinElectode, nChannelsinElectode))

for idx in range(nChannelsinElectode):
    sp_shapes[:, idx] = shapes_data[idx::nChannelsinElectode]

plt.plot(sp_shapes[:32, :])
plt.show()


# metadata_path = "/media/ivan/Seagate Backup Plus Drive/Data/Data_from_CRCNS/hc-3/docs/hc3-metadata-tables/"
# cells, sessions, metafiles, epos = rlib.get_metadata(metadata_path)
#
#
# channelorderspath = "/media/ivan/Seagate Backup Plus Drive/Data/Data_from_CRCNS/hc-3/docs/channelorder/"
#
# channelorders = rlib.gelRipMaxPos(channelorderspath, epos, metafiles)
#
#
#
# print(channelorders)

# import numpy as np
# import matplotlib.pyplot as plt
# import h5py




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