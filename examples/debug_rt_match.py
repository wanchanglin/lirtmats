# wl-24-11-2025, Mon: debug RT matching
# wl-25-11-2025, Tue: debug embedded rt library
import sys
import pandas as pd
from lamp import anno
from lamp import utils
# from importlib import reload

if False:      # import installed 'lirtmats'
    import lirtmats.lirtmats as rtm
else:          # import local 'lirtmats'(for development)
    sys.path.append("../lirtmats")
    import lirtmats as rtm

# reload(rtm)

# =========================================================================
data_set = False
# data_set = True

if data_set:
    d = 3
    ion_mode = "pos"
    if d == 1:
        d_data = "./data/df_pos_1.tsv"
        cols = [1, 2, 3, 5]
    elif d == 2:
        d_data = "./data/df_pos_2.tsv"
        cols = [1, 3, 6, 11]
    else:
        d_data = "./data/df_pos_3.tsv"
        cols = [1, 2, 3, 4]
    db_out = "./res/d" + str(d) + "_lamp.db"
    tmp_out = "./res/d" + str(d) + "_tmp.tsv"
    xlsx_out = "./res/" + str(d) + "_rt.xlsx"
    csv_out_s = "./res/d" + str(d) + "_lamp_s.tsv"
    csv_out_m = "./res/d" + str(d) + "_lamp_m.tsv"
else:
    # d = "Nikik_HILIC_Pos"
    d = "iSTOPP_C18aq_Neg"
    cols = [1, 2, 3, 4]
    ion_mode = "neg"
    data_dir = "./res/"
    # data_dir = "./data_wl/"
    d_data = data_dir + str(d) + ".xlsx"
    # d_data = data_dir + str(d) + ".tsv"
    xlsx_out = "./res/" + str(d) + "_rt.xlsx"
    csv_out_s = "./res/" + str(d) + "_rt_s.tsv"
    csv_out_m = "./res/" + str(d) + "_rt_m.tsv"

df = anno.read_peak(d_data, cols, sep='\t')
df

# ========================================================================
# RT matching
rt_tol = 5
# db_in = "./ref/rt_lib_202509.tsv"
db_in = ""

# get reference library for matching
ref = rtm.read_rt(db_in, ion_mode=ion_mode)
ref

# RT match
res = rtm.comp_match_rt(df, ref, rt_tol)
res.iloc[:, 0:5]

sr, mr = anno.comp_summ(df, res)

# wl-16-10-2025, Thu: save to tsv or xlsx
# mr.to_csv(csv_out_m, sep="\t", index=False)
# sr.to_csv(csv_out_s, sep="\t", index=False)
# wl-25-11-2025, Tue: take time to save in xlsx format
utils._tic()
with pd.ExcelWriter(xlsx_out, mode="w", engine="openpyxl") as writer:
    sr.to_excel(writer, sheet_name="single-row", index=False)
    mr.to_excel(writer, sheet_name="multiple-row", index=False)
utils._toc()
