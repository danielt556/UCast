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


PATH = r"data"  # load and save folder path
SAVE_FILE_NAME = "ALL_DAY"

ALL_FIELDS = list(range(24))
Rs24 = list(range(6, 12))
Vs24 = list(range(17, 23))
VIL24 = [23]


Rs13 = list(range(0, 6))
Vs13 = list(range(6, 12))
VIL13 = [12]

def IS_INVALID_R(x): return (x < 0) | (x > 75) | (x % 5 != 0)
def IS_INVALID_V(x): return (x < -33) | (x > 33)

#FIELDS, startR, endR, startV, endV, startVIL, endVIL = set_fields('ALL')

#print(Rs[0])
