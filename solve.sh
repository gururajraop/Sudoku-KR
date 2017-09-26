#!/bin/sh

for f in ~/Documents/GitHub/Sudoku-KR/encodings/4/*
do
    ./minisat -verb=2 $f hey.txt;
    echo $f;
done