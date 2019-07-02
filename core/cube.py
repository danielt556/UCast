import numpy as np
from core.config import PATH
import core.fileHandler as fh


class Cube():
    def __init__(self, date, clean, data, datafolder=PATH, datatype=".npz"):
        self.data = data
        self.shape = data.shape
        self.date = date
        self.timestamps = self.shape[0]
        self.x = self.shape[1]
        self.y = self.shape[2]
        self.feats = self.shape[3]
        self.clean = clean
        self.datatype = datatype
        self.datapath = datafolder + "/" + self.get_file_name() + self.datatype

    def refresh_path(self):
        self.datapath = self.datapath.split("/",1)[0] + "/" + self.get_file_name() + self.datatype

    def get_file_name(self):
        return (self.date + "(" +
                str(self.timestamps) + "," +
                str(self.x) + "," +
                str(self.y) + "," +
                str(self.feats) + ")-" +
                self.clean)

    def save(self, path=PATH):
        if path:
            file = open(path + "/" + self.get_file_name() + ".cube", "w")
            file.write(self.__repr__())
            file.close()

    def save_data(self, path=None):
        if not path:
            fh.save(self.data, self.datapath)
        else:
            fh.save(self.data, path + ".npz")

    @staticmethod
    def load(full_path):
        if full_path.endswith(".cube"):
            file = open(full_path, "r")
            repr = file.read().strip().split(";")
            print(repr)
            file.close()
            c = Cube(repr[0], repr[1], fh.load_one(repr[2]))
            c.datapath  = repr[2]
            return c


    def __repr__(self):
        return (self.date + ";" +
                self.clean + ";" +
                self.datapath)

    def __eq__(self, other):
        return np.array_equal(self.data, other.data)
