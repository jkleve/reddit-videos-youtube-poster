#!/bin/bash

# https://serverfault.com/questions/103501/how-can-i-fully-log-all-bash-scripts-actions
exec 3>&1 4>&2
trap 'exec 2>&4 1>&3' 0 1 2 3
exec 1>log.out 2>&1

if [ -f venv/bin/activate ]; then
    source venv/bin/activate
else
    echo "ERROR: No virtualenv found!"
    exit 1
fi

python runner.py
