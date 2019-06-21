import numpy as np
import matplotlib.pyplot as mpl
from core.config import IS_INVALID_R, IS_INVALID_V


class Plotter:
    def __init__(self, data, date_and_clean, feat_name):
        self.feat_name = feat_name
        if len(data) == 0:
            raise ValueError("Data is empty")
        self.data = data
        if feat_name == "R":
            self.finvalid = IS_INVALID_R
        elif feat_name == "V":
            self.finvalid = IS_INVALID_V
        else:
            self.finvalid = lambda x: False
        self.stats = self.get_stats()
        self.date_and_clean = date_and_clean

    def get_stats(self):
        results = []
        for d in self.data:
            fdata = d.astype("float32")
            vmeans = []
            vnzmeans = []
            vnz_invalid_means = []
            v_invalid_means = []

            for timestamp in range(fdata.shape[0]):
                tsdata = fdata[timestamp, :, :, :]
                vmeans.append(tsdata.mean())
                #vnzmeans.append(tsdata.sum() / np.count_nonzero(tsdata))
                tsdata[self.finvalid(tsdata)] = np.nan
                v_invalid_means.append(np.nanmean(tsdata))
                #tsdata[tsdata == 0] = np.nan
                #vnz_invalid_means.append(np.nanmean(tsdata))

            #results.append((vmeans, vnzmeans, v_invalid_means, vnz_invalid_means))
            results.append((vmeans, v_invalid_means))
        return results

    def plot(self, xaxis="Timestamp",
             figsize=(20, 20), legend_location="best", save=False):

        # for stat in self.stats:
        #     if not len(stat) == len(data_colors) == len(data_labels):
        #         raise ValueError("The number of data plots is not equal "
        #                             "to the number of colors and labels")

        data_colors = ("red", "green")
        #data_labels =
        yaxis = "Mean value " + self.feat_name


        mpl.figure(figsize=figsize)
        mpl.axis("tight")
        mpl.grid(True, axis="y", linestyle='-')
        mpl.xlabel(xaxis, fontsize=25)
        mpl.ylabel(yaxis, fontsize=25)

        MIN = min(self.stats[0][0])
        MAX = max(self.stats[0][0])

        for statidx in range(len(self.stats)):
            stat = self.stats[statidx]
            dandc = self.date_and_clean[statidx]
            #print(len(self.stats), " ", len(stat))
            means = stat[0]
            ignoring = stat[1]
            MIN = min(MIN, min(means), min(ignoring))
            MAX = max(MAX, max(means), max(ignoring))
            mpl.plot(means, data_colors[0], label="mean" + dandc)
            mpl.plot(ignoring, data_colors[1], label="ignore" + dandc)

        xstep = 10
        mpl.xlim((0, len(self.stats[0])))
        mpl.xticks(np.arange(0, len(self.stats[0][0]) + 5, xstep), fontsize=15)
        ystep = (MAX - MIN) // (figsize[1] * 1.5) or (MAX - MIN) / (figsize[1] * 1.5)
        try:
            mpl.yticks(np.arange(MIN - ystep, MAX + ystep, ystep), fontsize=15)
        except ValueError as e:
            print(e, MIN, MAX, ystep)
        mpl.legend(loc=legend_location)
        mpl.show()
        print("done")

        if save:
            mpl.savefig("05-06-17-" + yaxis + "-" + str(len(self.stats[0])))
