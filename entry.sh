#!/bin/sh

rsync -a --ignore-existing /app/_config/ /app/config/ > /dev/null
rsync -a --ignore-existing /app/_model/ /app/model/ > /dev/null
rsync -a --ignore-existing /app/_cache/ /app/cache/ > /dev/null

. ./bin/activate
python ./styles/info.py
streamlit run Chenyme-AAVT.py --browser.gatherUsageStats false
