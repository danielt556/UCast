from data.config import PATH, startV, endV, IS_INVALID_V
import data.fileHandler as fh
from data.ploter import get_stats, plot

befdata = fh.load_each()
aftdata = fh.load_one(PATH + "/ALL_DAY-CLEAN(231, 624, 800, 24).npz")
befvdata = befdata[:, :, :, startV:endV]
aftvdata = aftdata[:, :, :, startV:endV]
print("All V before")
bef_v_stats = get_stats(befvdata, IS_INVALID_V)
bef_v_means, bef_v_nz_means, bef_v_invalid_means, bef_vnz_invalid_means = bef_v_stats
print("All V after")
aft_v_stats = get_stats(aftvdata, IS_INVALID_V)
aft_v_means, aft_v_nz_means, aft_v_invalid_means, aft_vnz_invalid_means = aft_v_stats

plot((bef_v_means, aft_v_means, bef_v_invalid_means),
        ("red", "green", "blue"),
        ("Before cleaning", "After cleaning", "Ignoring invalid values"),
        "Mean value V")
plot((aft_v_means, bef_v_invalid_means),
        ("green", "blue"),
        ("After cleaning", "Ignoring invalid values"),
        "Mean value V")

vnames = ["V0" + str(i) for i in (1, 2, 3, 4, 6, 7)]
for i in range(endV-startV):
    print("Before " + str(i + 1))
    bef_stats = get_stats(befvdata[:, :, :, i:i + 1], IS_INVALID_V)
    bef_v_means, bef_v_nz_means, bef_v_invalid_means, bef_vnz_invalid_means = bef_stats
    print("After " + str(i + 1))
    aft_stats = get_stats(aftvdata[:, :, :, i:i + 1], IS_INVALID_V)
    aft_v_means, aft_v_nz_means, aft_v_invalid_means, aft_vnz_invalid_means = aft_stats
    plot((bef_v_means, aft_v_means, bef_v_invalid_means),
            ("red", "green", "blue"),
            ("Before cleaning", "After cleaning", "Ignoring invalid values"),
            "Mean " + vnames[i])
    plot((aft_v_means, bef_v_invalid_means),
            ("green", "blue"),
            ("After cleaning", "Ignoring invalid values"),
            "Mean " + vnames[i])
