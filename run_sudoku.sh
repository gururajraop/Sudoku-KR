#!/bin/sh
python script.py

for f in ~/Documents/GitHub/Sudoku-KR/encodings/3/naive/*
do
    minisat -verb=2 $f solution.txt;
    echo $f;
done

python plots.py
