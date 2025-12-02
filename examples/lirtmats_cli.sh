#!/usr/bin/env bash
# wl-07-10-2024, Mon: command-line test script
 
python lirtmats.py cli \
  --input-data "../examples/data/df_pos_3.tsv" \
  --input-sep "tab" \
  --col-idx "1, 2, 3, 4" \
  --rt-path "./lib/rt_lib_202509.xlsx" \
  --rt-sep "tab" \
  --ion-mode "pos" \
  --positive \
  --rt "5.0" \
  --save-db \
  --summ-type "comma" \
