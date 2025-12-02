#!/usr/bin/env bash
# wl-02-12-2025, Mon: command-line test script
 
lirtmats cli \
  --input-data "./data/df_pos_3.tsv" \
  --input-sep "tab" \
  --col-idx "1, 2, 3, 4" \
  --rt-path "" \
  --rt-sep "tab" \
  --rt-tol "5.0" \
  --ion-mode "pos" \
  --save-db \
  --summ-type "xlsx" \
