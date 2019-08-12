import numpy as np
import matplotlib.pyplot as plt
# import h5py

sourse_path =  "/media/ivan/Seagate Backup Plus Drive/Data/Data_from_CRCNS/hc-3/ec014.n329/ec014.n329/2007-3-29_12-11-20/"   # "/media/ivan/Seagate Backup Plus Drive/Data/Data_from_CRCNS/hc-3/ec012ec.11/ec012ec.11/ec012ec.187/"


# path = "/home/ivan/Data/Data from CRCNS/hc-3/ec012ec.11/ec012ec.11/ec012ec.187/"
# file = "ec012ec.187.eeg"

file = "2007-3-29_12-11-20"
ele_idx = 4


data = np.fromfile(sourse_path + file + ".spk." + str(ele_idx), dtype=np.int16)

train = np.loadtxt(sourse_path + file + ".res." + str(ele_idx))
fets = np.loadtxt(sourse_path + file + ".fet." + str(ele_idx), skiprows=1)
clusters_idxs = np.loadtxt(sourse_path + file + ".clu." + str(ele_idx))

print(data.size/8/54)
print(train.size)
print(fets.shape)
print(clusters_idxs.size)

# data = data[0:32*8] # for neuron 1
## data = data.reshape(-1, 32)

sp_shape = np.zeros((data.size//8, 8))

for idx in range(8):
    # sp_shape = data[idx::33]
    sp_shape[:, idx] = data[idx::8]





# print(sp_shape.size%32)
#fd = 1250
#ch1 = data[8::33]
#t = np.linspace(0, ch1.size/fd, ch1.size)
#
#
#plt.plot(t, ch1)
##plt.xlim(0, 0.5)
#plt.show()

# sp_shape = sp_shape[np.ones(4329216, dtype=np.bool), :] # sp_shape[0:32, :]

plt.plot(sp_shape[:64])
##plt.xlim(0, 0.5)
plt.show()
