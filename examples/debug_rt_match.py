# wl-28-07-2025, Mon: debug RT matching

# import warnings
# import sys
# import os
# import scipy
# import gzip
# import sqlite3
import re
# from collections import OrderedDict
import numpy as np
import janitor
import pandas as pd
from datascroller import scroll
import lamp_dev as mt
import utils as ut
import stats as st
from importlib import reload
# from inspect import getsource as source

reload(mt)

# =========================================================================
# data_set = False
data_set = False

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
    csv_out_s = "./res/d" + str(d) + "_lamp_s.tsv"
    csv_out_m = "./res/d" + str(d) + "_lamp_m.tsv"
else:
    d = "iSTOPP_C18aq_Neg"
    cols = [1, 2, 3, 4]
    ion_mode = "neg"
    data_dir = "./res/"
    # data_dir = "./data_wl/"
    d_data = data_dir + str(d) + ".xlsx"
    xlsx_out = "./res/" + str(d) + "_rt.xlsx"
    csv_out_s = "./res/" + str(d) + "_rt_s.tsv"
    csv_out_m = "./res/" + str(d) + "_rt_m.tsv"

df = mt.read_peak(d_data, cols, sep='\t')
df

# ========================================================================

# RT matching
rt_tol = 0.5
db_in = "./ref/rt_lib_202509.tsv"

# get reference library for matching
ref = mt.read_rt(db_in, ion_mode=ion_mode)
ref

# match compound based on exact mass
# ppm = 5.0
# res = mt.comp_match_mass(df, ppm, ref)

# RT match
res = mt.comp_match_rt(df, ref, rt_tol)
res.iloc[:, 0:5]

sr, mr = mt.comp_summ(df, res)

# wl-16-10-2025, Thu: save to Excel
# mr.to_csv(csv_out_m, sep="\t", index=False)
# sr.to_csv(csv_out_s, sep="\t", index=False)
with pd.ExcelWriter(xlsx_out, mode="w", engine="openpyxl") as writer:
    sr.to_excel(writer, sheet_name="single-row", index=False)
    mr.to_excel(writer, sheet_name="multiple-row", index=False)

# =========================== DEBUG =======================================

# wl-15-10-2025, Wed: load xlsx all sheets
df_dict = pd.read_excel("./ref/For_Wanchang_aqRP_RT_library_Sept2025.xlsx",
                        engine="openpyxl", sheet_name=None, header=0)
df_dict.keys()
df_pos = df_dict["POSITIVE ION MODE"]
df_neg = df_dict["NEGATIVE ION MODE"]

df_pos = (
    df_pos
    .clean_names()
    .remove_empty()
    .rename(columns=lambda x: re.sub("^rt.*", "rt_lib", x))
    .assign(rt_lib=lambda x: x["rt_lib"] * 60)
    .assign(ion_mod="positive")
)

df_neg = (
    df_neg
    .clean_names()
    .remove_empty()
    .rename(columns=lambda x: re.sub("^rt.*", "rt_lib", x))
    .assign(rt_lib=lambda x: x["rt_lib"] * 60)
    .assign(ion_mod="negative")
)

# =========================================================================
# wl-09-09-2025, Tue: Prepare rt library
df = pd.read_excel("./ref/For_Wanchang_aqRP_RT_library_Sept2025.xlsx",
                   sheet_name=0, header=0)
df_pos = (
    df
    .clean_names()
    .remove_empty()
    .rename(columns=lambda x: re.sub("^rt.*", "rt_lib", x))
    .assign(rt_lib=lambda x: x["rt_lib"] * 60)
    .assign(ion_mod="positive")
)

df = pd.read_excel("./ref/For_Wanchang_aqRP_RT library_Sept2025.xlsx",
                   sheet_name=1, header=0, engine='openpyxl')

df_neg = (
    df
    .clean_names()
    .remove_empty()
    .rename(columns=lambda x: re.sub("^rt.*", "rt_lib", x))
    .assign(rt_lib=lambda x: x["rt_lib"] * 60)
    .assign(ion_mod="negative")
)

rt_lib = pd.concat([df_pos, df_neg], axis=0, ignore_index=True, sort=False)
rt_lib.to_csv("./ref/rt_lib_202509.tsv", sep="\t", index=False)
rt_lib.to_excel("./ref/rt_lib_202509.xlsx", index=False)

# =========================================================================
# wl-28-07-2025, Mon: dummy RT values for reference file 
np.random.seed(101)
rt = df.rt
rt.describe()

s = np.random.uniform(1, 1000, ref.shape[0])
ref.insert(2, "rt", s)
ref.to_csv("./res/rt_lib", sep="\t", index=False)
