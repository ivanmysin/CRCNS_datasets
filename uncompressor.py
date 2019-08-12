import os
import tarfile

origin_path = "/media/ivan/Seagate Backup Plus Drive/Data/Data_from_CRCNS/hc-3/"

fails_to_uncpmressed = open(origin_path + "fails_to_uncpmressed2.txt", "w")



for root, dirs, files in sorted(os.walk(origin_path)):

    for file in files:
        if file.find(".gz")==-1:
            continue

        try:
            tar = tarfile.open(root + "/" + file, mode="r:gz")
            tar.extractall(root)
            tar.close()
            print("Successuly exract archive %s" % root + "/" + file)
        except:
            fails_to_uncpmressed.write(root + "/" + file + "\n")

fails_to_uncpmressed.close()

