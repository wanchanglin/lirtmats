
# ------------------------------------------------------------------------
# wl-28-07-2025, Mon: RT matching
# wl-10-09-2025, Wed: Minor changes
def comp_match_rt(peak, ref, rt_tol=2):
    """
    Compound retention time match.

    This function performs compound match against retention time in
    reference library.

    Parameters
    ----------
    peak : DataFrame
        A pandas data frame of peak table. It must have "name", "mz" and
        "rt" columns.
    ref : DataFrame
        A pandas data frame of a RT library with "rt_lib" column.
    rt_tol : float
        A value for RT error tolerance.

    Returns
    -------
    DataFrame
        A pandas dataframe of RT library compound match table.
    """

    # ---------------------------------------------------------------------
    # wl-28-07-2025, Mon: select compounds based on RT values
    def comp_sel_rt(tab_name, col_names, cur, peak_id, rt, rt_tol):
        min = rt - rt_tol
        max = rt + rt_tol

        rec = []
        cur.execute(
            """
            SELECT * from {} where rt_lib >= {} and rt_lib <= {}
            """.format(tab_name, min, max)
        )
        rec = [OrderedDict(zip(col_names, list(record)))
               for record in cur.fetchall()]
        for record in rec:
            record["id"] = peak_id
            record["rt"] = rt
            record["rt_range"] = rt_tol
        return rec

    # ---------------------------------------------------------------------
    # convert df to sql for speedy match
    con = sqlite3.connect(":memory:")
    cur = con.cursor()
    ref.to_sql(name='ref', con=con, if_exists="replace", index=False)
    con.commit()

    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tab_name = list(cur.fetchall())[0][0]
    # set index for fast query
    cur.execute(
        "CREATE INDEX idx_rt_lib ON {} (rt_lib)".format(tab_name))

    # get table column names
    if True:
        col_names = ref.columns.to_list()
    else:
        cur.execute("SELECT * FROM {}".format(tab_name))
        col_names = list(map(lambda x: x[0], cur.description))

    # convert peak list to dictionary for query
    pk = df2dict(peak[["name", "rt"]])

    # annotation/match compounds
    res = [comp_sel_rt(tab_name, col_names, cur, x, pk[x], rt_tol)
           for x in pk]
    res = flatten_list(res)
    res = pd.DataFrame(res)

    res = (
        res
        # .sort_values(["id", "compound_id"], ignore_index=True)
        .drop_duplicates(ignore_index=True)
    )

    # move id and mz at the front
    cols_to_move = ['id', 'rt']
    res = res[cols_to_move +
              [x for x in res.columns if x not in cols_to_move]]

    # wl-17-09-2025, Wed: convert all ref as string
    cols = ref.columns.to_list()
    res = res.assign(**{c: lambda x, y=c: x[y].astype(str) for c in cols})

    con.close()

    return res

# ------------------------------------------------------------------------
# wl-10-09-2025, Wed: load rt library file matching
def read_rt(fn="", ion_mode="pos", sheet_name=0, sep="\t"):
    """
    Load retention time library for matching

    Parameters
    ----------
    fn : str
        Full path for an reference file. If empty, use default reference
        file. This file must have `formula` or `molecular_formula` column.
        The current supported file formats are text formats (csv, tsv, txt
        and dat) and Excel formats (xls, xlsx).
    ion_mode : str
        A string for ion mode, "pos" or "neg".
    sheet_name: str or int
        This argument is used for Excel file format. Strings are used for
        sheet names. Integers are used in zero-indexed sheet positions
        (chart sheets do not count as a sheet position).

        Available cases:

        * Defaults to ``0``: 1st sheet as a `DataFrame`
        * ``1``: 2nd sheet as a `DataFrame`
        * ``"Sheet1"``: Load sheet with name "Sheet1"

    sep : str
        Character to treat as the delimiter. It is used for text file
        format.

    Returns
    -------
    DataFrame
        Retention time library.

    Notes
    -----
    This function will replace column with "rt" as "rt_lib".
    """

    # load default reference library
    if not fn:
        path = 'lib/rt_lib.xlsx'
        # fn = os.path.join(
        #     os.path.dirname(os.path.abspath(lamp.__file__)), path
        # )
        fn = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), path
        )

    ext = os.path.splitext(fn)[1][1:]
    if ext in ['xls', 'xlsx']:
        df = pd.read_excel(fn, sheet_name=sheet_name, header=0)
    elif ext in ['txt', 'csv', 'tsv', 'dat']:
        df = pd.read_table(fn, header=0, sep=sep)
    else:
        raise ValueError("Data must be: xls, xlsx, txt, csv, tsv or dat.")

    # tidy up
    df = df.remove_empty().clean_names()

    if "rt_lib" not in df.columns:
        raise ValueError("Input data must have 'rt_lib' column.")

    if (df.rt_lib.dtype != "float64"):
        df = df.assign(rt_lib=lambda x: x["rt_lib"].astype(float))

    # wl-17-09-2025, Wed: should use regex for 'ion_*'
    if "ion_mode" in df and ion_mode:
        # 30-10-2024, Wed: use regex for case-insensitive and partial match
        idx = df['ion_mode'].str.contains(ion_mode, case=False)
        if idx.sum() > 0:
            df = df[idx]
        else:
            raise ValueError("Ion mode must be pos/positive or neg/negative.")

    return df
