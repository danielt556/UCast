def set_fields(ftype):
    if ftype not in ['R', 'V', 'R,V', 'R,V,VIL', 'ALL']:
        raise ValueError("Unsupported field type")

    if ftype == 'R':
        field_list = Rs
        startR, endR = 0, len(Rs)
        startV = endV = None
        startVIL = endVIL = None

    if ftype == 'V':
        field_list = Vs
        startV, endV = 0, len(Vs)
        startR = endR = None
        startVIL = endVIL = None

    if ftype == 'R,V':
        field_list = Rs + Vs
        startR, endR = 0, len(Rs)
        startV, endV = endR, endR + len(Vs)
        startVIL = endVIL = None

    if ftype == 'R,V,VIL':
        field_list = Rs + Vs
        startR, endR = 0, len(Rs)
        startV, endV = endR, endR + len(Vs)
        startVIL = endVIL = endV

    if ftype == 'ALL':
        field_list = ALL_FIELDS
        startR, endR = 6, 6 + len(Rs)
        startV, endV = 17, 17 + len(Vs)
        startVIL = endVIL = 23

    return field_list, startR, endR, startV, endV, startVIL, endVIL


PATH = "/home/tdaniel/xception/Date-05-06-17"  # load and save folder path
SAVE_FILE_NAME = "ALL_DAY"

ALL_FIELDS = list(range(24))
Rs = list(range(6, 12))
Vs = list(range(17, 23))
VIL = [23]
IS_INVALID_R = lambda x: (x < 0) | (x > 75) | (x % 5 != 0)
IS_INVALID_V = lambda x: (x < -33) | (x > 33)
#def IS_INVALID_R(x): return (x < 0) | (x > 75) | (x % 5 != 0)
#def IS_INVALID_V(x): return (x < -33) | (x > 33)
FIELDS, startR, endR, startV, endV, startVIL, endVIL = set_fields('ALL')
# FIELDS = {6:"R01", 7:"R02", 8:"R03", 9:"R04", 10:"R06", 11:"R07", 17:"V01",
#           18:"V02", 19:"V03", 20:"V04", 21:"V06", 22:"V07"}#, 23:"VIL"}
# for data 0:"R01", 1:"R02", 2:"R03", 3:"R04", 4:"R06", 5:"R07", 6:"V01",
# 7:"V02", 8:"V03", 9:"V04", 10:"V06", 11:"V07"
