import numpy as np
from scipy.spatial import distance
from config import IS_INVALID_R, IS_INVALID_V, startR, endR, startV, endV


def get_weights(pdata, point, fdist, finvalid):
    """
    Construct a matrix of weights based on the data and distance from the centre.

    pdata = 2 dimention matrix containing the data (just x and y axis, no time/feat)
    point = point of interest, the point that we want to aproximate as (x, y) touple
    fdist = function to calculate the distance by
    finvalid = function that defines if a value is invalid
    """
    dist_sum = 0
    weights = np.zeros(pdata.shape)
    for rowNo in range(len(pdata)):
        for colNo in range(len(pdata[rowNo])):
            if not finvalid(pdata[rowNo][colNo]):
                dist = fdist((rowNo, colNo), (point[0], point[1]))
                weights[rowNo][colNo] = 1 / dist if dist != 0 else 0
                dist_sum += 1 / dist if dist != 0 else 0
    if dist_sum != 0:
        weights = weights / dist_sum
    return weights


def aprox_point(fdata, point, No_neighbours, fdist, finvalid):
    """
    Aproximate the value of an invalid point based on its neighbours.
    This functions assumes time is the first dimention of the matrix and feat is the last.

    fdata = 4 dimention matrix containing the data
    point = 4-tuple as (time coordonate,
                       x coordonate,
                       y coordonate,
                       feat number(see comment bellow FIELDS definition)
    No_neighbours = number of neighbours in each direction to take
    fdist = function to calculate the distance by
    finvalid = function that defines if a value is invalid
    """
    time = point[0]

    x_start = point[1] - No_neighbours if point[1] >= No_neighbours else 0
    x_end = point[1] + No_neighbours + 1

    y_start = point[2] - No_neighbours if point[2] >= No_neighbours else 0
    y_end = point[2] + No_neighbours + 1

    feat = point[3]

    pdata = fdata[time, x_start: x_end, y_start: y_end, feat]
    weights = get_weights(
        pdata, (point[1] - x_start, point[2] - y_start), fdist, finvalid)
    if np.sum(weights) != 0:
        return np.average(pdata, weights=weights)
    else:
        return aprox_point(fdata, point, No_neighbours + 1, fdist, finvalid)


def clean_field(field, data, No_neighbours=6, fdist=distance.euclidean):
    """
    Clean a feature.

    field = str R or V , or list containing one or more of these values.
    data = 4 dimention matrix containing the data
    No_neighbours = number of neighbours in each direction to take
    fdist = function to calculate the distance by
    """
    finvalid = None
    if field == 'R':
        startf = startR
        finvalid = IS_INVALID_R
        invalid_points = list(
            zip(*np.where(IS_INVALID_R(data[:, :, :, range(startR, endR)]))))
    elif field == 'V':
        startf = startV
        finvalid = IS_INVALID_V
        invalid_points = list(
            zip(*np.where(IS_INVALID_V(data[:, :, :, range(startV, endV)]))))
    elif isinstance(field, list):
        for f in field:
            clean_field(f, data, No_neighbours, fdist)
    else:
        raise ValueError('Unsupported field')
    i = 1
    for point in invalid_points:
        # correction for the above slicing
        point = *point[0:3], point[3] + startf
        newp = aprox_point(data, point, No_neighbours, fdist, finvalid)
        # aprox_point(data, point, No_neighbours, fdist, finvalid)
        data[point] = round(newp)
        if i % 1000 == 0:
            print(str(i) + "/" + str(len(invalid_points)))
        i += 1