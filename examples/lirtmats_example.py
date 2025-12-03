# wl-24-11-2025, Mon: debug RT matching
# wl-25-11-2025, Tue: debug embedded rt library
import sys
from lamp import anno
from lamp import utils

if True:      # import installed 'lirtmats'
    import lirtmats.lirtmats as rtm
else:          # import local 'lirtmats'(for development)
    sys.path.append("../lirtmats")
    import lirtmats as rtm

# data loading
d_data = "./data/df_pos_3.tsv"
cols = [1, 2, 3, 4]

df = anno.read_peak(d_data, cols, sep='\t')
df

# RT matching
rt_tol = 5
ion_mode = "pos"
rt_ref = "./data/rt_lib_202509.tsv"

# get reference library for matching
ref = rtm.read_rt(rt_ref, ion_mode=ion_mode)
ref

# RT match
utils._tic()
res = rtm.comp_match_rt(df, ref, rt_tol)
sr, mr = anno.comp_summ(df, res)
utils._toc()

res.iloc[:, 0:5]
sr.head(10)
mr.tail(10)