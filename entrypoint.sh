#!/bin/bash

if [ -f "data/generated/data_full.csv.gz" ]; then
    gunzip data/generated/data_full.csv.gz
fi

python -i main.py
