rem  wl-03-12-2025, Wed:command-line test script for windows
 
lirtmats cli ^
  --input-data "./data/df_pos_3.tsv" ^
  --input-sep "tab" ^
  --col-idx "1, 2, 3, 4" ^
  --rt-path "./data/rt_lib_202509.tsv" ^
  --rt-sep "tab" ^
  --rt-tol "5.0" ^
  --ion-mode "pos" ^
  --save-db ^
  --summ-type "tsv"
