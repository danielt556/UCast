import os
import re

from zipfile import BadZipFile
import numpy as np
import sparse

from config import PATH, SAVE_FILE_NAME, ALL_FIELDS, FIELDS


def save(array, path=PATH, name=SAVE_FILE_NAME):
    """
    Save a numpy matrix/array.
    """
    if not os.path.exists(path):
        os.mkdir(path)
    print(name + str(array.shape) + ".npz")
    point = sparse.COO(array)
    sparse.save_npz(path + "/" + name + str(array.shape) + ".npz", point)


def load_each():
    """
    Load each file that has the name format containing the timestamps.
    """
    files = os.listdir(PATH)
    timestamps = []
    files.sort()
    prog = re.compile(r"20\d{6}\.\d{6}.npz$")
    for file in files:
        if prog.match(file):
            timestamps.append(file)
    # to get in order of timestamps

    data = None
    for ts_idx in range(len(timestamps)):
        print(str(ts_idx + 1) +
              "/" + str(len(timestamps)) +
              " " + timestamps[ts_idx])
        # prints progress
        try:
            record = sparse.load_npz(PATH + "/" + timestamps[ts_idx])
            record = record.todense().astype(np.int16)
            if FIELDS != ALL_FIELDS:
                record = record[:, :, FIELDS]
            #record = sparse.DOK.from_coo(record)
            if ts_idx == 0:
                #data = mx.nd.sparse.zeros('row_sparse', (len(timestamps), *record.shape))
                data = np.zeros((len(timestamps), *record.shape), dtype=np.int16)
                #data = sparse.DOK((len(timestamps), *record.shape))
                #data = sparse.DOK.from_numpy(np.zeros((len(timestamps), *record.shape)))

            data[ts_idx] += record
            # print(data[ts_idx])

#             if data is None:
#                 data = record
#                 data = data.reshape((1, *record.shape))
#             else:
#                 data = np.append(data, record.reshape((1, *record.shape)), axis = 0)
        except BadZipFile as e:
            print(e, file)
    return data


def load_one(path=PATH + "/" + SAVE_FILE_NAME):
    """
    Load the matrix from a single file.
    """
    data = sparse.load_npz(path)
    data = data.todense()
    data = data.astype(np.int16)
    print("Finished loading " + path)
    return data
