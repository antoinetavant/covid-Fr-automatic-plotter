#!/usr/bin/env bash

echo "running python scrtip"
python3 /home/pi/covid/covid.py

echo "script finished, pushing on github"

cd /home/pi/covid/myblog/

git pull

cp /home/pi/covid/covid_positivity_days.png /home/pi/covid/myblog/static/images/blog/covid_positivity_days.png

git add /home/pi/covid/myblog/static/images/blog/covid_positivity_days.png

now=$(date +'%m/%d/%Y')

git commit -m"Update covid image ${now}"
git push
