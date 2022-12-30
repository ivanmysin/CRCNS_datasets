import numpy as np
import h5py
import os
import pandas as pd
import shutil


def gelRipMaxPos(channelorderspath, epos, metafiles):
    channelorders = []

    for file in sorted(os.listdir(channelorderspath)):

        if file.find("RipMaxPosi.txt") == -1:
            continue

        animal_name = file.split(".")[0]

        # print(epos["animal"].isin([animal_name]).sum())
        if epos["animal"].isin([animal_name]).sum().astype(np.bool):
            diaposon = file.split(".")[1]
            diaposon_min, diaposon_max = diaposon.split("_")

            diaposon_min = int(diaposon_min)
            diaposon_max = int(diaposon_max)

            for metafile in metafiles["session"].values:

                animal_sess = metafile.split(".")
                if len(animal_sess) != 2:
                    continue
                animal = animal_sess[0]
                sess = int(animal_sess[1])
                if (animal == animal_name and sess >= diaposon_min and sess <= diaposon_max):

                    chor = {
                        "animal": animal_name,
                        "session": metafile,
                        "shanks": [],
                        "recording_cite": [],
                    }

                    ripposfile = open(channelorderspath + file, "r")

                    for ripposline in ripposfile.readlines():
                        shank, reccite = ripposline.split("\t")

                        chor["shanks"].append(int(shank))
                        chor["recording_cite"].append(int(reccite))

                    ripposfile.close()

                    channelorders.append(chor)
    return channelorders





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
            # print(ch[10:-2])
            ch = int( ch.split(">")[1].split("<")[0] )
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

    metadata["nSamples"] = get_val_from_xml(filecontent, "nSamples")
    metadata["peakSampleIndex"] = get_val_from_xml(filecontent, "peakSampleIndex")
    # print(metadata["nSamples"],  metadata["peakSampleIndex"])
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
    try:
        train = np.loadtxt(path + ".res." + str(ele_idx) )
        fets = np.loadtxt(path + ".fet." + str(ele_idx), skiprows=1 )
        clusters_idxs = np.loadtxt(path + ".clu." + str(ele_idx) )
        shapes_data = np.fromfile(path + ".spk." + str(ele_idx), dtype=np.int16)
       
    except OSError:
        train = np.empty(0)
        fets = np.empty(0)
        clusters_idxs = np.empty(0)
        sp_shapes = np.empty(0)
        
    try:
        sp_shapes = np.zeros((shapes_data.size // nChannelsinElectode, nChannelsinElectode), dtype=np.int16)
        for idx in range(nChannelsinElectode):
            sp_shapes[:, idx] = shapes_data[idx::nChannelsinElectode]
    except ValueError:
        sp_shapes = np.zeros(shape=(shapes_data.size//nChannelsinElectode+2, nChannelsinElectode), dtype=np.int16)
        for idx in range(nChannelsinElectode):
            sp_tmp = shapes_data[idx::nChannelsinElectode]
            sp_shapes[:len(sp_tmp), idx] = sp_tmp
        
    return train, fets, sp_shapes, clusters_idxs
##########################################################################
def copy_video_file(origin_path, session_name, target_path):
    video_file = origin_path + session_name + ".m1v"
    if os.path.isfile(video_file):
        shutil.copy(video_file, target_path, follow_symlinks=True)

    video_file = origin_path + session_name + ".mpg"
    if os.path.isfile(video_file):
        shutil.copy(video_file, target_path, follow_symlinks=True)

##########################################################################
def encode2hdf5(topdir, datadir, target_path, origin_path, cells, sessions, files, epos, additional_whl_files_path, channelorders):
    animal_name = epos["animal"][epos["topdir"] == topdir].values[0]

    if (sum( sessions["session"].where(sessions["topdir"] == topdir).isin([datadir]))  ) :
        session_name = datadir

    shanks = []
    for chor in channelorders:
        if (chor["animal"] == animal_name and chor["session"] == session_name):
            shanks = chor["shanks"]
            recording_cite = chor["recording_cite"]


    # if os.path.isfile(target_path + session_name + '.hdf5'):
    #     return

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

        animalPosition = h5file.create_group('animalPosition')
        animalPositionFile = origin_path + session_name + ".whl"
        animalCoordinates = None
        if (os.path.isfile(animalPositionFile)):
            animalCoordinates = np.loadtxt(animalPositionFile)
        else:
            animalPositionFile = additional_whl_files_path + "/".join(animalPositionFile.split("/")[-2:])
            if (os.path.isfile(animalPositionFile)):
                animalCoordinates = np.loadtxt(animalPositionFile)

        if not animalCoordinates is None:
            animalPosition.create_dataset("xOfFirstLed", data=animalCoordinates[:, 0])
            animalPosition.create_dataset("yOfFirstLed", data=animalCoordinates[:, 1])
            animalPosition.create_dataset("xOfSecondLed", data=animalCoordinates[:, 2])
            animalPosition.create_dataset("yOfSecondLed", data=animalCoordinates[:, 3])
            animalPosition.attrs["coordinatesSampleRate"] = 39.06  # данные взяты из описания к hc-2 набору данных
        else:
            print("No file with data of aninaml position!")


        copy_video_file(origin_path, session_name, target_path)


        n_electrodes = len(metadata4channels["channelsInElectrodes"])
        nChannels = metadata4channels["nChannels"]
        nSamples = metadata4channels["nSamples"]
        peakSampleIndex = metadata4channels["peakSampleIndex"]

        lfp = np.fromfile(origin_path + session_name + ".eeg", dtype=np.int16)

        ch_idx_4lfp_indexing = 0
        # Цикл по электродам
        for ele_idx in range(n_electrodes):
            ele = h5file.create_group('electrode_' + str(ele_idx + 1) )
            # ele.attrs['stereotaxicCoordinates'] = 0 # !!!!!!!
            brainZone = epos["e" + str(ele_idx + 1)][epos["topdir"] == topdir].values[0]
            ele.attrs['brainZone'] = epos["e" + str(ele_idx + 1)][epos["topdir"] == topdir].values[0]

            lfp_group = ele.create_group('lfp')
            lfp_group.attrs['lfpSamplingRate'] = metadata4channels["lfpSamplingRate"]

            # Цикл по всем каналам
            for ch_idx in metadata4channels["channelsInElectrodes"][ele_idx]:
                lfp_group.create_dataset("channel_"  + str(ch_idx + 1), data = lfp[ch_idx_4lfp_indexing::nChannels])
                ch_idx_4lfp_indexing += 1

                if len(shanks) > 0:
                    for sh in shanks:
                        if sh == ele_idx + 1:
                            for rec in recording_cite:
                                if ch_idx_4lfp_indexing == rec:
                                    #  + sh + 1
                                    # print(brainZone, sh, ch_idx_4lfp_indexing)
                                    # if not pyramidal_layer_index is None:
                                    ele.attrs['pyramidal_layer'] = 1

            if (ch_idx == nChannels-1):
                continue

            spikes_group = ele.create_group('spikes')

            nChannelsinElectode = len(metadata4channels["channelsInElectrodes"][ele_idx])

            try:
                train, features, spike_shapes, clusters_idxs = get_spikes_data(origin_path + session_name, ele_idx, nChannelsinElectode)
            except FileNotFoundError:
                continue
            # По описанию: первое значение в файле .clu. - число кластеров, кладем его в отдельную переменную и удаляем из массива
            if train.size == 0 or clusters_idxs.size==0:
                continue
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

                cluster.attrs["peakSampleIndex"] = peakSampleIndex
                cluster.create_dataset( "train", data=train[clusters_idxs == clu_idx] )
                spike_shapes_slice = np.repeat(clusters_idxs == clu_idx, nSamples) # nSamples - число отсчетов для сохранения формы импульса

                # print(spike_shapes.shape, spike_shapes_slice.shape)
                try:
                    cluster.create_dataset( "spike_shapes", data=spike_shapes[spike_shapes_slice, :].reshape(-1, nSamples, nChannelsinElectode) )
                except IndexError:
                    pass
                cluster.create_dataset( "features", data=features[clusters_idxs == clu_idx] )
