#!/bin/bash

python3 main.py
cp code_files/pMem.vhd ../sweep_CPU

#Om du får Bash script – "/bin/bash^M: bad interpreter: No such file or directory" skriv
#sed -i -e 's/\r$//' scriptname.sh och kör igen