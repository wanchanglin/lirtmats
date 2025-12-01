#!/usr/bin/env python
# -*- coding: utf-8 -*-

# wl-27-11-2025, Thu: commence
# wl-01-12-2025, Mon: debug and test
import os
import sys
import sqlite3
import pandas as pd
from functools import partial
from PySide6 import QtCore, QtWidgets
from lamp import anno
from lamp import utils
from lirtmats.qt import lirtmats_form
# import qt.lirtmats_form as lirtmats_form    # for debug
from lirtmats import lirtmats as rtm


# -------------------------------------------------------------------------
# wl-27-11-2025, Thu: commence
class lirtmats_app(QtWidgets.QMainWindow, lirtmats_form.Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(lirtmats_app, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # ---- Input data ----
        self.pushButton_wd.clicked.connect(
            partial(self.open_directory, self.lineEdit_wd)
        )
        self.pushButton_data.clicked.connect(
            partial(self.open_file, self.lineEdit_data)
        )

        # ---- Retention time Matching ----
        self.pushButton_ref.clicked.connect(
            partial(self.open_file, self.lineEdit_ref)
        )

        # ---- Save results ----
        self.pushButton_summ.clicked.connect(
            partial(self.save_file, self.lineEdit_summ, "rtm_summ")
        )
        self.pushButton_sql.clicked.connect(
            partial(self.save_file,
                    self.lineEdit_sql, "rtm_comp.db")
        )

        # ---- Others ----
        # self.path_wd = os.path.expanduser("~")
        self.path_wd = os.getcwd()

        self.pushButton_cancel.clicked.connect(
            QtCore.QCoreApplication.instance().quit
        )
        self.pushButton_start.clicked.connect(self.run)

    # ---------------------------------------------------------------------
    def open_directory(self, field):
        d = QtWidgets.QFileDialog.getExistingDirectory(
            None, "Select a folder", self.path_wd
        )
        if d:
            if str(d) == "":
                QtWidgets.QMessageBox.critical(
                    None,
                    "Select a folder",
                    "No folder selected",
                    QtWidgets.QMessageBox.Ok,
                )
            else:
                field.setText(d)
                self.path_wd = d
        return

    # ---------------------------------------------------------------------
    def open_file(self, field, field_extra=None):
        d = QtWidgets.QFileDialog.getOpenFileName(self, "Select File",
                                                  self.path_wd)
        if d:
            if str(d[0]) == "":
                QtWidgets.QMessageBox.critical(
                    None, "Select File", "No file selected",
                    QtWidgets.QMessageBox.Ok
                )
            else:
                field.setText(d[0])
                if field_extra and field_extra.text() == "Use default":
                    field_extra.setText(d[0])
        return

    # ---------------------------------------------------------------------
    def save_file(self, field, filename):
        d = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save File", os.path.join(self.path_wd, filename)
        )
        if d:
            if str(d[0]) == "":
                QtWidgets.QMessageBox.critical(
                    None,
                    "Save File",
                    "Provide a valid filename",
                    QtWidgets.QMessageBox.Ok,
                )
            else:
                field.setText(d[0])
        return

    # ---------------------------------------------------------------------
    def run(self):
        if not os.path.isfile(self.lineEdit_data.text()):
            QtWidgets.QMessageBox.critical(
                None,
                "Select file",
                "Select file(s) for input data (peak-list + intensity matrix)",
                QtWidgets.QMessageBox.Ok,
            )
            return

        # self.hide()
        self.pushButton_start.setEnabled(False)

        sepa = {"tab": "\t", "comma": ","}
        mode = {"Positive": "pos", "Negative": "neg"}

        # --------------------------------------------------------------
        if self.lineEdit_ref.text() == "Use default":
            ref_path = ""
        else:
            ref_path = self.lineEdit_ref.text()

        # -----------------------------------------------------------------
        # get data with peak list and intensity matrix
        cols = [
            self.spinBox_name_col.value(),
            self.spinBox_mz_col.value(),
            self.spinBox_rt_col.value(),
            self.spinBox_data_col.value(),
        ]

        # -----------------------------------------------------------------
        df = anno.read_peak(self.lineEdit_data.text(), cols=cols,
                            sep=sepa[self.comboBox_data_sep.currentText()])
        ref = rtm.read_rt(
            fn=ref_path,
            ion_mode=mode[self.comboBox_ion_mode.currentText()],
            sheet_name=0,
            sep=sepa[self.comboBox_ref_sep.currentText()]
        )

        utils._tic()
        res = rtm.comp_match_rt(peak=df, ref=ref,
                                rt_tol=self.doubleSpinBox_rt.value())
        print("\n***Retention time matching done***")

        # -----------------------------------------------------------------
        # retention time matching summary
        sr, mr = anno.comp_summ(df, res)
        print("\n***Summary done***")
        utils._toc()

        # -----------------------------------------------------------------
        # save all results to a sqlite database
        utils._tic()
        conn = sqlite3.connect(self.lineEdit_sql.text())
        df[["name", "mz", "rt"]].to_sql("peaklist", conn,
                                        if_exists="replace", index=False)
        mr.to_sql("rtm_mr", conn, if_exists="replace", index=False)
        sr.to_sql("rtm_sr", conn, if_exists="replace", index=False)
        conn.commit()
        conn.close()

        # save results into xlsx or text file with formats of tsv or csv.
        # The saving of xlsx takes considerable long time comparing with text
        # file saving.
        if self.comboBox_ext.currentText() == "xlsx":
            xlsx_out = self.lineEdit_summ.text() + ".xlsx"
            with pd.ExcelWriter(xlsx_out, mode="w", engine="openpyxl") as writer:
                sr.to_excel(writer, sheet_name="single-row", index=False)
                mr.to_excel(writer, sheet_name="multiple-row", index=False)
        elif self.comboBox_ext.currentText() == "tsv":
            tsv_out_s = self.lineEdit_summ.text() + "_s.tsv"
            tsv_out_m = self.lineEdit_summ.text() + "_m.tsv"
            sr.to_csv(tsv_out_s, sep="\t", index=False)
            mr.to_csv(tsv_out_m, sep="\t", index=False)
        else:
            csv_out_s = self.lineEdit_summ.text() + "_s.csv"
            csv_out_m = self.lineEdit_summ.text() + "_m.csv"
            sr.to_csv(csv_out_s, sep=",", index=False)
            mr.to_csv(csv_out_m, sep=",", index=False)

        print("\n***Save results done.***")
        utils._toc()

        print("\n***You may close this app.***\n")

        self.pushButton_start.setEnabled(True)
        # self.close()


# -------------------------------------------------------------------------
# wl-27-11-2025, Thu: test and debug GUI
def main():
    # Exception Handling
    try:
        app = QtWidgets.QApplication(sys.argv)
        form = lirtmats_app()
        form.show()
        sys.exit(app.exec())
    except NameError:
        print("Name Error:", sys.exc_info()[1])
    except SystemExit:
        print("Closing Window...")
    except Exception:
        print(sys.exc_info()[1])


# -------------------------------------------------------------------------
# wl-27-11-2025, Thu: command line: 'python gui.py' to test
if __name__ == '__main__':
    main()
