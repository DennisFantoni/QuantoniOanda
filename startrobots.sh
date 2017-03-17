#!/bin/bash
#cd ./IdeaProjects/QuantoniOanda
gnome-terminal --title="housekeeping" -x ./housekeeping.sh

#for i in {04_01,04_03,04_04,02_01,06_01}
#for i in {02_25,02_20,02_15,02_10,03_30,03_25,03_20,03_15,03_10,05_13,05_11,05_09,05_07,05_05,06_13,06_11,06_09,06_07,06_05}
for i in {02_25,02_20,02_15,02_10,03_30,03_25,03_20,03_15,03_10,06_13,06_11,06_09,06_07,06_05}
do
    gnome-terminal --title="robot_$i" -x ./robot_$i.sh $@
done
x-tile g 5 3
