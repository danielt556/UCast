import numpy as np
import matplotlib.pyplot as mpl


def get_stats(data, finvalid):
    fdata = data.astype("float32")
    vmeans = []
    vnzmeans = []
    vnz_invalid_means = []
    v_invalid_means = []

    for timestamp in range(fdata.shape[0]):
        tsdata = fdata[timestamp, :, :, :]
        vmeans.append(tsdata.mean())
        vnzmeans.append(tsdata.sum() / np.count_nonzero(tsdata))
        tsdata[finvalid(tsdata)] = np.nan
        v_invalid_means.append(np.nanmean(tsdata))
        tsdata[tsdata == 0] = np.nan
        vnz_invalid_means.append(np.nanmean(tsdata))

    return vmeans, vnzmeans, v_invalid_means, vnz_invalid_means


def plot(data, data_colors, data_labels, yaxis, xaxis="Timestamp",
         figsize=(20, 20), legend_location="best", save=False):
    if len(data) == 0:
        raise ValueError("Data is empty")
    if not len(data) == len(data_colors) == len(data_labels):
        raise ValueError("The number of data plots is not equal to the number of colors and labels")

    mpl.figure(figsize=figsize)
    mpl.axis("tight")
    mpl.grid(True, axis="y", linestyle='-')
    mpl.xlabel(xaxis, fontsize=25)
    mpl.ylabel(yaxis, fontsize=25)

    MIN = min(data[0])
    MAX = max(data[0])

    for idx in range(len(data)):
        MIN = min(MIN, min(data[idx]))
        MAX = max(MAX, max(data[idx]))
        mpl.plot(data[idx], data_colors[idx], label=data_labels[idx])

    xstep = 10
    mpl.xlim((0, 235))
    mpl.xticks(np.arange(0, len(data[0]) + 5, xstep), fontsize=15)
    ystep = (MAX - MIN) // (figsize[1] * 1.5) or (MAX - MIN) / (figsize[1] * 1.5)
    try:
        mpl.yticks(np.arange(MIN - ystep, MAX + ystep, ystep), fontsize=15)
    except ValueError as e:
        print(e, MIN, MAX, ystep)
    mpl.legend(loc=legend_location, prop={'size': figsize[0]})
    mpl.show()

    if save:
        mpl.savefig("05-06-17-" + yaxis + "-" + str(len(data)))
