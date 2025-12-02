#!/usr/bin/env python
# -*- coding: utf-8 -*-

# wl-25-11-2025, Tue: commence
# wl-02-12-2025, Mon: major changes

from lirtmats import __version__
import argparse
import os
import sys
import sqlite3
import pandas as pd
from PySide6.QtWidgets import QApplication
from lamp import anno
from lirtmats import gui
from lirtmats import lirtmats as rtm


# --------------------------------------------------------------------------
def main():
    separators = {"tab": "\t", "comma": ","}

    print("Executing lirtmats version {}.".format(__version__))

    parser = argparse.ArgumentParser(
        description='Retention Time Matching of LC-MS data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    subparsers = parser.add_subparsers(dest='step')
    parser_am = subparsers.add_parser('cli',
                                      help='Retention Time Matching in CLI.')
    parser_gui = subparsers.add_parser('gui',
                                       help='Retention Time Matching in GUI.')

    # ---------------------------------------------------------------------
    # data loading
    parser_am.add_argument('--input-data', type=str, required=True,
                           help="Data set including peak-list.")
    parser_am.add_argument('--col-idx', default="1,2,3,4", type=str,
                           help="Column index of name, mz, rt and start of"
                                " data intensity")
    parser_am.add_argument('--input-sep', default="tab", type=str,
                           choices=["tab", "comma"],
                           help="Values in input or output file are "
                                "separated by this character.")

    # ---------------------------------------------------------------------
    # compounds annotation with reference and adduct files
    parser_am.add_argument('--rt-path', type=str, default=None,
                           required=False,
                           help="Retention time reference file for matching.")
    parser_am.add_argument('--rt-sep', default="tab", type=str,
                           choices=["tab", "comma"],
                           help="Delimiter in retention time reference file")
    parser_am.add_argument('--rt-tol', default=5.0, type=float,
                           help="Retention time tolerance in seconds.")
    parser_am.add_argument('--ion-mode', default='pos', type=str,
                           choices=["pos", "neg"],
                           help="Ion mode of data set.")

    # ---------------------------------------------------------------------
    # results outcome
    parser_am.add_argument('--save-db', action="store_true",
                           help="Save all results in a sql database.")
    parser_am.add_argument('--summ-type', default="xlsx", type=str,
                           choices=["xlsx", "tsv", "csv"],
                           help="Retention time matching result file format.")

    # ---------------------------------------------------------------------
    args = parser.parse_args()
    print(args)

    if args.step == "cli":

        # -----------------------------------------------------------------
        # get data with peak list and intensity matrix
        idx_list = [int(item.strip()) for item in args.col_idx.split(',')]
        df = anno.read_peak(fn=args.input_data, cols=idx_list,
                            sep=separators[args.input_sep])

        # -----------------------------------------------------------------
        # load retention time reference.
        ref = rtm.read_rt(fn=args.rt_path,
                          ion_mode=args.ion_mode,
                          sheet_name=0,
                          sep=separators[args.rt_sep])

        # -----------------------------------------------------------------
        # retention time matching
        res = rtm.comp_match_rt(peak=df, ref=ref, rt_tol=args.rt_tol)

        # -----------------------------------------------------------------
        # get summary of retention time matching
        sr, mr = anno.comp_summ(df, res)

        # get file name for results
        # extract data file name and path
        fn = os.path.splitext(args.input_data)[0]

        # -----------------------------------------------------------------
        # save all results to a sqlite database or not
        if args.save_db:
            db_out = fn + "_rtm" + ".db"
            conn = sqlite3.connect(db_out)
            df[["name", "mz", "rt"]].to_sql("peaklist", conn,
                                            if_exists="replace", index=False)
            mr.to_sql("rtm_mr", conn, if_exists="replace", index=False)
            sr.to_sql("rtm_sr", conn, if_exists="replace", index=False)

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

    if args.step == "gui":
        # Exception Handling
        try:
            app = QApplication(sys.argv)
            form = gui.lirtmats_app()
            form.show()
            sys.exit(app.exec())
        except NameError:
            print("Name Error:", sys.exc_info()[1])
        except SystemExit:
            print("Closing Window...")
        except Exception:
            print(sys.exc_info()[1])


# -------------------------------------------------------------------------
if __name__ == '__main__':
    main()
