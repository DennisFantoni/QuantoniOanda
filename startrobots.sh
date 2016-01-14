#!/bin/bash
#cd ./IdeaProjects/QuantoniOanda
gnome-terminal --title="housekeeping" -x ./housekeeping.sh

#for i in {04_01,04_03,04_04,02_01,06_01}
for i in {01_15,01_12,01_09,02_25,02_20,02_15,03_30,03_25,03_20,03_15,03_10,05_15,05_12,05_09,05_06,06_15,06_20,06_10}
do
    gnome-terminal --title="robot_$i" -x ./robot_$i.sh $@
done
x-tile g 5 3
