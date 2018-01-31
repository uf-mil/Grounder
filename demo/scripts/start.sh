#!/bin/bash
git clone https://github.com/uf-mil/Groundr.git
export port=$2
export host=$1
cd Groundr
python3 main.py

