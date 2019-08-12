import numpy as np
import h5py
import os
import pandas as pd
import lib4reading_hc3_dataset as rlib
import tarfile

metadata_path = "/media/ivan/Seagate Backup Plus Drive/Data/Data_from_CRCNS/hc-3/docs/hc3-metadata-tables/"
cells, sessions, files, epos = rlib.get_metadata(metadata_path)

channelorderspath = "/media/ivan/Seagate Backup Plus Drive/Data/Data_from_CRCNS/hc-3/docs/channelorder/"

channelorders = rlib.gelRipMaxPos(channelorderspath, epos, files)

# print(channelorders)

# animal_name = epos["animal"][epos["topdir"] == "ec012ec.12"].values[0]


origin_path = "/media/ivan/Seagate Backup Plus Drive/Data/Data_from_CRCNS/hc-3/" #  ec012ec.11/ec012ec.11/ec012ec.187/"
target_path = "/media/ivan/Seagate Backup Plus Drive/Data/myCRCNC/hc-3/"  # target_path = "/media/ivan/Seagate Backup Plus Drive/Data/myCRCNC/hc-3/"  #
additional_whl_files_path = "/media/ivan/Seagate Backup Plus Drive/Data/Data_from_CRCNS/hc-3/docs/additional_whl_files/"

topdirs = epos["topdir"].unique().tolist()

MYCOUNTER = 1
for topdir in sorted( os.listdir(origin_path) ):
    if not topdir in topdirs:
        print("Continued path %s" % topdir)
        continue

    extract_path = origin_path + topdir + "/"
    for uncompressed_file in sorted( os.listdir(extract_path) ):
        if (uncompressed_file == "." or uncompressed_file==".." or uncompressed_file.find(".gz")==-1):
            continue
        if uncompressed_file.find(".mpg") != -1:
             continue
        # if not os.path.isfile(extract_path + topdir + "/" + uncompressed_file[:-7] + "/" + uncompressed_file[:-7] + ".eeg"):
        #     tar = tarfile.open(extract_path + uncompressed_file, mode="r:gz")
        #     tar.extractall(extract_path)
        #     tar.close()
        #     print("Successuly exract archive %s" % uncompressed_file)



        uncompressed_file = uncompressed_file[:-7] # remove ".tar.gz" to get dir with decompressed files
        target_path4session = target_path + topdir + "/" + uncompressed_file
        if not os.path.isdir(target_path4session):
            os.makedirs(target_path4session)
        target_path4session += "/"
        origin_path4session = extract_path + topdir + "/" + uncompressed_file + "/"

        print(MYCOUNTER, topdir + "/" + uncompressed_file)

        if MYCOUNTER > 362:
            rlib.encode2hdf5(topdir, uncompressed_file, target_path4session, origin_path4session, cells, sessions, files, epos, additional_whl_files_path, channelorders)
        MYCOUNTER += 1


