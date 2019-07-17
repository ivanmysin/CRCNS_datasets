import numpy as np
import h5py
import os
import pandas as pd


def get_val_from_xml(xml, teg, isvalint=True):
    val = xml.split(teg)[1][1:-2]
    if isvalint:
        val = int(val)
    return val

def get_channels_in_electrodes(xml):
    electrodes_content = xml.split("channelGroups")[1][1:-2]
    electrodes = []

    for el in electrodes_content.split("group"):
        if el.find("channel") == -1:
            continue

        electrodes.append( [] )

        for ch in el.split("channel"):
            if ch.find("skip") == -1:
                continue
            ch = int(ch[11:-2])
            electrodes[-1].append(ch)

    return electrodes

###########################################################################
def get_data4readingchannels(metadatafile):
    file = open(metadatafile, "r")
    filecontent = file.read()
    file.close()

    metadata = {}
    metadata["nBits"] = get_val_from_xml(filecontent, "nBits")
    metadata["samplingRate"] = get_val_from_xml(filecontent, "samplingRate")
    metadata["voltageRange"] = get_val_from_xml(filecontent, "voltageRange")
    metadata["amplification"] = get_val_from_xml(filecontent, "amplification")
    metadata["lfpSamplingRate"] = get_val_from_xml(filecontent, "lfpSamplingRate")
    metadata["nChannels"] = get_val_from_xml(filecontent, "nChannels")
    metadata["date"] = get_val_from_xml(filecontent, "date", isvalint=False)
    metadata["experimenters"] = get_val_from_xml(filecontent, "experimenters", isvalint=False)

    metadata["channelsInElectrodes"] = get_channels_in_electrodes(filecontent)

    # print(metadata)
    return metadata
###########################################################################
def get_metadata(metadata_path):
    cells_names = ["id", "topdir", "animal", "ele", "clu", "region", "ne", "ni", "eg", "ig", "ed", "ih", "fireRate",
                     "totalFireRate", "type"]
    cells = pd.read_csv(metadata_path + "hc3-cell.csv", names=cells_names)

    sessions_names = ["id", "topdir", "session", "behavior", "fam", "duration"]
    sessions = pd.read_csv(metadata_path + "hc3-session.csv", names=sessions_names)

    files_names = ["topdir", "session", "size", "vtype", "video_size"]
    files = pd.read_csv(metadata_path + "hc3-files.csv", names=files_names)

    epos_names = ["topdir", "animal", "e1", "e2", "e3", "e4", "e5", "e6", "e7", "e8", "e9", "e10", "e11", "e12",
                    "e13", "e14", "e15", "e16"]
    epos = pd.read_csv(metadata_path + "hc3-epos.csv", names=epos_names)

    return cells, sessions, files, epos
##############################################################################
def get_spikes_data(path, ele_idx, nChannelsinElectode):
    ele_idx += 1
    train = np.loadtxt(path + ".res." + str(ele_idx) )
    fets = np.loadtxt(path + ".fet." + str(ele_idx), skiprows=1 )
    clusters_idxs = np.loadtxt(path + ".clu." + str(ele_idx) )

    shapes_data = np.fromfile(path + ".spk." + str(ele_idx), dtype=np.int16)
    sp_shapes = np.zeros((shapes_data.size // nChannelsinElectode, nChannelsinElectode))

    for idx in range(nChannelsinElectode):
        sp_shapes[:, idx] = shapes_data[idx::nChannelsinElectode]

    return train, fets, sp_shapes, clusters_idxs
##########################################################################
def encode2hdf5(topdir, datadir, target_path, origin_path, cells, sessions, files, epos):


    # datadir = "ec012ec.187"

    animal_name = epos["animal"][sessions["topdir"] == topdir][0]
    if (sum( sessions["session"].where(sessions["topdir"] == topdir).isin([datadir]))  ) :
        session_name = datadir

    # print(animal_name)
    # print(session_name)

    with h5py.File(target_path + session_name + '.hdf5', 'w') as h5file:
        h5file.attrs["animal"] = animal_name
        h5file.attrs["session"] = session_name

        h5file.attrs["familarity_of_environment"] = sessions["fam"][sessions["session"] == session_name]
        h5file.attrs["behavior_test"] = sessions["behavior"][sessions["session"] == session_name].values[0]
        h5file.attrs["duration"] = sessions["duration"][sessions["session"] == session_name]
        h5file.attrs["topdir"] = topdir

        metadata4channels = get_data4readingchannels(origin_path + session_name + ".xml")

        h5file.attrs["amplification"] = metadata4channels["amplification"]
        h5file.attrs["nBits"] = metadata4channels["nBits"]
        h5file.attrs["samplingRate"] = metadata4channels["samplingRate"]
        h5file.attrs["experimenters"] = metadata4channels["experimenters"]
        h5file.attrs["voltageRange"] = metadata4channels["voltageRange"]
        h5file.attrs["date"] = metadata4channels["date"]

        n_electrodes = len(metadata4channels["channelsInElectrodes"])
        nChannels = metadata4channels["nChannels"]

        lfp = np.fromfile(origin_path + session_name + ".eeg", dtype=np.int16)

        # Цикл по электродам
        for ele_idx in range(n_electrodes):
            ele = h5file.create_group('electrode_' + str(ele_idx + 1) )
            # ele.attrs['stereotaxicCoordinates'] = 0 # !!!!!!!
            ele.attrs['brainZone'] = epos["e" + str(ele_idx + 1)][epos["topdir"] == topdir].values[0]
            # ele.attrs['layers'] = "channel_1 : alveuls; channel_2 : pyr;" # !!!!!!

            lfp_group = ele.create_group('lfp')
            lfp_group.attrs['lfpSamplingRate'] = metadata4channels["lfpSamplingRate"]

            # Цикл по всем каналам
            for ch_idx in metadata4channels["channelsInElectrodes"][ele_idx]:
                lfp_group.create_dataset("channel_"  + str(ch_idx + 1) , data = lfp[ch_idx::nChannels])

            if (ch_idx == nChannels-1):
                continue

            spikes_group = ele.create_group('spikes')

            nChannelsinElectode = len(metadata4channels["channelsInElectrodes"][ele_idx])
            train, features, spike_shapes, clusters_idxs = get_spikes_data(origin_path + session_name, ele_idx, nChannelsinElectode)

            # По описанию: первое значение в файле .clu. - число кластеров, кладем его в отдельную переменную и удаляем из массива
            n_clusters = int(clusters_idxs[0])
            clusters_idxs = clusters_idxs[1:]

            # Цикл по всем кластерам
            for clu_idx in range(n_clusters):
                cluster = spikes_group.create_group("cluster_" + str(clu_idx+1))
                neuron_type = cells[(cells["topdir"] == topdir)&(cells["ele"] == ele_idx+1)&(cells["clu"] == clu_idx)]["type"].values

                if len(neuron_type) == 0:
                    neuron_type = "n"
                else:
                    neuron_type = neuron_type[0]

                if neuron_type == "p":
                    neuron_type = "Pyr"
                if neuron_type == "i":
                    neuron_type = "Int"
                if neuron_type == "n":
                    neuron_type = "None"

                if clu_idx > 1:
                    cluster.attrs["quality"] = "Nice"
                    cluster.attrs["type"] = neuron_type
                else:
                    cluster.attrs["quality"] = "Bad"
                    cluster.attrs["type"] = "None"

                cluster.create_dataset( "train", data=train[clusters_idxs == clu_idx] )
                spike_shapes_slice = np.repeat(clusters_idxs == clu_idx, 32) # 32 - число отсчетов для сохранения формы импульса
                cluster.create_dataset( "spike_shapes", data=spike_shapes[spike_shapes_slice, :] )
                cluster.create_dataset( "features", data=features[clusters_idxs == clu_idx] )
