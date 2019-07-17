import numpy as np
import h5py
import os
import pandas as pd
import lib4reading_hc3_dataset as rlib
import tarfile

metadata_path = "/media/ivan/Seagate Backup Plus Drive/Data/Data_from_CRCNS/hc-3/docs/hc3-metadata-tables/"
cells, sessions, files, epos = rlib.get_metadata(metadata_path)

origin_path = "/media/ivan/Seagate Backup Plus Drive/Data/Data_from_CRCNS/hc-3/" #  ec012ec.11/ec012ec.11/ec012ec.187/"
target_path = "/media/ivan/Seagate Backup Plus Drive/Data/myCRCNC/hc-3/"  # target_path = "/media/ivan/Seagate Backup Plus Drive/Data/myCRCNC/hc-3/"  #


topdirs = epos["topdir"].unique().tolist()

for topdir in os.listdir(origin_path):
    if not topdir in topdirs:
        print("Continued path %s" % topdir)
        continue

    extract_path = origin_path + topdir + "/"
    for uncompressed_file in os.listdir(extract_path):
        if (uncompressed_file == "." or uncompressed_file==".." or uncompressed_file.find(".gz")==-1):
            continue
        tar = tarfile.open(extract_path + uncompressed_file, mode="r:gz")
        tar.extractall(extract_path)
        tar.close()
        print("Successuly exract archive %s" % uncompressed_file)

        uncompressed_file = uncompressed_file[:-7] # remove ".tar.gz" to get dir with decompressed files
        target_path4session = target_path + topdir + "/" + uncompressed_file
        if not os.path.isdir(target_path4session):
            os.makedirs(target_path4session)
        target_path4session += "/"
        origin_path4session = extract_path + topdir + "/" + uncompressed_file + "/"
        rlib.encode2hdf5(topdir, uncompressed_file, target_path4session, origin_path4session, cells, sessions, files, epos)

    break


