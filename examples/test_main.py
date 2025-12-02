#!/usr/bin/env python
# -*- coding: utf-8 -*-

# wl-01-12-2025, Mon: lirtmats command-line workflow. Consistent with
# 'lirtmats cli'.

import os
import sys
import sqlite3
import pandas as pd
from lamp import anno
from lamp import utils
if False:      # import installed 'lirtmats'
    import lirtmats.lirtmats as rtm
else:          # import local 'lirtmats'(for development)
    sys.path.append("../lirtmats")
    import lirtmats as rtm


# -------------------------------------------------------------------------
def lirtmats_cmd(args):
    # convert dictionary to pandas series for dot use
    args = pd.Series(args)
    print(args)
    separators = {"tab": "\t", "comma": ","}

    # get data with peak list and intensity matrix
    idx_list = [int(item.strip()) for item in args.col_idx.split(',')]
    df = anno.read_peak(fn=args.input_data, cols=idx_list,
                        sep=separators[args.input_sep])

    # load retention time reference.
    ref = rtm.read_rt(fn=args.rt_path,
                      ion_mode=args.ion_mode,
                      sheet_name=0,
                      sep=separators[args.rt_sep])

    utils._tic()
    # retention time matching
    res = rtm.comp_match_rt(peak=df, ref=ref, rt_tol=args.rt_tol)

    # get summary of retention time matching
    sr, mr = anno.comp_summ(df, res)
    utils._toc()

    # get file name for results
    # extract data file name and path
    fn= os.path.splitext(args.input_data)[0]

    utils._tic()
    # save all results to a sqlite database or not
    if args.save_db:
        db_out = fn + "_rtm" + ".db"
        conn = sqlite3.connect(db_out)
        df[["name", "mz", "rt"]].to_sql("peaklist", conn,
                                        if_exists="replace", index=False)
        mr.to_sql("anno_mr", conn, if_exists="replace", index=False)
        sr.to_sql("anno_sr", conn, if_exists="replace", index=False)

        conn.commit()
        conn.close()

    if args.summ_type == "xlsx":
        xlsx_out = fn + "_rtm" + ".xlsx"
        with pd.ExcelWriter(xlsx_out, mode="w", engine="openpyxl") as writer:
            sr.to_excel(writer, sheet_name="single-row", index=False)
            mr.to_excel(writer, sheet_name="multiple-row", index=False)
    elif args.summ_type == "tsv":
        tsv_out_s = fn + "_rtm" + "_s.tsv"
        tsv_out_m = fn + "_rtm" + "_m.tsv"
        sr.to_csv(tsv_out_s, sep="\t", index=False)
        mr.to_csv(tsv_out_m, sep="\t", index=False)
    else:
        csv_out_s = fn + "_rtm" + "_s.csv"
        csv_out_m = fn + "_rtm" + "_m.csv"
        sr.to_csv(csv_out_s, sep=",", index=False)
        mr.to_csv(csv_out_m, sep=",", index=False)

    utils._tic()

    return


# -------------------------------------------------------------------------
def main():

    # --------------------------
    # User's parameters setting
    # --------------------------

    args = {
        # 1.) load input data
        # 'input_data': "./data/df_pos_3.tsv",
        'input_data': "./res/iSTOPP_C18aq_Pos.xlsx",
        'col_idx': "1, 2, 3, 4",
        'input_sep': "tab",                  # file separator: '\t' or ','

        # 2.) compounds annotation with reference and adduct files
        # 'rt_path': "",        # default retention time reference
        'rt_path': "./ref/rt_lib_202509.tsv",
        'rt_sep': "tab",
        'rt_tol': 5.0,         # rt torrance threshold
        'ion_mode': "pos",     # Ion mode of data set

        # 3.) results outcome
        'save_db': True,       # save all results in sqlite database
        'summ_type': "xlsx"    # summary file type
    }

    # -----------
    # run lirtmats
    # -----------
    lirtmats_cmd(args)
    print(args['input_data'], "****Done****")


# -------------------------------------------------------------------------
if __name__ == '__main__':
    main()
