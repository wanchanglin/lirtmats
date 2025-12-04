# # Quick Start
#
# This python script describes how to use `LiRTMaTS` python package. The
# input data and retention time reference files used here are in
# https://github.com/wanchanglin/lirtmats/tree/master/examples/data.
#
# ## Setup
#
# The users need to load python package `LAMP` before using `LiRTMaTS`. It's
# functions used here are for loading data set and summarising the matching
# results. For details, see https://github.com/wanchanglin/lamp.

import sqlite3
import pandas as pd
from lamp import anno
import lirtmats.lirtmats as rtm

# ## Data Loading
#
# `LiRTMaTS` supports text files separated by comma (`,`) or tab (`\t`).
# The Microsoft's XLSX is also supported, using argument `sheet_name` to
# indicate which sheet is used for input data. The default is 0 for the
# first sheet.
#
# Here we use a small example data set with `tsv` format. This data set
# includes peak list and intensity data matrix. `LiRTMaTS` requires peak
# list's name, m/z value and retention time. User needs to indicate the
# locations of feature name, m/z value, retention time and starting points
# of data matrix from data. Here they are 1, 2, 3 and 4, respectively.
#

cols = [1, 2, 3, 4]
data_fn = "./data/df_pos_3.tsv"                 # use tsv file
df = anno.read_peak(data_fn, cols, sep='\t')
df

# Data frame `df` now includes only `name`, `mz`, `rt` and intensity data
# matrix.
#
# ## Retention Time Matching
#
# To perform retention time matching, users use either default retention
# time library or their own reference file. The reference file must have one
# column: `rt_lib` which is used for retention time matching with a range or
# torrance in seconds. Also the column `ion_mode` should be required for
# indication of positive or negative mode matching. If `ion_mode` is not
# included in the reference file, all rows will be used for matching.
#

ion_mode = "pos"
# ref_path = ""  # if empty, use default reference file for matching
ref_path = "./data/rt_lib_202509.tsv"
ref = rtm.read_rt(ref_path, ion_mode=ion_mode)
ref

# `rt_tol` is a threshold for the retention time matching window. The unit
#  is seconds and the default value is 5.

rt_tol = 5
res = rtm.comp_match_rt(df, ref, rt_tol)
res

# ## Summarize Results
#
# The function `comp_summ` in package `LAMP`  summarises the retention time
# matching.

sr, mr = anno.comp_summ(df, res)

# This function combines peak table with retention time matching results and
# returns two results in different formats. `sr` is single row results for
# each peak id in peak table `df`:

sr

# `mr` is multiple rows format if the match more than once from the reference
# file:

mr

# All of results can be saved into a `sqlite3` database and use
# [DB Browser for SQLite](https://sqlitebrowser.org/) to view. Or save these
# results in other formats, such as TSV, CSV or XLSX, separately.

f_save = False          # here we do NOT save results
db_out = "test.db"
sr_out = "test_s.tsv"
mr_out = "test_m.tsv"
xlsx_out = "test.xlsx"

if f_save:
    # save all results into a sqlite3 database
    conn = sqlite3.connect(db_out)
    df[["name", "mz", "rt"]].to_sql("peaklist",
                                    conn,
                                    if_exists="replace",
                                    index=False)
    mr.to_sql("anno_mr", conn, if_exists="replace", index=False)
    sr.to_sql("anno_sr", conn, if_exists="replace", index=False)

    conn.commit()
    conn.close()

    # save results into text files
    sr.to_csv(sr_out, sep="\t", index=False)
    mr.to_csv(mr_out, sep="\t", index=False)

    # save results into Excel format
    with pd.ExcelWriter(xlsx_out, mode="w", engine="openpyxl") as writer:
        sr.to_excel(writer, sheet_name="single-row", index=False)
        mr.to_excel(writer, sheet_name="multiple-row", index=False)

# It should be noted that saving of Excel file takes much longer time than
# text files.
#
# ## End User Usages
#
# `LiRTMaTS` provides two computation options: command line interface(CLI)
# and graphical user interface (GUI).
#
# To use GUI,  you need to open a terminal and type in:
#
# ```bash
# $ lirtmats gui
# ```
#
# To use CLI, open a terminal and type in command with required arguments,
# something like:
#
# ```bash
# lirtmats cli \
#   --input-data "./data/df_pos_3.tsv" \
#   --input-sep "tab" \
#   --col-idx "1, 2, 3, 4" \
#   --rt-path "" \
#   --rt-sep "tab" \
#   --rt-tol "5.0" \
#   --ion-mode "pos" \
#   --save-db \
#   --summ-type "xlsx" \
# ```
#
# Execution of this command line will produce `df_pos_3_rtm.db` and
# `df_pos_3_rtm.xlsx` in the directory `./data/`. If the `summ-type` is `tsv`
# or `csv`, files `df_pos_3_rtm_s.tsv` or `df_pos_3_rtm_s.csv` and
# `df_pos_3_rtm_m.tsv` or `df_pos_3_rtm_m.csv` will be saved into `./data`.
#
# For the best practice, you can create a bash script `.sh` (Linux
# and MacOS) or Windows script `.bat` to contain these CLI
# arguments. Change parameters in these files each time when processing new
# data set.
#
# For example, there are `lirtmats_cli.sh` and `lirtmats_cli.bat` in
# https://github.com/wanchanglin/lirtmats/tree/master/examples.
#
# - For Linux and MacOS terminal:
#
#   ```bash
#   $ chmod +x lirtmats_cli.sh
#   $ ./lirtmats_cli.sh
#   ```
#
# - For Windows terminal:
#
#   ```bash
#   $ lirtmats_cli.bat
#   ```
#
# Note that if users use `xlsx` files for input data and reference file when
# using GUI or CLI, all data must be in the first sheet. If you use
# `LiRTMaTS` functions in your python scripts, there are no such
# requirements.
