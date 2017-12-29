# Sudoku-KR

## **Contributors:**
* Gururaja Rao P
* [Linda Petrini](https://github.com/LindaPetrini)


* [Paper](https://github.com/gururajraop/Sudoku-KR/blob/master/Tex/report.pdf)
* [Presentation](https://docs.google.com/presentation/d/1LLf5MYiiOk9Ahzr1Jxybnudsi8cje2qFx2RU3oixYFY/edit?usp=sharing)
              
## **Requirements:**
* OS: Linux/Mac
* Programs: Python3
* Cmake/Make

## **To install minisat please follow below steps:**
```shell
$git clone https://github.com/pascalesser/minisat.git
$cd minisat
$mkdir build
$make config prefix=<CURRENT_DIRECTORY/build>
$make install
```
If the minisat build directory is not in your PATH, add it using below command.
```shell
$export PATH=$PATH:<PATH_TO_MINISAT_REPO>/build/
```
For more details and test click [here](https://github.com/pascalesser/minisat.git)

### **How to Run**
```shell
./run_sudoku.sh
```
