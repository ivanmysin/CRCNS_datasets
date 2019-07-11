import numpy as np
import h5py
import os
import pandas as pd


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