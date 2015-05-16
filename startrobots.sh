#!/bin/bash
#cd ./IdeaProjects/QuantoniOanda
gnome-terminal --title="housekeeping" -x ./housekeeping.sh

#for i in {04_01,04_03,04_04,02_01,06_01}
for i in {01_03,01_04,01_05,02_01,02_02,02_03,03_01,03_02,03_03,03_04,03_06,05_06,05_09,05_12,05_15,06_02,06_03,06_04}
do
    gnome-terminal --title="robot_$i" -x ./robot_$i.sh $@
done
x-tile g 5 3
