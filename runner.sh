#!/bin/bash

if [ -f venv/bin/activate ]; then
    source venv/bin/activate
else
    echo "ERROR: No virtualenv found!"
    exit 1
fi

python runner.py
